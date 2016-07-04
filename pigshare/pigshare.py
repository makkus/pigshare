# PYTHON_ARGCOMPLETE_OK

from signal import signal, SIGPIPE, SIG_DFL
import caching
import sys

# Ignore SIG_PIPE and don't throw exceptions on it...
# (http://docs.python.org/library/signal.html)
signal(SIGPIPE, SIG_DFL)


from api import figshare_api
from stats_api import figshare_stats_api as stats_api
from stats_api import STATS_API_ID_ARG_MAP
from api import API_ARG_MAP

import os
import ConfigParser
import logging
from models import *
from api import FIGSHARE_BASE_URL
from input_helpers import create_article

from pyclist.pyclist import pyclist

CONF_FILENAME = 'pigshare.conf'
CONF_HOME = os.path.expanduser('~/.' + CONF_FILENAME)


class PigshareConfig(object):

    def __init__(self):
        self.config = ConfigParser.SafeConfigParser({'token': None, 'url': FIGSHARE_BASE_URL, 'institution': None, 'stats_token': None})

        try:
            user = os.environ['SUDO_USER']
            conf_user = os.path.expanduser('~' + user + "/." + CONF_FILENAME)
            candidates = [conf_user, CONF_HOME]
        except KeyError:
            candidates = [CONF_HOME]

        self.config.read(candidates)

        try:
            self.figshare_url = self.config.get('default', 'url')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError) as e:
            self.figshare_url = FIGSHARE_BASE_URL

        try:
            self.figshare_token = self.config.get('default', 'token')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError) as e:
            self.figshare_token = None

        try:
            self.figshare_stats_token = self.config.get('default', 'stats_token')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError) as e:
            self.figshare_token = None


class Pigshare(object):

    def __init__(self):

        self.config = PigshareConfig()

        self.cli = pyclist(
            'pigshare', 'A commandline wrapper for the Figshare REST API')
        self.cli.root_parser.add_argument(
            '--url', '-u', help='Figshare base url', default=self.config.figshare_url)
        self.cli.root_parser.add_argument(
            '--token', '-t', help='Token to connect to figshare', default=self.config.figshare_token)
        self.cli.root_parser.add_argument(
            '--stats_token', help='Token to connect to figshare stats api', default=self.config.figshare_stats_token)

        self.cli.root_parser.add_argument(
            '--profile', '-p', help='Profile to use (profile must be defined in ~/.pigshare.conf), takes precedence over --url and --token config')

        self.cli.root_parser.add_argument(
            '--institution', '-i', help='The institution, necessary for some of the stats lookups')

        self.cli.root_parser.add_argument(
            '--verbose', '-v', help='Verbose output, for debugging/displaying generated json', action='store_true')
        self.cli.root_parser.add_argument(
            '--output', '-o', help='Filter output format')
        self.cli.root_parser.add_argument(
            '--separator', '-s', default='\n', help='Seperator for output, useful to create a comma-separated list of ids. Default is new-line')

        self.cli.add_command(figshare_api, API_ARG_MAP, {'ArticleCreate': create_article, 'CollectionCreate': CollectionCreate})

        self.cli.add_command(stats_api, STATS_API_ID_ARG_MAP)

        self.cli.parse_arguments()

        self.url = self.cli.namespace.url
        self.token = self.cli.namespace.token
        self.institution = self.cli.namespace.institution
        self.stats_token = self.cli.namespace.stats_token

        if self.cli.namespace.profile:
            self.cli.parameters['url'] = self.config.config.get(
                self.cli.namespace.profile, 'url')
            self.cli.parameters['token'] = self.config.config.get(
                self.cli.namespace.profile, 'token')
            self.cli.parameters['stats_token'] = self.config.config.get(
                self.cli.namespace.profile, 'stats_token')
            self.cli.parameters['institution'] = self.config.config.get(
                self.cli.namespace.profile, 'institution')

        if self.institution:
            self.cli.parameters['institution'] = self.institution

        self.cli.execute()

        self.output = self.cli.namespace.output
        self.separator = self.cli.namespace.separator

        self.cli.print_result(self.output, self.separator)

        # print caching.get_authors()
        caching.close_authors_cache()
        sys.exit(0)


def run():
    Pigshare()
