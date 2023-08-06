""" Search and scrape wikipedia articles from a chosen category

This is how secure access to es works using basic auth

```python
from elasticsearch import Elasticsearch, NotFoundError
ES_HOST = 'es.qary.ai'
ES_PORT = 80
ES_USER = 'kibadmin'
ES_PASS = 'p@ss'
client = Elasticsearch(f"http://{ES_USER}:{ES_PASS}@{ES_HOST}:{ES_PORT}")
client.indices.exists('wikipedia')
```

"""
import os
import requests
from pathlib import Path

from elasticsearch import Elasticsearch, NotFoundError
import wikipediaapi
from slugify import slugify
import numpy as np
import pandas as pd
import yake

from qary import constants
from qary.constants import ES_URL, ES_INDEX, ARTICLES_URL

log = constants.logging.getLogger(__name__)


def connect(es_url=ES_URL):
    client = None
    if es_url:
        try:
            client = Elasticsearch(es_url)
        except ConnectionRefusedError:
            log.error("Failed to connect ElasticSearch client")
    return client


client = connect()


wiki_wiki = wikipediaapi.Wikipedia('en')
kw_extractor = yake.KeywordExtractor()


def create_index(index=ES_INDEX):
    if client and not client.indices.exists(index=index):
        log.info(f"No index {index} found, creating it ...")
        client.indices.create(index=ES_INDEX, ignore=400)
    if client.indices.exists(index=index):
        return index
    log.warning(f"Unable to create index {index} using {client}")


def extract_keywords(text):
    keywords = kw_extractor.extract_keywords(text)
    kw = ','.join([kw[1] for kw in keywords])
    return kw


def load_parsed_articles_from_url(url=ARTICLES_URL, filename='parsed_wiki_articles.pkl'):
    r = requests.get(url)
    open(filename, 'wb').write(r.content)


def get_articles_from_pkl(filedir='parsed_wiki_articles.pkl', index=ES_INDEX):
    unpickled_df = pd.read_pickle(filedir)
    articles = unpickled_df.to_dict('records')
    return articles


def add_parsed_document_to_elasticsearch(sections, index=ES_INDEX):
    pageid = sections[0]['page_id']
    if not client:
        return
    exists = None
    try:
        exists = in_index(article_id=pageid, index=index)
    except NotFoundError as e:
        log.warning(f'It looks like the {index} does not exist (NotFoundError):')
        log.error(e)

    if not exists:
        log.info(f"Loading article with page id {pageid} into ElasticSearch index {index}...")
        for section in sections:
            try:
                client.index(index=index, body=section)
            except Exception as err:
                log.error(f'Failed to add the article with page ID {pageid} to {index}', err)
        return sections
    else:
        log.info(f'Article with page_id {pageid} is already in the index.')


def print_categorymembers(categorymembers, level=0, max_level=1):
    for c in categorymembers.values():
        print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            print_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)


def save_articles(
        path=os.path.join(constants.DATA_DIR, "wikipedia"),
        category='Natural_language_processing'):
    """ Save articles in separate .txt files """
    os.makedirs(path, exist_ok=True)
    wiki_wiki = wikipediaapi.Wikipedia('en')
    cat = wiki_wiki.page(f"Category:{category}")

    for key, value in cat.categorymembers.items():
        page = wiki_wiki.page(key)
        slug = slugify(key)
        try:
            with open(f'{path}/{slug}.txt', 'w') as new_file:
                new_file.write(page.title)
                new_file.write('\n')
                new_file.write(page.fullurl)
                new_file.write('\n')
                new_file.write(page.text)
        except Exception as error:
            log.error(f"Error writing document {page.title}: {error}")


def index_dir(path=Path(constants.DATA_DIR, 'corpora', 'wikipedia')):
    """ NotImplemented... yet"""
    raise NotImplementedError(
        "Walks a directory tree and returns a list of paths but doesn't do anything with them.")
    paths = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.txt' in file:
                paths.append(os.path.join(r, file))

    return paths


class Document:

    def __init__(self, title, text, source):

        self.title = title
        self.text = text
        self.source = source
        self.body = {}
        try:
            self.body = {
                "title": self.title,
                "text": self.text,
                "source": self.source
            }
            log.info(f"Elasticsearch Document JSON created: {self.body}")
        except Exception as error:
            log.warning(f"Document JSON instance error: ", error)

    def insert(self):
        slug = slugify(self.body['title'])
        if client:
            try:
                return client.index(index=slug, body=self.body)
            except Exception as e:
                log.error(f"Could not create a JSON entry for an article {slug}. error: {e}")


