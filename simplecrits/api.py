"""
simplecrits.api
~~~~~~~~~~~~

This module implements the simplecrits API.

"""

import logging
from urllib import urlencode

from .lib.core.singleton import ResourceSingleton


# Setup the module LOGGER
logger = logging.getLogger(__name__)


class API(object):
    """
    Abstraction layer to communicate with CRITS API
    """
    __metaclass__ = ResourceSingleton

    def __init__(self, session, base_uri, auth_pair, verify_ssl, _resource):
        """
        :param session: Requests session
        :param base_uri: URI of crits instance with version included
        :param auth_pair: dictionary of username/apikey eg
               {'username':'joe','api_key':'zomgkey'}
        :param verify_ssl: verify SSL or not
        :param _resource: identification of which resource we
        are acting against eg "ips","campaigns"
        :return:
        """
        self.session = session
        self.base_uri = base_uri
        self.auth_pair = auth_pair
        self.verify_ssl = verify_ssl
        self._resource = _resource
        self.request = None
        self._next = None

        logger.debug('Base URI: %s Caller: %s', self.base_uri,
                     self._resource)

    def __iter__(self):
        """
        Currently a terrible hack that needs to be broken out so that if you for loop through a get from the
        start of the object, you get all the results you desire
        :return:
        """
        return self

    def next(self):
        """
        Convience wrapper to call the next set of results
        :return: A call to the "find" method
        """
        if self._next is not None:
            return self.find(self._next[0], self._next[1], **self._next[2])
        else:
            raise StopIteration

    def _set_next(self, request, o_id, modifiers, filters):
        # Setup the call to "next"
        limit = request.json()['meta']['limit']
        offset = request.json()['meta']['offset']
        total_count = request.json()['meta']['total_count']

        # Basic math to determine if there is no next
        # if we need to ask for what's left
        # or if we can just make another request with the proper limit
        if offset + limit >= total_count:
            self._next = None
        elif offset + limit*2 > total_count:
            modifiers.update(offset=offset + limit, limit=total_count - (offset + limit))
            self._next = (o_id, filters, modifiers)
        else:
            modifiers.update(offset=offset + limit)
            self._next = (o_id, filters, modifiers)

    def find(self, o_id=None, filters=None, **modifiers):
        """
        Abstraction function to call http "get" against CRITs interface
        :param o_id: object unique identifier to work upon
        :param filters: filter logic to get specific results
        :param modifiers: parameters to modify the results
        specific to the filter
        :return: Results of query in the format requested -- Json by default
        """
        # combine all arguments for filtering and modification
        modifiers.update(self.auth_pair)
        
        # Build proper URI path based upon o_id only 
        # setup filters for requests without a o_id
        # as they won't work
        if o_id:
            uri = '%s%s/%s' % (self.base_uri, self._resource, o_id)
        else:
            uri = '%s%s/' % (self.base_uri, self._resource)
            # Add any filters that may exist
            if filters:
                modifiers.update(filters)

        logger.debug('%s.find called with ARGS: %s', self._resource,
                     modifiers)

        # Perform the get on the provided URI
        request = self.session.get(uri, params=urlencode(modifiers),
                                   verify=self.verify_ssl,
                                   stream=modifiers.get('file', False))
        # Set the results to the parent class for later utilization
        self.request = request
        logger.debug('Request status: %s HEADERS: %s', request.status_code, request.headers)

        # Prepare the json applications, give an iter to download files
        # or otherwise return a text object
        if request.headers['content-type'] == 'application/json':
            self._set_next(request, o_id, modifiers, filters)
            return request.json()

        # Must be a file object -- stream it
        elif request.headers['content-type'].find('octet-stream') != -1:
            return request.iter_content

        # Random other encoding... which does not set "next" object
        else:
            return request.text

    def add(self, file_path=None, **post_data):
        """
        Abstraction function to call http "get" against CRITs interface
        :param file_path: files to upload to CRITS in the following format:
              '/path/to/file.pcap'
        :param post_data: keyword arguments to particular post type
        :return: Results of query in the format requested -- Json by default
        """
        # Build proper URI path based upon resource
        uri = '%s%s/' % (self.base_uri, self._resource)

        # Update post in data with authentication pieces
        post_data.update(self.auth_pair)
        logger.debug('%s.add called with POST_DATA: %s', self._resource, post_data)

        # Perform the POST on the provided URI
        if file_path:
            logger.debug('uploading_file: %s', file_path)
            post_file = {'filedata': open(file_path, 'rb')}
            request = self.session.post(uri, files=post_file, data=post_data,
                                        verify=self.verify_ssl)
        else:
            request = self.session.post(uri, data=post_data,
                                        verify=self.verify_ssl)

        logger.debug('URL: %s Request Status: %s HEADERS: %s', request.url,
                     request.status_code, request.headers)

        # Set the results to the parent class for later utilization
        self.request = request

        # Prepare the json applications
        # or otherwise return a text object
        if request.headers['content-type'] == 'application/json':
            return request.json()
        else:
            return request.text