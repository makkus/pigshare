from models import *
from pyclist.model_helpers import ask_details_for_type, MODEL_MAP, parse_for_help, edit_details_for_type
import caching
import booby

CATEGORIES_CACHE = {}


def create_custom_fields():

    result = {}

    print "Enter custom field key/value pairs. Once finished, press enter when asked for a key."
    print

    while True:
        key = raw_input(" - custom field key (String): ")

        if parse_for_help(key, custom_fields_help):
            continue

        if not key:
            break

        value = raw_input(
            " - custom field value for key '{}' (String)': ".format(key))
        while not value:
            print "Value can't be empty."
            value = raw_input(
                " - custom field value for key '{}' (String)': ".format(key))

        result[key] = value

    return result


def create_author(id_or_name=None):
    '''
    Create an AutorCreate object using an id or name.

    If no id/name is provided, ask user on the commandline.
    '''

    if not id_or_name:
        id_or_name = raw_input(" - author id or name (Integer or String): ")

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


def defined_type_help(*args):

    print "Article type, one of:"
    print
    for k, v in FIGSHARE_DEFINED_TYPES_DICT.iteritems():
        print v

    print


def author_help(*args):

    print "If possible, use the authors id instead of name, that way all articles belonging to the same author are guaranteed to end up associated with the same entity in Figshare."
    print
    print "Following is a list of cached names and associated ids. This list is not complete and just used as a workaround because the Figshare API does not allow querying authors directly."
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


def create_categories_help_func(api):

    def categories_help(*args):

        global CATEGORIES_CACHE
        if args:
            filter = args[0]
        else:
            filter = None

        if not CATEGORIES_CACHE:
            CATEGORIES_CACHE = api.call_list_categories()

        for c in CATEGORIES_CACHE:
            if filter:
                if filter.islower():
                    if filter not in c['title'].lower():
                        continue
                else:
                    if filter not in c['title']:
                        continue

            print "{}. {}".format(c['id'], c['title'])

    return categories_help


def create_licenses_help_func(api):

    def licenses_help(*args):

        if args:
            filter = args[0]
        else:
            filter = None

        licenses = api.call_list_licenses()

        for c in licenses:
            if filter:
                if filter.islower():
                    if filter not in c['title'].lower():
                        continue
                else:
                    if filter not in c['title']:
                        continue

            print "{}. {} ({})".format(c.value, c.name, c.url)

    return licenses_help


def create_articles_help_func(api):

    def articles_help(*args):

        if args:
            filter = args[0]
            articles = api.call_search_articles(filter)
        else:
            articles = api.call_list_articles()

        for a in articles:
            print u"{} - {}".format(a.id, a.title)

    return articles_help


def custom_fields_help():

    print "Custom metadata fields."


def create_article_help_map(api):

    help_map = {}
    help_map['title'] = title_help
    help_map['categories'] = create_categories_help_func(api)
    help_map['authors'] = author_help
    help_map['defined_type'] = defined_type_help
    help_map['license'] = create_licenses_help_func(api)
    help_map['custom_fields'] = custom_fields_help

    return help_map


def create_collection_help_map(api=None):

    help_map = {}
    help_map['title'] = title_help
    help_map['categories'] = create_categories_help_func(api)
    help_map['authors'] = author_help
    help_map['articles'] = create_articles_help_func(api)

    return help_map


def create_collection(details=None, api=None):

    if not details:
        help_map = create_collection_help_map(api=api)
        collection = ask_details_for_type(CollectionCreate, False, help_map)
    elif isinstance(details, dict):
        collection = CollectionCreate(**details)
    elif isinstance(details, basestring):
        collection = CollectionCreate(**(json.loads(details)))
    else:
        raise Exception("Can't convert to CollectionCreate object.")

    return collection


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


def edit_collection(id, api=None):

    # load current collection
    old = api.call_read_my_collection(id)
    help_map = create_collection_help_map(api)

    return edit_details_for_type(CollectionCreate, old, help_map)


def edit_article(id, api=None):

    # load current article
    old = api.call_read_my_article(id)
    help_map = create_article_help_map(api)

    return edit_details_for_type(ArticleCreate, old, help_map)


MODEL_MAP[AuthorCreate] = create_author
MODEL_MAP[booby.fields.Field] = create_custom_fields