def search(text=None, title=None, index=''):
    """ Full text search within an ElasticSearch index (''=all indexes) for the indicated text """
    if not client:
        return {}
    if title:
        body = {"query": {"match": {"title": title}}}
    else:
        body = {"query": {"match": {"text": text}}}
    try:
        results = client.search(index=index, body=body)
    except NotFoundError:
        return {}
    return results


def in_index(article_id=None, title=None, index=ES_INDEX):
    """ Check if the article is already in the ElasticSearch index by looking it up by page_id

    >>> bool(in_index(article_id=123, index=''))
    False
    >>> x = in_index(article_id=31491224, index='')
    >>> (x is True) or (x is None)
    True
    >>> x = in_index(title='Trevor Noah', index='')
    >>> (x is True) or (x is None)
    True
    """
    if not client:
        return
    if title:
        body = {"query": {"match": {"article_title": title}}}
    else:
        body = {"query": {"match": {"page_id": article_id}}}
    try:
        results = client.search(index=index, body=body)
    except NotFoundError:
        return False
    return len(results.get('hits', {}).get('hits', {})) > 0


def deconstruct_wikipedia_article(page=None, pageid=None, title=None):
    page = page or wiki_wiki.page(pageid or title)
    if not in_index(page.pageid):
        sections = deconstruct_article(page=page)
        return sections


def deconstruct_article(page=None, title=None):
    """ This is horribly recursive """
    page = page or wiki_wiki.page(title)
    section_list = []
    section_list = [{'level': 0,
                     'section_title': 'Summary',
                     'text': page.summary}]

    def get_sections(sections, level=0):
        for s in sections:
            section_dict = {'level': level,
                            'section_title': s.title,
                            'text': s.text}
            section_list.append(section_dict)
            get_sections(s.sections, level + 1)

    get_sections(page.sections)
    return section_list


def build_elasticsearch_record(page, section_list):

    # Transform list of dictionaries to dataframe
    df = pd.DataFrame(section_list)

    # Create column "main_section"
    df['main_section'] = np.nan
    df.loc[df['level'] == 0, 'main_section'] = df['section_title']
    df['main_section'].fillna(method='ffill', inplace=True)

    # Create column "subsection"
    df['subsection'] = np.nan
    df.loc[df['text'] == '', 'subsection'] = df['section_title']
    df['subsection'].fillna(method='ffill', inplace=True)

    # Add wikipedia article title, source url and page id
    df1 = df.fillna('')
    df1['article_title'] = page.title
    df1['source_url'] = page.fullurl
    df1['page_id'] = page.pageid

    # Create a list of section tags
    df1['tags'] = df1.apply(lambda row: [row['article_title'],
                                         row['main_section'],
                                         row['subsection'],
                                         row['section_title']],
                            axis=1)
    df1['tags'] = df1['tags'].apply(lambda cell: [s for s in cell if s != ""])
    df1['tags'] = df1['tags'].apply(lambda cell: list(dict.fromkeys(cell)))
    df1['keywords'] = df1.apply(lambda x: extract_keywords(x['text']) if len(x['text']) > 1000 else "", axis=1)

    # Drop rows with NaN values (empty sections)
    df2 = df1.replace('', np.nan, regex=True)
    df2 = df2.drop(['level', 'subsection'], axis=1).dropna()

    # Transform a list of tags to a comma separated string
    df2['tags'] = df2.apply(lambda row: ','.join(row['tags']), axis=1)

    # Add tags as the first line of the text field
    df2['text'] = df2.apply(lambda row: row['tags'] + '\n' + row['text'], axis=1)

    # Add number of section withing the article
    df2['section_number'] = df2.index

    return df2.to_dict(orient='records')


def parse_and_index_wikipedia_article(title='Trevor Noah', index=ES_INDEX):
    page = wiki_wiki.page(title)
    sections = deconstruct_wikipedia_article(page=page) or []
    records = build_elasticsearch_record(page, sections) or []
    return add_parsed_document_to_elasticsearch(sections=records, index=index)
