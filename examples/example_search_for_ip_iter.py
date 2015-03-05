import logging

from simplecrits import Crits


if __name__ == '__main__':
    # Setup tons of debugging so we can see exactly how everything works
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    logger_handler = logging.StreamHandler()
    logger_handler.setLevel(logging.INFO)
    root_logger.addHandler(logger_handler)
    
    # Connect to CRITS
    crits = Crits(uri='https://example.com/crits/api/v1/',
                  username='example',
                  apikey='thatkeythatispartofanapi',
                  verify_ssl=False)
    
    # Search for IPs
    a = crits.ips.find(filters={'c-campaign.name': 'IsItMalicious',
                                'c-source.name': 'IsItMalicious'},
                                only='ip',
                                offset=5,
                                limit=5,
                                format='json')
    root_logger.info(a)

    for l in crits.ips:
        root_logger.info(l)
