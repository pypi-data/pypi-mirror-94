""" Transformer based chatbot dialog engine for answering questions """

import logging
import os
import urllib.request
import uuid
import zipfile
from pathlib import Path
import numpy as np
from multiprocessing import cpu_count

from qary.qa.torch_models import QuestionAnsweringModel
from qary.constants import DATA_DIR, USE_CUDA, MIDATA_URL, MIDATA_QA_MODEL_DIR, args
from qary.skills.base import BotReply
from qary.skills.base import ContextBot
from qary.etl.netutils import DownloadProgressBar
from qary.etl import wikipedia_api

log = logging.getLogger(__name__)

STOP_WIKI_PROBABILITY = .4


class Skill(ContextBot):
    """ Skill that provides answers to questions given context data containing the answer """

    def __init__(self, context=None, args=args, **kwargs):
        context = {'doc': {'text': ''}}
        super().__init__(context=context, args=args, **kwargs)
        log.debug(f'Initial qa.Skill.context: {self.context}')
        self.transformer_loggers = []
        for name in logging.root.manager.loggerDict:
            if (len(name) >= 12 and name[:12] == 'transformers') or name == 'qary.skills.qa.utils':
                self.transformer_loggers.append(logging.getLogger(name))
                self.transformer_loggers[-1].setLevel(logging.ERROR)

        qa_model = args.qa_model
        url_str = f"{MIDATA_URL}/{MIDATA_QA_MODEL_DIR}/{qa_model}.zip"
        log.debug(f"Attempting to download url: {url_str}")
        model_dir = os.path.join(DATA_DIR, 'qa-models', f"{qa_model}")
        model_type = qa_model.split('-')[0].lower()
        self.wikiscraper = wikipedia_api.WikiScraper()
        if not os.path.isdir(model_dir):
            os.makedirs(model_dir)

        required_files = 'config.json pytorch_model.bin tokenizer_config.json version.json vocab.txt'.split()
        if model_type == 'albert':
            required_files[-1] = 'spiece.model'
        if not all(Path(model_dir, fn).is_file() for fn in required_files):
            zip_local_path = os.path.join(DATA_DIR, 'qa-models', f"{qa_model}.zip")
            with DownloadProgressBar(
                    unit='B', unit_scale=True, miniters=1,
                    desc=url_str.split('/')[-1]
            ) as t:
                urllib.request.urlretrieve(url_str, filename=zip_local_path, reporthook=t.update_to)
            with zipfile.ZipFile(zip_local_path, 'r') as zip_file:
                zip_file.extractall(os.path.join(DATA_DIR, 'qa-models'))
            os.remove(zip_local_path)

        model_args = {
            'process_count': cpu_count() - 2 if cpu_count() > 2 else 1,
            'output_dir': model_dir,
            'cache_dir': model_dir,
            'no_cache': True,
            'use_cached_eval_features': False,
            'overwrite_output_dir': False,
            'silent': True
        }

        self.model = QuestionAnsweringModel(
            model_type, model_dir, args=model_args,
            pretrained=True, use_cuda=USE_CUDA
        )

    def encode_input(self, statement, text):
        """ Converts statement and context strings into json format compatible with BERT transformer

        BERT models use the word "context" to mean a single str read by BERT for QA.
        `qary.skills.base` uses context to manage a dict of many variables
        that help manage conversation

        >>> bot = Skill()
        >>> encoded = bot.encode_input('statement', text='example text')
        >>> encoded[0]['qas'][0]['question']
        'statement'
        >>> encoded[0]['context']
        'example text'
        """
        encoded = [{
            'qas': [{
                'id': str(uuid.uuid1()),
                'question': statement
            }],
            'context': text
        }]
        return encoded

    def decode_output(self, output):
        """
        Extracts reply string from the model's prediction output

        >>> bot = Skill()
        >>> bot.decode_output(
        ...    [{'id': 'unique_id', 'answer': 'response', 'probability': 0.75}])
        (0.75, 'response')
        """
        return output[0]['probability'], output[0]['answer']

    def reply(self, statement, context=None, **kwargs):
        """ Use context document + BERT to answer question in statement

        context is a nested dictionary with two ways to specify the documents for a BERT context:
        {docs: ['doc text 1', '...', ...]}
        or, as only syntactic sugar (internally this is converted to the format above)
        {doc: {text: 'document text ...'}}
        """
        statement = statement or ''
        log.info(f"QABot.reply(statement={statement}, context={context})")
        if isinstance(context, str):
            context = dict(docs=[context], doc=dict(text=context))
        elif isinstance(context, (list, tuple, np.ndarray)):
            context = dict(docs=context, doc=dict(text='\n'.join(context)))
        # this calls self.update_context(context=context) internally:
        elif isinstance(context, dict):
            if not context.get('docs') and context.get('doc'):
                context['docs'] = [context.get('doc').get('text')]

        if (not context or not any(context.get('docs', ['']))):
            gendocs = self.wikiscraper.find_article_texts(
                query=statement,
                max_articles=1, max_depth=1,
                ngrams=3,
                ignore='who what when where why'.split()) or []
            context = dict(docs=gendocs)
        responses = super().reply(
            statement=statement, context=context, **kwargs) or []
        log.info(f"qa_bots.Skill.super() responses (before BERT): {responses}")
        docs = self.context.get('docs') or [self.context['doc']['text']]
        for i, text in enumerate(docs):
            log.info(
                f"text[{i}] from context['doc']['text'] or wikipedia_api: "
                f"{repr(text)[:40]}...{repr(text)[-40:]} ({len(text)} chars)")
            super().update_context(context=dict(doc=dict(text=text)))
            if len(text.strip()) < 2:
                log.info(f'Context document text was too short: "{text}"')
                continue
            encoded_input = self.encode_input(statement, text)
            encoded_output = self.model.predict(encoded_input)
            probability, response_text = self.decode_output(encoded_output)
            if len(response_text) > 0:
                responses.append(
                    BotReply(
                        confidence=probability,
                        text=response_text,
                        skill=self.__module__))
                if probability > STOP_WIKI_PROBABILITY:
                    log.info(f"Short circuiting wiki crawl because p > thresh: {probability} > {STOP_WIKI_PROBABILITY}")
                    break
        return responses
