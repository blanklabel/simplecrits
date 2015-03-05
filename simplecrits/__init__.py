"""
simplecrits
~~~~~~~~~~~~

This module implements the factory for the crits API

"""

import logging

import requests

from .api import API

# Setup the module LOGGER
logger = logging.getLogger(__name__)


class Crits(object):
    """
    Top level abstraction libary to interact with crits
    """
    def __init__(self, uri, username, apikey, verify_ssl=True):
        """
        :param uri: CRITS URI
        :param username: username to authenticate against crits
        :param apikey: APIKEY provided by crits
        :param verify_ssl: Validate the crits ssl cert or not
        :return:
        """
        self.uri = uri
        self.authpair = {'username': username,
                         'api_key': apikey}
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        logger.debug('URI: %s USERNAME: %s APIKEY: %s', uri, username, apikey)

    def __getattr__(self, name):
        """
        :param name: the resource in crits to be interacted with
        :return: Worker abstraction interaction with CRITS API
        """
        return API(self.session, self.uri, self.authpair,
                   self.verify_ssl, name)