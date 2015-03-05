import logging

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
    
    # Add a new file
    crits.samples.add(file_path='testfile.txt', source='CSIRT', 
                      upload_type='file',
                      bucket_list='zomgdeleteme,notreal,tagsforlife',
                      file_format='raw',
                      file_type='text',
                      confidence='high')
    
    root_logger.info('Body from previous request: %s', crits.samples.request.text)
    root_logger.info('Headers from previous request: %s', crits.samples.request.headers)
