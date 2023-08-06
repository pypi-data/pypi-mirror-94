from collections import Counter, OrderedDict
try:
    from collections.abc import Mapping
except ImportError:  # python <3.7
    from collections import Mapping
from decimal import Decimal
import datetime
import logging
import os
from pytz import timezone
import requests
import string
import sys

import numpy as np
import pandas as pd

import nltk
import nltk.corpus
import spacy  # noqa
import configargparse
from environment import Environment
import django.conf

from qary import __version__

# TODO: Do Django ACCESS_KEY and SECRET need to be integrated into env ?
env = Environment(spacy_lang=str, loglevel=int, name=str)
# if you need consistent hashes from builtin hash function set env['PYTHONHASHSEED']

HOME_DIR = os.path.expanduser('~')
QARY_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.dirname(QARY_DIR)
BASE_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(QARY_DIR, 'data')
LOG_DIR = os.path.join(DATA_DIR, 'log')
CONSTANTS_DIR = os.path.join(DATA_DIR, 'constants')
HISTORY_PATH = os.path.join(DATA_DIR, 'history.yml')
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(CONSTANTS_DIR, exist_ok=True)

MIDATA_DOMAINNAME = 'tan.sfo2.digitaloceanspaces.com'
MIDATA_URL = f'https://{MIDATA_DOMAINNAME}'
MIDATA_QA_MODEL_DIR = 'midata/public/models/qa'
MIDATA_QA_MODEL_DIR_URL = f'{MIDATA_URL}{MIDATA_QA_MODEL_DIR}'
ARTICLES_URL = f'{MIDATA_URL}/midata/public/corpora/wikipedia/articles_with_keywords.pkl'

USE_CUDA = False
MAX_TURNS = 10000
DEFAULT_SKILL_CONFIDENCE = .667


DEFAULT_CONFIG = {
    'name': 'bot',
    'persist': 'False',  # Yes, yes, 1, Y, y, T, t
    'bots': 'glossary',  # glossary,qa,parul,eliza,search_fuzzy'
    'spacy_lang': 'en_core_web_sm',
    'use_cuda': USE_CUDA,
    'loglevel': 0,  # 0 allows the user to set a value 10-50 (lower more verbose)
    'num_top_replies': 10,
    'self_score': '.5',
    'semantic_score': '.5',
    'debug': True,
    'wiki_title_max_words': 4,
    'score_weights': '{"spell": .25, "sentiment": .25, "semantic": .5}',
    'qa_model': 'albert-large-v2-0.2.0',
}
DEFAULT_CONFIG.update(env.parsed)

LOGLEVELS = [
    logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.FATAL]
# LOG_LEVELS = [         10,           20,              30,            40,            50]
LOGLEVEL_NAMES = 'DEBUG INFO WARNING ERROR FATAL'.split()
LOGLEVEL_ABBREVIATIONS = [s[:4].lower() for s in LOGLEVEL_NAMES]
LOGLEVEL_ABBR_DICT = dict(zip(LOGLEVEL_ABBREVIATIONS, LOGLEVELS))
# this is the LOGLEVEL for the top of this file, once args and .ini file are read, it will change
LOGLEVEL = getattr(env, 'loglevel', DEFAULT_CONFIG.get('loglevel', logging.WARNING))
USE_CUDA = getattr(env, 'use_cuda', DEFAULT_CONFIG.get('use_cuda', USE_CUDA))

