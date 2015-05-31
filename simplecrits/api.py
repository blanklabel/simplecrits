import requests
from urllib import urlencode

class ResourceSingleton(type):
    '''Resource Singleton
    
    Each Crits resource, e.g. ips, campaigns, is represented
    by a singleton object. To put it another way, all calls to

        https://crits.example.com/api/v1/ips
    
    are made by a singleton object, and all calls to 

        https://crits.example.com/api/v1/campaigns

    are made by a separate singleton object, etc.
    '''
    _instances = {}

    def __call__(cls, *args, **kwargs):
        '''Create & return new obj if one doesn't exists, else return existing one.'''
        key = (cls, args[1])
        if key not in cls._instances:
            cls._instances[key] = super(ResourceSingleton, cls).__call__(*args, **kwargs)

        return cls._instances[key]

class API(object):
    '''Crits API

    The API class wraps the Crits REST API. See link below
    for official REST API documentation:

        https://github.com/crits/crits/wiki/Authenticated-API#post-responses

    The API class implements the Singleton pattern around the
    different types of Crits resources, i.e. campaigns, ips, etc.
    
    Each Resource Singleton maintains its own Session object that persists
    certain parameters across requests.
    '''
    __metaclass__ = ResourceSingleton

    def __init__(self, base_uri, resource, session = None, **options):
        '''Constructor
        
        Args:
            base_uri (str): Base API URI, e.g. https://crits.example.com/api/v1
            resource (str): Crits resource, e.g. campaigns, ips, etc.
            session (Session obj): Requests lib session obj, default None
            **options: keyword args
                username (str): Crits API user name
                api_key (str): Crits API key
                verify_ssl (bool): verify SSL certs for HTTPS requests 
        '''
        self.uri = '/'.join([x.rstrip('/') for x in (base_uri, resource)])
        if session:
            self.session = session
        else:
            self.session = requests.Session()
        self.options = {}
        self.options.update(options)

    def __iter__(self):
        '''Iterator'''
        return self.iterfind()

    def find(self, oid = '', **options):
        '''Find Crits resources

        See link below for docs on using query params:

            https://github.com/crits/crits/wiki/Authenticated-API#searching-using-get-parameters
        
        Args:
            oid (str): object id. Defaults to ''
            **options: keyword args
                username (str): API username -- override value passed in ctor
                api_key (str): API key -- override value passed in ctor
                sundry other params 
        Returns:
            Request result
        '''
        params = { 'verify': self.options.get('verify_ssl', False) }
        params.update(options)

        params['username'] = params.get('username', self.options.get('username'))
        params['api_key'] = params.get('api_key', self.options.get('api_key'))

        if oid:
            uri = '/'.join([self.uri, oid, ''])
        else:
            uri = '/'.join([self.uri, ''])

        verify = params.pop('verify')

        request = self.session.get(
                    uri, 
                    params = urlencode(params), 
                    verify = verify,
                    stream = params.get('file', False))

        if request.headers['content-type'] == 'application/json':
            return request.json()
        elif request.headers['content-type'].find('octet-stream') != -1:
            return request.iter_content
        else:
            return request.text

    def iterfind(self, **options):
        '''Iterate over filtered find results

        Retrieve 1st 100 resource objects and yield each one,
        retrieve 2nd 100 resource objects and yield each one,
        etc, etc, etc...until done.

        See link below for docs on using query params:

            https://github.com/crits/crits/wiki/Authenticated-API#searching-using-get-parameters

        Args:
            **options: keyword args

        Yields:
            Resource Object
        '''
        offset = 0
        limit = 100

        tmp = self.find(offset = offset, limit = limit, **options)
        total_count = tmp['meta']['total_count']

        while offset < total_count:
            for obj in tmp['objects']:
                yield obj
            offset += limit
            tmp = self.find(offset = offset, limit = limit, **options)

    def add(self, file_path = None, **options):
        '''Add Crits resource objects

        See link below for more info:

            https://github.com/crits/crits/wiki/Authenticated-API#post-responses

        Args:
            file_path (str): file to upload, Default None
            **options: keword args
                username (str): API username -- override value passed in ctor
                api_key (str): API key -- override value passed in ctor
                sundry other params 
        Returns:
            Request result
        '''
        params = { 'verify': self.options.get('verify_ssl', False) }
        params.update(options)

        params['username'] = params.get('username', self.options.get('username'))
        params['api_key'] = params.get('api_key', self.options.get('api_key'))
        
        uri = '/'.join([self.uri, ''])
        verify = params.pop('verify')

        files = None
        if file_path:
            files = { 'filedata': open(file_path, 'rb')}

        request = self.session.post(uri, data = params, verify = verify, files = files)

        if request.headers['content-type'] == 'application/json':
            return request.json()
        else:
            return request.text

