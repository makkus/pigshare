from restkit import Resource, request
from api import FIGSHARE_BASE_URL, get_headers
try:
    import simplejson as json
except ImportError:
    import json  # py2.6 only

STATS_DEFAULT_URL="https://stats.figshare.com/"

STATS_TYPES = ["views", "downloads", "shares"]
ITEM_TYPES = ["article", "author", "collection"]

STATS_API_ID_ARG_MAP = {}

def get_headers(token=None):

    headers = {}
    headers['Content-Type'] = 'application/json'

    if token:
        headers['Authorization'] = 'Basic ' + token

        return headers

def get_request_params(params={}, start_date=None, end_date=None, sub_item=None, sub_item_id=None):

    if start_date:
        params["start_date"] = start_date

    if end_date:
        params["end_date"] = end_date

    if sub_item:
        params["sub_item"] = sub_item

    if sub_item_id:
        params["sub_item_id"] = sub_item_id

    return params



def add_totals_method(cls, stats_type, item_type):

    def totals_method(self, id):

        if self.institution:
            response = self.get('/{0}/total/{1}/{2}/{3}'.format(self.institution, stats_type, item_type, id), params_dict={}, headers=get_headers(token=self.token))
        else:
            response = self.get('/total/{0}/{1}/{2}'.format(stats_type, item_type, id), params_dict={}, headers=get_headers(token=self.token))

        totals_json = json.loads("{{\"{0}\":{1}}}".format(id, response.body_string()))

        return totals_json

    totals_method.__doc__ = '''
    Shows {0} stats for {1}.

    :type id: int
    :param id: the id of the {1}
    :return: json-formatted number of {0}
    :rtype: str
    '''.format(stats_type, item_type)

    totals_method.__name__ = 'call_get_total_{0}_{1}'.format(item_type, stats_type)
    setattr(cls, totals_method.__name__, totals_method)
    STATS_API_ID_ARG_MAP[totals_method.__name__[5:]] = 'id'


def add_timeline_method(cls, stats_type, item_type):

    def timeline_method(self, id, granularity="total", start_date=None, end_date=None, sub_item=None, sub_item_id=None):

        if not granularity:
            granularity = "total"

        if self.institution:
            response = self.get('/{0}/timeline/{1}/{2}/{3}/{4}'.format(self.institution, granularity, stats_type, item_type, id), headers=get_headers(token=self.token), params_dict=get_request_params(start_date=start_date, end_date=end_date, sub_item=sub_item, sub_item_id=sub_item_id))
        else:
            response = self.get('/timeline/{0}/{1}/{2}/{3}'.format(granularity, stats_type, item_type, id), headers=get_headers(token=self.token), params_dict=get_request_params(start_date=start_date, end_date=end_date, sub_item=sub_item, sub_item_id=sub_item_id))

        timeline_json = json.loads("{{\"{0}\":{1}}}".format(id, response.body_string()))
        return timeline_json

    timeline_method.__doc__ = '''
    Shows {0} timeline stats for {1}.

    :type id: int
    :param id: the id of the {1}
    :type granularity: str
    :param granularity: One of 'year', 'month', 'day', or 'total' (default)
    :type start_date: str
    :param start_date: Start date (format: yyyy-mm-dd)
    :type end_date: str
    :param end_date: End date (format: yyyy-mm-dd)
    :type sub_item: str
    :param sub_item: Can be one of 'category' and 'item_type'. Acts as a filter on the result.
    :type sub_item_id: int
    :param sub_item_id: Required if sub_item is also specified.
    :return: json-formatted timeline of {0}
    :rtype: str
    '''.format(stats_type, item_type)

    timeline_method.__name__ = 'call_get_timeline_{0}_{1}'.format(item_type, stats_type)
    setattr(cls, timeline_method.__name__, timeline_method)
    STATS_API_ID_ARG_MAP[timeline_method.__name__[5:]] = 'id'

def add_breakdown_method(cls, stats_type, item_type):

    def breakdown_method(self, id, granularity="total", start_date=None, end_date=None, sub_item=None, sub_item_id=None):

        params_dict=get_request_params(start_date=start_date, end_date=end_date, sub_item=sub_item_id, sub_item_id=sub_item_id)

        if not granularity:
            granularity = "total"

        if self.institution:
            response = self.get('/{0}/breakdown/{1}/{2}/{3}/{4}'.format(self.institution, granularity, stats_type, item_type, id), headers=get_headers(token=self.token), params_dict=params_dict)
        else:
            response = self.get('/breakdown/{0}/{1}/{2}/{3}'.format(granularity, stats_type, item_type, id), headers=get_headers(token=self.token), params_dict=params_dict)

        breakdown_json = json.loads("{{\"{0}\":{1}}}".format(id, response.body_string()))
        return breakdown_json


    breakdown_method.__doc__ = '''
    Shows {0} breakdown stats for {1}.

    :type id: int
    :param id: the id of the {1}
    :type granularity: str
    :param granularity: One of 'year', 'month', 'day', or 'total' (default)
    :type start_date: str
    :param start_date: Start date (format: yyyy-mm-dd)
    :type end_date: str
    :param end_date: End date (format: yyyy-mm-dd)
    :type sub_item: str
    :param sub_item: Can be one of 'category' and 'item_type'. Acts as a filter on the result.
    :type sub_item_id: int
    :param sub_item_id: Required if sub_item is also specified.
    :return: json-formatted breakdown of {0}
    :rtype: str
    '''.format(stats_type, item_type)

    breakdown_method.__name__ = 'call_get_breakdown_{0}_{1}'.format(item_type, stats_type)
    setattr(cls, breakdown_method.__name__, breakdown_method)
    STATS_API_ID_ARG_MAP[breakdown_method.__name__[5:]] = 'id'

class figshare_stats_api(Resource):

    def __init__(self, stats_url=STATS_DEFAULT_URL, institution=None, stats_token=None, verbose=False, **kwargs):

        self.url = stats_url
        self.token = stats_token
        self.institution = institution
        self.verbose = verbose
        super(figshare_stats_api, self).__init__(self.url)


for s in STATS_TYPES:
    for t in ITEM_TYPES:
        add_totals_method(figshare_stats_api, s, t)
        add_timeline_method(figshare_stats_api, s, t)
        add_breakdown_method(figshare_stats_api, s, t)