logging.basicConfig(
    format='%(asctime)s.%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=LOGLEVEL)
root_logger = logging.getLogger()
log = logging.getLogger(__name__)

# TZ constants
DEFAULT_TZ = timezone('UTC')

MAX_LEN_FILEPATH = 1023  # on OSX `open(fn)` raises OSError('Filename too long') if len(fn)>=1024

ROUNDABLE_NUMERIC_TYPES = (float, int, Decimal, bool)
FLOATABLE_NUMERIC_TYPES = (float, int, Decimal, bool)
BASIC_NUMERIC_TYPES = (float, int)
NUMERIC_TYPES = (float, int, Decimal, complex, str)  # datetime.datetime, datetime.date
NUMBERS_AND_DATETIMES = (float, int, Decimal, complex, str)
SCALAR_TYPES = (float, int, Decimal, bool, complex, str)  # datetime.datetime, datetime.date
# numpy types are derived from these so no need to include numpy.float64, numpy.int64 etc
DICTABLE_TYPES = (Mapping, tuple, list)  # convertable to a dictionary (inherits Mapping or is a list of key/value pairs)
VECTOR_TYPES = (list, tuple)
PUNC = str(string.punctuation)

# synonyms for "count"
COUNT_NAMES = ['count', 'cnt', 'number', 'num', '#', 'frequency', 'probability', 'prob', 'occurences']
# 4 types of

###########
# secrets
SPACES_ACCESS_KEY = os.environ.get('SPACES_ACCESS_KEY')
SPACES_SECRET_KEY = os.environ.get('SPACES_SECRET_KEY')

ES_HOST = os.environ.get('ES_HOST')
ES_PORT = os.environ.get('ES_PORT', 9200)
ES_USER = os.environ.get('ES_USER', os.environ.get('KIBANA_USER', 'kibadmin'))
ES_PASS = os.environ.get('ES_PASS', os.environ.get('KIBANA_PASS', 'YoUrPaSsWoRd'))
ES_INDEX = os.environ.get('ES_INDEX', 'wikipedia')

# secrets
############


def parse_args(args):
    """Parse command line parameters using qary.ini for the default values

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """

    parser = configargparse.ArgParser(
        default_config_files=[
            '~/qary.ini',
            # '~/qary.ini',
            # '~/nlpiabot.ini',
            # '~/nlpia.ini',
            # os.path.join(BASE_DIR, '*.ini'),
            os.path.join(DATA_DIR, '*.ini'),
        ],
        description="Command line bot application. Try `$ bot how do you work?`")
    parser.add('-c', '--config', required=False, is_config_file=True,
               help="Config file path (default: ~/qary.ini)")
    parser.add_argument(
        '-d', '--debug',
        help="Set DEBUG logging level and raise more exceptions immediately.",
        dest="debug",
        default=str(DEFAULT_CONFIG['debug'])[0].lower() in 'fty1p',
        action='store_true')
    parser.add_argument(
        '--version',
        action='version',
        version='qary {ver}'.format(ver=__version__))
    parser.add_argument(
        '--name',
        default=None,  # DEFAULT_CONFIG['name'],
        dest="nickname",
        help="IRC nick or CLI command name for the bot",
        type=str,
        metavar="STR")
    parser.add_argument(
        '-n',
        '--num_top_replies',
        default=None,  # DEFAULT_CONFIG['num_top_replies'],
        dest="num_top_replies",
        help="Limit on the number of top (high score) replies that are randomly selected from.",
        type=int,
        metavar="INT")
    parser.add_argument(
        '-u',
        '--use_cuda',
        help="Use CUDA and GPU to speed up transformer inference.",
        dest='use_cuda',
        default=USE_CUDA,
        action='store_true')
    parser.add_argument(
        '-p',
        '--persist',
        help="DEPRECATED: Don't exit. Retain language model in memory and maintain dialog until user says 'exit' or 'quit'",
        dest='persist',
        default=str(DEFAULT_CONFIG['persist'])[0].lower() in 'fty1p',
        action='store_true')
    parser.add_argument(
        '-b',
        '--bots',
        default=None,  # DEFAULT_CONFIG['bots'],  # None so config.ini can populate defaults
        dest="bots",
        help="Comma-separated list of bot personalities to load. Defaults: pattern,parul,search_fuzzy,time,eliza",
        type=str,
        metavar="STR")
    parser.add_argument(
        '-s',
        '--skills',
        default=None,  # DEFAULT_CONFIG['bots'],  # None so config.ini can populate defaults
        dest="bots",
        help="Comma-separated list of bot personalities to load. Defaults: pattern,parul,search_fuzzy,time,eliza",
        type=str,
        metavar="STR")
    parser.add_argument(
        '-q',
        '--quiet',
        dest="verbosity",
        help="Quiet: set loglevel to ERROR",
        action='store_const',
        const=logging.ERROR)
    parser.add_argument(
        '-qq',
        '--very_quiet',
        dest="verbosity",
        help="Very quiet: set loglevel to FATAL",
        action='store_const',
        const=logging.FATAL)
    parser.add_argument(
        '-v',
        '--verbose',
        dest="verbosity",
        help="Verbose: set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very_verbose',
        dest="verbosity",
        help="Verty verbose: set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    parser.add_argument(
        '-l',
        '--loglevel',
        dest="loglevel",
        help="Raw integer loglevel (10=debug, 20=info, 30=warn, 40=error, 50=fatal)",
        type=int,
        default=0)  # DEFAULT_CONFIG['loglevel'])
    parser.add_argument(
        '--spacy_lang',
        default=None,  # None allows ini to set default
        dest="spacy_lang",
        help="SpaCy language model: en_core_web_sm, en_core_web_md, or en_core_web_lg",
        type=str,
        metavar="STR")
    parser.add_argument(
        '--wiki_title_max_words',
        default=DEFAULT_CONFIG['wiki_title_max_words'],
        dest="wiki_title_max_words",
        help='Maximum n-gram length (in tokens) for wikipedia article title guesses.',
        type=int,
        metavar="INT")
    parser.add_argument(
        '--semantic',
        type=float,
        default=1.0,
        dest='semantic',
        metavar='FLOAT',
        help='set weight of the semantic quality score')
    parser.add_argument(
        '--sentiment',
        type=float,
        default=0.5,
        dest='sentiment',
        metavar='FLOAT',
        help='set weight of the sentiment quality score')
    parser.add_argument(
        '--spell',
        type=float,
        default=0.2,
        dest='spell',
        metavar='FLOAT',
        help='set weight of the spell quality score')
    parser.add_argument(
        'words',
        type=str,
        nargs='*',
        help="Words to pass to bot as an utterance or conversational statement requiring a bot reply or action.")
    parser.add_argument(
        '--qa_model',
        help="Select which model qa_bots will use",
        dest='qa_model',
        default=DEFAULT_CONFIG['qa_model'],
        type=str,
        metavar='STR')
    parsed_args = parser.parse_args(args)
    # print(parsed_args)
    return parsed_args


def setup_logging(loglevel=LOGLEVEL):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    global LOGLEVEL, log, root_logger

    logformat = '%(asctime)s.%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
    logdatefmt = "%Y-%m-%d%H:%M:%S"
    root_logger.setLevel(loglevel)
    log.setLevel(loglevel)
    # FIXME: this doesn't seem to change things, the original format and level set at top of file rules
    logging.basicConfig(level=loglevel, stream=sys.stdout, format=logformat, datefmt=logdatefmt)
    # set the root logger to the same log level
    logging.getLogger().setLevel(loglevel)


def parse_argv(argv=sys.argv):
    """ Parse the command line args and ini file. Business logic to resolve conflicting arg values """
    global BOT, USE_CUDA, log

    new_argv = []
    if len(argv) > 1:
        command_line_path = str(argv[0]).lower().strip()
        if command_line_path.endswith('qary') or command_line_path.endswith('bot'):
            new_argv.extend(list(argv[1:]))
    else:
        log.info(f"It doesn't look like you're running this as a command line application. sys.argv: {argv}")
    args = parse_args(args=new_argv)

    # consolidate the 2 synonymous args, loglevel and verbosity, by using the minimum of the 2
    #   loglevel may be set by the ini file or the command line arg loglevel
    #   verbosity may only be set by the command line args -v/verbose -qq -vv and -q/quiet
    #   The more verbose of the 2 (lower loglevel value) wins

    loglevel = min(args.loglevel or 0, args.verbosity or 0) or logging.WARNING
    setup_logging(loglevel=loglevel)
    log.debug(f'RAW ARGS (including config file): {vars(args)}')
    args.loglevel = loglevel

    # strip quotes in case ini file incorrectly uses single quotes that become part of the str
    args.nickname = str(args.nickname).strip().strip('"').strip("'")
    args.bots = 'glossary,qa' if getattr(args, 'bots', getattr(args, 'skills', None)) is None else args.bots
    args.bots = [m.strip() for m in args.bots.split(',')]
    log.debug(f"Building a BOT with: {args.bots}")

    USE_CUDA = args.use_cuda

    return args


try:
    # This will fail if another application (like gunicorn) imports qary and redirects stdin without
    # running it as a command line app
    print()  # can't log anything until we know what the user's log level is.
    # print(f"sys.argv: {sys.argv}")
    args = parse_argv(argv=sys.argv)
except Exception as e:  # noqa
    log.info(e)
    log.info('Unable to parse command line arguments. Are you trying to import this into gunicorn?')
    # Workaround for the bug when Django app tries to import qary.constants:
    # `usage: gunicorn [-h] [-c CONFIG] ... gunicorn: error: unrecognized arguments
    args = parse_argv(argv=[])


LOGLEVEL = args.loglevel or LOGLEVEL


# handler = logging.handlers.TimedRotatingFileHandler(os.path.join(LOG_DIR, 'qary.constants.log'), when='midnight')
# handler.setLevel(logging.INFO)
# log.addHandler(handler)


LANGS = ['en_core_web_sm', 'en_core_web_md', 'en_core_web_lg']
LANGS_ABBREV = 'en enmd enlg'.split()
LANGS += 'de_core_news_sm de_core_news_md de_trf_bertbasecased_lg'.split()
LANGS_ABBREV += 'de demd delg'.split()

# FOREIGN_LANGS_DF = pd.read_csv(os.path.join(DATA_DIR, 'spacy_languages.csv'))
# for i, row in FOREIGN_LANGS_DF.iterrows():
#     match = re.match(r'(\d)+\b', row['Models'])
#     if match:
#         num_models = int(match.groups()[0])
#         LANGS.extend([row['Code']] * num_models)

# tuple('de de de'.split())  # df=pd.read_html('https://spacy.io/usage/models')[0]
LANGS_ABBREV = dict(zip(LANGS_ABBREV, LANGS))

LANG = getattr(args, 'spacy_lang', None) or DEFAULT_CONFIG.get('spacy_lang') or LANGS[0]
log.info(f'LANG=spacy_lang={LANG}')

try:
    STOPWORDS_DICT = Counter(nltk.corpus.stopwords.words('english'))
except LookupError:
    log.info('Downloading NLTK stopwords and punkt corpora')
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    STOPWORDS_DICT = Counter(nltk.corpus.stopwords.words('english'))
STOPWORDS = set(STOPWORDS_DICT)

QUESTIONWORDS = set('who what when were why which how'.split() + ['how come', 'why does', 'can i', 'can you', 'which way'])
QUESTION_STOPWORDS = QUESTIONWORDS | STOPWORDS

ASCII_LOWER = 'abcdefghijklmnopqrstuvwxyz'
ASCII_UPPER = ASCII_LOWER.upper()


# clibot.py
DEFAULT_BOTS = ['pattern']  # 'search_fuzzy', 'parul', 'eliza', 'glossary', 'qa'

# faq_bots.py
FAQ_DOMAINS = (
    'python-data-science',
)
FAQ_MIN_SIMILARITY = 0.88
FAQ_MAX_NUM_REPLIES = 3

# glossary_bots.py
DEFAULT_GLOSSARY_DOMAINS = ('dsdh', )

TFHUB_USE_MODULE_URL = "https://tfhub.dev/google/universal-sentence-encoder-large/3"

# # templates for medical sentences
# SENTENCE_SPEC_PATH = os.path.join(DATA_DIR, 'medical_sentences.json')
# SENTENCE_SPEC = json.load(open(SENTENCE_SPEC_PATH, 'r'))


# Universal Sentence Encoder's TF Hub module for creating USE Embeddings from
USE = None


def set_django_settings(settings=None):
    DATABASES = {
        'sqlite': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
        'postgres': {
            'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.sqlite3'),
            'NAME': os.environ.get('SQL_DATABASE', os.path.join(BASE_DIR, 'db.sqlite3')),
            'USER': os.environ.get('SQL_USER', 'user'),
            'PASSWORD': os.environ.get('SQL_PASSWORD', 'password'),
            'HOST': os.environ.get('SQL_HOST', 'localhost'),
            'PORT': os.environ.get('SQL_PORT', '5432'),
        }
    }
    DATABASES['default'] = DATABASES['sqlite']
    settings = {'DATABASE_' + k: v for (k, v) in DATABASES['default'].items()}
    settings['TIME_ZONE'] = 'America/Los_Angeles'
    try:
        django.conf.settings.configure(**settings)
    except RuntimeError:  # RuntimeError('Settings already configured.')
        pass
    return django.conf.settings


