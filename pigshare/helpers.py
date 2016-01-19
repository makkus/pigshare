# helpers


def create_models(cls, response):

    json = response.json()

    if len(json) >= 1000:
        print "Max number of results, try to filter."

    models = []

    for item in json:
        model = create_model_object(cls, item)
        models.append(model)

    return models


def print_item(model):

    print model


def print_items(models):

    for m in models:
        print m


def create_model(cls, response):

    json = response.json()

    model = create_model_object(cls, json)
    return model


def create_model_object(cls, properties):

    # TODO, maybe do some validation, error handling
    model = cls(properties)
    return model


def add_ordering(args, req_params={}):
    '''Adds parameters for ordering of results.'''

    # TODO
    pass


def add_filters(args, req_params={}):
    '''Adds the default filtering arguments (institution, group, published_since, modified_since).'''

    if args.institution:
        req_params['institution'] = args.institution
    if args.group:
        req_params['group'] = args.group
    if args.published_since:
        req_params['published_since'] = args.published_since
    if args.modified_since:
        req_params['modified_since'] = args.modified_since

    return req_params


def utf8lize(obj):
    if isinstance(obj, dict):
        temp = {}
        for k, v in obj.iteritems():
            temp[k] = to_utf8(v)
        return temp

    if isinstance(obj, list):
        temp = []
        for x in obj:
            temp.append(to_utf8(x))
        return temp

    if isinstance(obj, unicode):
        return obj.encode('utf-8')

    return obj


def to_utf8(obj):
    if isinstance(obj, unicode):
        return obj.encode('utf-8')
    return obj


def querystr(**kwargs):
    return '?' + urlencode(kwargs)
