from models import *
from restkit import Resource, request
import inspect
import hashlib
import os
import caching
from input_helpers import create_article, create_collection, edit_article, edit_collection
try:
    import simplejson as json
except ImportError:
    import json  # py2.6 only


FIGSHARE_BASE_URL = 'https://api.figshare.com/v2'
DEFAULT_LIMIT = 1000

API_ARG_MAP = {'read_my_article': 'id', 'read_my_collection': 'id', 'add_article': 'article_ids', 'publish_article': 'id', 'read_article': 'id', 'read_collection': 'id', 'read_collection_articles': 'id',
                                            'read_my_collection_articles': 'id', 'remove_article': 'article_id', 'search_articles': 'search_term', 'search_collections': 'search_term', 'upload_new_file': 'file', 'delete_article': 'article_id'}

# Helper methods ========================================


def get_headers(token=None):

    headers = {}
    headers['Content-Type'] = 'application/json'

    if token:
        headers['Authorization'] = 'token ' + token

    return headers


def get_request_params(params={}, limit=DEFAULT_LIMIT):

    params['limit'] = limit
    return params


def create_fileupload_dict(fname):
    '''
    Creates the dict necessary for a file upload ( https://github.com/figshare/user_documentation/blob/master/APIv2/articles.md#initiate-new-file-upload-within-the-article )
    '''

    result = {}
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    result['md5'] = hash.hexdigest()
    result['name'] = os.path.basename(fname)
    result['size'] = os.path.getsize(fname)

    return result


def multiply_call(function_to_call, list_of_ids):
    '''
    If a method is called with multiple ids, it can use this method to create a list of results, using all ids.
    '''

    result = []
    for id in list_of_ids:

        r = function_to_call(id)
        result.append(r)

    return result


API_MARKER = 'call'


def is_api_method(field):

    return inspect.ismethod(field) and field.__name__.startswith(API_MARKER)