django_settings = set_django_settings()


#####################################################################################
# pugnlp.constants

tld_iana = pd.read_csv(os.path.join(DATA_DIR, 'constants', 'tlds-from-iana.csv'), encoding='utf8')
tld_iana = OrderedDict(sorted(zip((tld.strip().lstrip('.') for tld in tld_iana.domain),
                                  [(sponsor.strip(), -1) for sponsor in tld_iana.sponsor]),
                              key=lambda x: len(x[0]),
                              reverse=True))
# top 20 in Google searches per day
# sorted by longest first so .com matches before .om (Oman)
tld_popular = OrderedDict(sorted([
    ('com', ('Commercial', 4860000000)),
    ('org', ('Noncommercial', 1950000000)),
    ('edu', ('US accredited postsecondary institutions', 1550000000)),
    ('gov', ('United States Government', 1060000000)),
    ('uk', ('United Kingdom', 473000000)),  # noqa
    ('net', ('Network services', 206000000)),
    ('ca', ('Canada', 165000000)),  # noqa
    ('de', ('Germany', 145000000)),  # noqa
    ('jp', ('Japan', 139000000)),  # noqa
    ('fr', ('France', 96700000)),  # noqa
    ('au', ('Australia', 91000000)),  # noqa
    ('us', ('United States', 68300000)),  # noqa
    ('ru', ('Russian Federation', 67900000)),  # noqa
    ('ch', ('Switzerland', 62100000)),  # noqa
    ('it', ('Italy', 55200000)),  # noqa
    ('nl', ('Netherlands', 45700000)),  # noqa
    ('se', ('Sweden', 39000000)),  # noqa
    ('no', ('Norway', 32300000)),  # noqa
    ('es', ('Spain', 31000000)),  # noqa
    ('mil', ('US Military', 28400000)),
    ], key=lambda x: len(x[0]), reverse=True))

