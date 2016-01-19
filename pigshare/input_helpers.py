from models import *
from pyclist.model_helpers import ask_details_for_type, MODEL_MAP, parse_for_help
import caching

CATEGORIES_CACHE = {}


def create_author(id_or_name=None):
    '''
    Create an AutorCreate object using an id or name.

    If no id/name is provided, ask user on the commandline.
    '''

    if not id_or_name:
        id_or_name = raw_input("Author id or name: ")

        if parse_for_help(id_or_name, author_help):
            return create_author()

    if not id_or_name:
        # user is finished
        return None

    author = AuthorCreate()

    try:
        author.id = int(id_or_name)
    except:
        author.name = id_or_name

    return author


def title_help(*args):

    print "The title for the article."


def author_help(*args):

    print
    print "This is a list of cached names and associated ids. This list is not complete and just used as a workaround because the Figshare API does not allow querying authors directly."
    print

    for id, name in caching.get_authors().iteritems():
        if args:
            filter = args[0]
            if filter.islower():
                if filter not in name.lower():
                    continue
            else:
                if filter not in name:
                    continue

        print "{} - {}".format(id, name)

    print


def create_article_help_map(api):

    help_map = {}
    help_map['title'] = title_help

    def categories_help(*args):

        global CATEGORIES_CACHE
        if args:
            filter = args[0]
        else:
            filter = None

        if not CATEGORIES_CACHE:
            CATEGORIES_CACHE = api.call_list_categories()

        print
        for c in CATEGORIES_CACHE:
            if filter:
                if filter.islower():
                    if filter not in c['title'].lower():
                        continue
                else:
                    if filter not in c['title']:
                        continue

            print "{}. {}".format(c['id'], c['title'])

        print

    help_map['categories'] = categories_help

    help_map['authors'] = author_help

    return help_map


def create_article(details=None, api=None):

    if not details:
        help_map = create_article_help_map(api)
        article = ask_details_for_type(ArticleCreate, False, help_map)
    elif isinstance(details, dict):
        article = ArticleCreate(**details)
    elif isinstance(details, basestring):
        article = ArticleCreate(**(json.loads(details)))
    else:
        raise Exception("Can't convert to ArticleCreate object.")

    return article


MODEL_MAP[AuthorCreate] = create_author
