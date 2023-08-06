import re
from functools import lru_cache

from nltk import download, word_tokenize
from unicodedata import normalize

download('punkt')


def tokenize(text, language='english'):
    tokens = word_tokenize(text, language=language)
    return tokens


@lru_cache(maxsize=1000)
def remove_token_accents(token):
    normalized = normalize("NFKD", token)
    no_acents = normalized.encode('ASCII', 'ignore')
    return no_acents.decode()


@lru_cache(maxsize=1000)
def mask_token_numbers(token, mask='#'):
    masked = re.sub(r'[0-9]', mask, token)
    return masked