uri_schemes_iana = sorted(pd.read_csv(os.path.join(DATA_DIR, 'constants', 'uri-schemes.xhtml.csv'),
                                      index_col=0).index.values,
                          key=lambda x: len(str(x)), reverse=True)
uri_schemes_popular = ['chrome-extension', 'example', 'content', 'bitcoin',
                       'telnet', 'mailto',
                       'https', 'gtalk',
                       'http', 'smtp', 'feed',
                       'udp', 'ftp', 'ssh', 'git', 'apt', 'svn', 'cvs']

# these may not all be the sames isinstance types, depending on the env
FLOAT_TYPES = tuple([t for t in set(np.typeDict.values()) if t.__name__.startswith('float')] + [float])
FLOAT_DTYPES = tuple(set(np.dtype(typ) for typ in FLOAT_TYPES))
INT_TYPES = tuple([t for t in set(np.typeDict.values()) if t.__name__.startswith('int')] + [int])
INT_DTYPES = tuple(set(np.dtype(typ) for typ in INT_TYPES))
NUMERIC_TYPES = tuple(set(list(FLOAT_TYPES) + list(INT_TYPES)))
NUMERIC_DTYPES = tuple(set(np.dtype(typ) for typ in NUMERIC_TYPES))

DATETIME_TYPES = [t for t in set(np.typeDict.values()) if t.__name__.startswith('datetime')]
DATETIME_TYPES.extend([datetime.datetime, pd.Timestamp])
DATETIME_TYPES = tuple(DATETIME_TYPES)

