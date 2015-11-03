import inspect
from api import figshare_api, is_api_method
import argparse
import os
import ConfigParser
import sys
import logging
import models
from models import *
from parinx import parser
from api import API_MARKER, FIGSHARE_BASE_URL
from pprint import pprint, pformat
from booby import Model

from pyclist.pyclist import pyclist

CONF_FILENAME = 'pigshare.conf'
CONF_HOME = os.path.expanduser('~/.'+CONF_FILENAME)

class PigshareConfig(object):

    def __init__(self):
        self.config = ConfigParser.SafeConfigParser()

        try:
            user = os.environ['SUDO_USER']
            conf_user = os.path.expanduser('~'+user+"/."+CONF_FILENAME)
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



class Pigshare(object):

    def __init__(self):

        self.config = PigshareConfig()

        self.cli = pyclist('pigshare', 'A commandline wrapper for the Figshare REST API')
        self.cli.root_parser.add_argument('--url', '-u', help='Figshare base url', default=self.config.figshare_url)
        self.cli.root_parser.add_argument('--token', '-t', help='Token to connect to figshare', default=self.config.figshare_token)

        self.cli.root_parser.add_argument('--profile', '-p', help='Profile to use (profile must be defined in ~/.pigshare.conf), takes precedence over --url and --token config')

        self.cli.root_parser.add_argument('--output', '-o', help='Filter output format')
        self.cli.root_parser.add_argument('--separator', '-s', default='\n', help='Seperator for output, useful to create a comma-separated list of ids. Default is new-line')

        self.cli.add_command(figshare_api)

        self.cli.parse_arguments()

        self.url = self.cli.namespace.url
        self.token = self.cli.namespace.token

        if self.cli.namespace.profile:
            self.cli.parameters['url'] = self.config.config.get(self.cli.namespace.profile, 'url')
            self.cli.parameters['token'] = self.config.config.get(self.cli.namespace.profile, 'token')


        self.cli.execute()

        self.output = self.cli.namespace.output
        self.separator = self.cli.namespace.separator

        self.cli.print_result(self.output, self.separator)

        # try:
            # self.namespace.func(self.namespace)
        # except Exception as e:
            # traceback.print_exc()
            # print e
            # sys.exit(0)


    def print_output(self, result, output_format=None, separator='\n'):

        # json = result.to_json(indent=2, sort_keys=True)

        if isinstance(result, bool):
            print result
            return

        if isinstance(result, (Collections, Articles)):
            output = []
            for item in result:
                output.append(self.create_output_item(item, output_format))

            print separator.join(output)

            return

        else:
            output = self.create_output_item(result, output_format)
            print output

        # if not output_format:

            # if issubclass(result.__class__, Model):
                # pprint(dict(result))
            # else:
                # print result.__str__().encode('utf-8')


            # return

        # filter output


    def create_output_item(self, item, output_format=None):

        result = ""

        if output_format:
            values = []
            for token in output_format.split(","):
                v = getattr(item, token)
                values.append(unicode(v).replace('\n', ' '))

            result = u'\t'.join(values).encode('utf-8')

        else:
            result = pformat(dict(item))

        return result

def run():
    Pigshare()
