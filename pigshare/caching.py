import shelve
import os

PIGSHARE_DIR = os.path.expanduser('~/.pigshare')
try:
    os.mkdir(PIGSHARE_DIR)
except OSError:
    pass


def get_authors_cache():

    s = shelve.open('{}/cache.db'.format(PIGSHARE_DIR), writeback=True)
    authors = s.get('authors', None)
    if not authors:
        s['authors'] = {}

    return s

s = None


def get_shelve():

    global s
    if not s:
        s = get_authors_cache()

    return s


def get_authors():

    return get_shelve()['authors']


def add_author(id, name):

    get_authors()[id] = name


def close_authors_cache():

    get_shelve().close()