DATE_TYPES = (datetime.datetime, datetime.date)

# matrices can be column or row vectors if they have a single col/row
VECTOR_TYPES = (list, tuple, np.matrix, np.ndarray)
MAPPING_TYPES = (Mapping, pd.Series, pd.DataFrame)

# These are the valid dates for all 3 datetime types in python (and the underelying integer nanoseconds)
INT_MAX = INT64_MAX = 2 ** 63 - 1
INT_MIN = INT64_MIN = - 2 ** 63
UINT_MAX = UINT64_MAX = - 2 ** 64 - 1

INT32_MAX = 2 ** 31 - 1
INT32_MIN = - 2 ** 31
UINT32_MAX = - 2 ** 32 - 1

INT16_MAX = 2 ** 15 - 1
INT16_MIN = - 2 ** 15
UINT16_MAX = - 2 ** 16 - 1

# Pandas timestamps can handle nanoseconds? but python datetimestamps cannot.
MAX_TIMESTAMP = pd.Timestamp('2262-04-11 23:47:16.854775', tz='utc')
MIN_TIMESTAMP = pd.Timestamp(datetime.datetime(1677, 9, 22, 0, 12, 44), tz='utc')
ZERO_TIMESTAMP = pd.Timestamp('1970-01-01 00:00:00', tz='utc')

