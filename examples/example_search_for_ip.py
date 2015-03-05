import logging
from pprint import pprint

from simplecrits import Crits


if __name__ == '__main__':
    # Setup tons of debugging so we can see exactly how everything works
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    logger_handler = logging.StreamHandler()
    logger_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(logger_handler)
    
    # Connect to CRITS
    crits = Crits(uri='https://example.com/crits/api/v1/',
                  username='example',
                  apikey='thatkeythatispartofanapi',
                  verify_ssl=False)
    
    # Search for IPs
    pprint(crits.ips.find(filters={'c-campaign.name': 'IsItMalicious',
                                   'c-source.name': 'IsItMalicious'},
                          only='ip',
                          limit=5))
    root_logger.info('Status of code of previous event: %s', crits.samples.request.status_code)
    root_logger.info('Headers from previous request: %s' % crits.samples.request.headers)