# API-Wrapper classes ===================================
class figshare_api(Resource):

    def __init__(self, url=FIGSHARE_BASE_URL, token=None, verbose=False, **kwargs):

        self.url = url
        self.token = token
        self.verbose = verbose
        super(figshare_api, self).__init__(self.url)

    def call_create_json(self, model):
        '''
        Creates a json string by interactively asking the user questions about field values.

        :type model: str
        :param model: the model type to create json for (one of: article, collection)
        :return: the initiated model
        :rtype: Model
        '''

        if model == 'article':
            result = create_article(api=self)

        elif model == 'collection':
            result = create_collection(api=self)
        else:
            raise Exception("Model type '{}' not supported".format(model))

        print
        print "Result json for {}:".format(model)
        print
        return result

    def call_list_articles(self):
        '''Returns a list of all articles.

        :return: A list of articles matching the search term.
        :rtype: list
        '''

        response = self.get('/articles', params_dict=get_request_params())

        articles_json = json.loads(response.body_string())
        result = []
        for a in articles_json:
            art = ArticleShort(**a)
            result.append(art)
        return result

    def call_list_institution_articles(self, inst_id):
        '''Returns a list of all articles.

        :type inst_id: int
        :param inst_id: internal figshare id for institution
        :return: A list of articles matching the search term.
        :rtype: list
        '''

        data = get_request_params()
        data['institution'] = inst_id

        payload = json.dumps(data)

        response = self.post('/articles/search', payload=payload)

        articles_json = json.loads(response.body_string())
        result = []
        for a in articles_json:
            art = ArticleShort(**a)
            result.append(art)
        return result


    def call_search_articles(self, search_term):
        '''
        Searches for an article, returns a list of all matches.

        :type search_term: str
        :param search_term: the term to search for
        :return: A list of articles matching the search term.
        :rtype: list
        '''

        data = get_request_params()
        data['search_for'] = search_term

        payload = json.dumps(data)

        response = self.post('/articles/search', payload=payload)

        articles_json = json.loads(response.body_string())
        result = []
        for a in articles_json:
            art = ArticleShort(**a)
            result.append(art)
        return result

    def call_read_article(self, id):
        '''
        Read an articles.

        :type id: int
        :param id: the article id
        :return: the article details
        :rtype: ArticleL2
        '''

        response = self.get('/articles/{}'.format(id),
                            headers=get_headers(token=self.token))

        article_dict = json.loads(response.body_string())
        # print article_dict
        article = ArticleL2(**article_dict)

        # cache authors
        for au in article.authors:
            caching.add_author(au.id, au.full_name)

        return article

    def call_list_my_articles(self):
        '''
        Returns a list of of your own articles.

        :return: A list of articles.
        :rtype: Articles
        '''

        response = self.get('/account/articles', headers=get_headers(
            token=self.token), params_dict=get_request_params())

        articles_json = json.loads(response.body_string())

        result = []
        for a in articles_json:
            art = ArticleShort(**a)
            result.append(art)
        return result

    def call_search_my_articles(self, search_term):
        '''
        Searches within your own articles.

        :type search_term: str
        :param search_term: the term to search for
        :return: A list of articles matching the search term.
        :rtype: Articles
        '''

        data = get_request_params()
        data['search_for'] = search_term

        # payload = json.dumps(data)
        payload = data

        payload = json.dumps(data)

        response = self.post('/account/articles/search',
                             payload=payload, headers=get_headers(token=self.token))

        articles_json = json.loads(response.body_string())
        result = []
        for a in articles_json:
            art = ArticleShort(**a)
            result.append(art)
        return result

    def call_create_article(self, article=None):
        '''
        Upload a new article.

        :type article: ArticleCreate
        :param article: the article to create

        :return: whether the creation process was successful
        :rtype: bool
        '''

        if not article:
            article = create_article(api=self)

        payload = article.to_json()

        if self.verbose:
            print
            print "--------------------"
            print "Generated json:"
            print
            print payload
            print "--------------------"
            print

        response = self.post(path='/account/articles',
                             payload=payload, headers=get_headers(token=self.token))

        loc = ArticleLocation(**json.loads(response.body_string()))
        return loc

    def call_update_article(self, id, article):
        '''
        Update an article.

        :type id: int
        :param id: the id of the article to udpate
        :type article:  str
        :param article: the article details to update

        :return: the link to the article
        :rtype: str
        '''

        if not article:
            article_dict = edit_article(id, api=self)

        else:
            article_dict = json.loads(article)

        payload = json.dumps(article_dict)

        if self.verbose:
            print
            print "--------------------"
            print "Generated json:"
            print
            print payload
            print "--------------------"
            print

        try:
            response = self.put('/account/articles/{}'.format(id),
                                headers=get_headers(token=self.token), payload=payload)
        except Exception as e:
            print e
            return False

        return self.call_read_my_article(id)

    def call_upload_new_file(self, id, file):
        '''
        Upload a file and associate it with an article.

        :type id: int
        :param id: the id of the article
        :type file: str
        :param file: the file to upload
        :return: the upload location
        :rtype: ArticleLocation
        '''
        payload = json.dumps(create_fileupload_dict(file))
        response = self.post('/account/articles/{}/files'.format(id),
                             headers=get_headers(token=self.token), payload=payload)
        loc = ArticleLocation(**json.loads(response.body_string()))

        response = request(loc.location, headers=get_headers(token=self.token))
        article_file = ArticleFile(**json.loads(response.body_string()))

        # upload_url = '{0}/{1}'.format(article_file.upload_url,
                                      # article_file.upload_token)
        upload_url = article_file.upload_url
        response = request(upload_url)

        article_file_upload_status = ArticleFileUploadStatus(
            **json.loads(response.body_string()))

        with open(file, 'rb') as file_input:
            for part in article_file_upload_status.parts:
                size = part['endOffset'] - part['startOffset'] + 1
                response = request(
                    '{0}/{1}'.format(upload_url, part.partNo), method='PUT', body=file_input.read(size))

        response = request(loc.location, method='POST',
                           headers=get_headers(token=self.token))
        return loc

    def call_read_my_article(self, id):
        '''
        Read one of your articles.

        :type id: int
        :param id: the article id
        :return: the article details
        :rtype: ArticleL2
        '''

        response = self.get('/account/articles/{}'.format(id),
                            headers=get_headers(token=self.token))

        article_dict = json.loads(response.body_string())
        # print article_dict
        article = ArticleL2(**article_dict)

        # cache authors
        for au in article.authors:
            caching.add_author(au.id, au.full_name)
        return article

    def call_list_my_article_files(self, id):
        '''
        List all files associated with one of your articles.

        :type id: int
        :param id: the article id
        :return: a list of files
        :rtype: FileShort
        '''

        response = self.get('/account/articles/{}/files'.format(id),
                            headers=get_headers(token=self.token))

        file_json = json.loads(response.body_string())

        result = []
        for f in file_json:
            fi = FileShort(**f)
            result.append(fi)
        return result

    def call_publish_article(self, id):
        '''
        Publish an article.

        :type id: int
        :param id: the article id
        :return: the link to the article
        :rtype: str
        '''

        response = self.post(
            '/account/articles/{}/publish'.format(id), headers=get_headers(token=self.token))

        loc = ArticleLocation(**json.loads(response.body_string()))
        return loc

    def call_publish_collection(self, id):
        '''
        Publish a collection.

        :type id: int
        :param id: the collection id
        :return: the link to the collection
        :rtype: str
        '''

        response = self.post(
            '/account/collections/{}/publish'.format(id), headers=get_headers(token=self.token))

        loc = ArticleLocation(**json.loads(response.body_string()))
        return loc

    def call_list_collections(self):
        '''
        Lists all publicly available collections.

        :return: all collections
        :rtype: Collections
        '''

        response = self.get('/collections', params_dict=get_request_params())

        collections_json = json.loads(response.body_string())

        result = []
        for c in collections_json:
            col = CollectionShort(**c)
            result.append(col)
        return result

    def call_search_collections(self, search_term):
        '''
        Searches for a collection, returns a list of all matches.

        :type search_term: str
        :param search_term: the term to search for
        :return: A list of collections matching the search term.
        :rtype: Collections
        '''

        data = get_request_params()
        data['search_for'] = search_term

        payload = json.dumps(data)

        response = self.post('/collections/search', payload=payload)

        collections_json = json.loads(response.body_string())
        result = []
        for c in collections_json:
            col = CollectionShort(**c)
            result.append(col)
        return result

    def call_read_collection(self, id):
        '''
        Reads the collection with the specified id.

        :type id: int
        :param id: the collection id
        :return: the collection details
        :rtype: CollectionL1
        '''

        response = self.get('/collections/{}'.format(id))

        col_dict = json.loads(response.body_string())
        col = CollectionL1(**col_dict)

        # author caching
        for au in col.authors:
            caching.add_author(au.id, au.full_name)

        return col

    def call_read_collection_articles(self, id):
        '''
        Lists all articles of a collection.

        :type id: int
        :param id: the collection id
        :return: a list of articles
        :rtype: list
        '''

        response = self.get('/collections/{}/articles'.format(id),
                            params_dict=get_request_params())

        articles_json = json.loads(response.body_string())
        result = []

        for a in articles_json:
            art = ArticleShort(**a)
            result.append(art)
        return result

    def call_list_my_collections(self):
        '''
        Lists all publicly available collections.

        :return: all collections
        :rtype: Collections
        '''

        response = self.get('/account/collections', params_dict=get_request_params(),
                            headers=get_headers(token=self.token))

        collections_json = json.loads(response.body_string())

        result = []
        for c in collections_json:
            col = CollectionShort(**c)
            result.append(col)
        return result

    def call_read_my_collection(self, id):
        '''
        Reads the collection with the specified id.

        :type id: int
        :param id: the collection id
        :return: the collection details
        :rtype: CollectionL1
        '''

        response = self.get('/account/collections/{}'.format(id),
                            headers=get_headers(token=self.token))

        col_dict = json.loads(response.body_string())

        col = CollectionL1(**col_dict)
        print col

        # author caching
        for au in col.authors:
            caching.add_author(au.id, au.full_name)

        return col

    def call_read_my_collection_articles(self, id):
        '''
        Lists all articles of a collection.

        :type id: int
        :param id: the collection id
        :return: a list of articles
        :rtype: Articles
        '''

        response = self.get('/account/collections/{}/articles'.format(id),
                            headers=get_headers(token=self.token), params_dict=get_request_params())

        articles_json = json.loads(response.body_string())

        result = []
        for a in articles_json:
            art = ArticleShort(**a)
            result.append(art)
        return result

    def call_create_collection(self, collection=None):
        '''
        Create a new collection using the provided article_ids

        :type collection: CollectionCreate
        :param collection: the collection to create

        :return: the link to the new collection
        :rtype: str
        '''

        if not collection:
            collection = create_collection(api=self)

        payload = collection.to_json()

        if self.verbose:
            print
            print "--------------------"
            print "Generated json:"
            print
            print payload
            print "--------------------"
            print

        response = self.post(
            '/account/collections', headers=get_headers(token=self.token), payload=payload)

        loc = ArticleLocation(**json.loads(response.body_string()))
        return loc

    def call_update_collection(self, id, collection):
        '''
        Update a collection.

        :type id: int
        :param id: the id of the collection to update
        :type collection: str
        :param collection: the collection to create

        :return: the link to the new collection
        :rtype: str
        '''

        if not collection:
            collection_dict = edit_collection(id, api=self)
        else:
            collection_dict = json.loads(collection)

        payload = json.dumps(collection_dict)

        if self.verbose:
            print
            print "--------------------"
            print "Generated json:"
            print
            print payload
            print "--------------------"
            print

        try:
            response = self.put('/account/collections/{}'.format(id),
                                headers=get_headers(token=self.token), payload=payload)
        except Exception as e:
            print e
            return False

        # print "XXX"+str(response.body_string())

        return self.call_read_my_collection(id)

    def call_add_article(self, id, article_ids):
        '''
        Adds one or more articles to a collection.

        :type id: int
        :param id: the id of the collection
        :type article_ids: list
        :param article_ids: one or more article ids

        :return: whether the operation succeeded
        :rtype: bool
        '''

        if isinstance(article_ids, (int, long)):
            article_ids = [article_ids]

        # convert to ints
        article_ids = [int(x) for x in article_ids]
        if len(article_ids) > 10:
            raise Exception("No more than 10 articles allowed.")

        payload = {}
        payload['articles'] = article_ids
        payload = json.dumps(payload)
        try:
            response = self.post('/account/collections/{}/articles'.format(id),
                                 headers=get_headers(token=self.token), payload=payload)
        except Exception as e:
            print e
            return {"success": False}

        return {"success": True}

    def call_replace_articles(self, collection_id, article_ids):
        '''
        Replace all articles of a collection.

        :type collection_id: int
        :param collection_id: the id of the collection
        :type article_ids: list
        :param article_ids: a list of one or more article ids

        :return: whether the operation succeeded
        :rtype: bool
        '''

        if len(article_ids) > 10:
            raise Exception("No more than 10 articles allowed.")

        payload = {}
        payload['articles'] = article_ids
        payload = json.dumps(payload)

        try:
            response = self.put('/account/collections/{}/articles'.format(
                collection_id), headers=get_headers(token=self.token), payload=payload)
        except Exception as e:
            print e
            return {"success": False}

        return {"success": True}

    def call_delete_article(self, article_id):
        '''
        Deletes an article (that is not published yet).

        :type article_id: int
        :param article_id: the id of the article to delete
        :return: whether the operation succeeded
        :rtype: bool
        '''

        try:
            response = self.delete('/account/articles/{}'.format(
                article_id), headers=get_headers(token=self.token))
        except Exception as e:
            print e
            return {"success": False}

        return {"success": True}



    def call_remove_article(self, collection_id, article_id):
        '''
        Removes one or more articles from a collection.

        :type collection_id: int
        :param collection_id: the id of the collection
        :type article_id: int
        :param article_id: the article to remove

        :return: whether the operation succeeded
        :rtype: bool
        '''

        try:
            response = self.delete('/account/collections/{}/articles/{}'.format(
                collection_id, article_id), headers=get_headers(token=self.token))
        except Exception as e:
            print e
            return {"success": False}

        return {"success": True}

    def call_list_categories(self, filter=None):
        '''
        Lists all categories.

        If a filter is provided, it'll filter the results using a simple, case-insensitive string match.
        If the filter contains at least one uppercase letter, the match is case-sensitive.

        :type filter: str
        :param filter: a string to filter the category names
        :return: a list of all categories
        :rtype: list
        '''

        response = self.get('/categories')

        categories_json = json.loads(response.body_string())

        result = []
        for c in categories_json:
            if filter:
                if filter.islower():
                    if filter not in c['title'].lower():
                        continue
                else:
                    if filter not in c['title']:
                        continue

            col = Category(**c)
            result.append(col)

        return result

    def call_list_licenses(self, filter=None):
        '''
        Lists all licenses.

        If a filter is provided, it'll filter the results using a simple, case-insensitive string match.
        If the filter contains at least one uppercase letter, the match is case-sensitive.

        :type filter: str
        :param filter: a string to filter the license names
        :return: a list of all licenses
        :rtype: list
        '''

        response = self.get('/licenses')

        licenses_json = json.loads(response.body_string())

        result = []
        for c in sorted(licenses_json, key=lambda lic: lic['value']):
            if filter:
                if filter.islower():
                    if filter not in c['title'].lower():
                        continue
                else:
                    if filter not in c['title']:
                        continue

            lic = License(**c)
            result.append(lic)

        return result
