import requests
from .api import API
requests.packages.urllib3.disable_warnings()

class Crits(object):
    '''Top-level Crits API abstraction.

    See link below for Crits Authenticated API info:

         https://github.com/crits/crits/wiki/Authenticated-API
    '''
    def __init__(self, base_uri, username, api_key, verify_ssl=True):
        '''Constructor

        Args:
            base_uri (str): Base API URI, e.g. https://crits.example.com/api/v1
            username (str): Crits API user name
            api_key (str): Crits API key
            verify_ssl (bool): verify SSL certs for HTTPS requests
        '''
        self.base_uri = base_uri
        self.username = username
        self.api_key = api_key
        self.verify_ssl = verify_ssl
        self.session = requests.Session()

    def __getattr__(self, resource):
        '''Access Crits resource API object as attr

        Returns Crits resourse API singleton object

        Args:
            resource (attr): Crits resource name
        '''
        options = {
            'username': self.username,
            'api_key': self.api_key,
            'verify_ssl': self.verify_ssl
        }
        return API(self.base_uri, resource, self.session, **options)