# to_pydatetime() rounds to microseconds, ignoring 807 nanoseconds available in other MAX TIMESTAMPs
MIN_DATETIME = MIN_TIMESTAMP.to_pydatetime()
MAX_DATETIME = MAX_TIMESTAMP.to_pydatetime()
MIN_DATETIME64 = MIN_TIMESTAMP.to_datetime64()
MAX_DATETIME64 = MAX_TIMESTAMP.to_datetime64()
INF = np.inf
NAN = np.nan
NAT = pd.NaT


# str constants
MAX_CHR = MAX_CHAR = chr(127)
APOSTROPHE_CHARS = "'`’"
# Monkey patch so import from constants if you want this:
string.unprintable = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0e\x0f' \
    '\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x7f'
ASCII_UNPRINTABLE_CHRS = string.unprintable  # ''.join(chr(i) for i in range(128) if chr(i) not in string.printable)

NULL_VALUES = set(['0', 'None', 'null', "'", ""] + ['0.' + z for z in ['0' * i for i in range(10)]])
# if datetime's are 'repr'ed before being checked for null values sometime 1899-12-30 will come up
NULL_REPR_VALUES = set(['datetime.datetime(1899, 12, 30)'])
# to allow NULL checks to strip off hour/min/sec from string repr when checking for equality
MAX_NULL_REPR_LEN = max(len(s) for s in NULL_REPR_VALUES)

PERCENT_SYMBOLS = ('percent', 'pct', 'pcnt', 'pt', r'%')
FINANCIAL_WHITESPACE = ('Flat', 'flat', ' ', ',', '"', "'", '\t', '\n', '\r', '$')
FINANCIAL_MAPPING = (('k', '000'), ('M', '000000'))

# pugnlp.constants
#####################################################################################


def check_es_url(es_host=ES_HOST, es_port=ES_PORT, es_user=ES_USER, es_pass=ES_PASS, es_index=ES_INDEX, es_url=None):
    es_url = es_url or f'http://{ES_USER}:{ES_PASS}@{ES_HOST}:{ES_PORT}'
    # TODO, use regex to check to make sure es_url contains an es_host too
    if es_url:
        es_index_url = f'{es_url}/{es_index}' if es_index else es_url
        try:
            response = requests.get(es_index_url, timeout=3)
            log.debug(f'ElasticSearch Server Replied: {response.json()}')
        except requests.ConnectTimeout:
            log.info(f"ConnectTimeout while trying to connect to {es_index_url}...")
            return None
        except requests.ConnectionError:
            log.info(f"Unable to connect to {es_index_url}...")
            return None
        except requests.Timeout:
            log.info(f"Timeout while trying to connect to {es_index_url}...")
            return None
        except requests.exceptions.InvalidURL:
            log.info(f"Invalid URL: {es_index_url}...")
            return None
    return es_url


ES_URL = check_es_url()
ES_HOST = None if ES_URL is None else ES_HOST
