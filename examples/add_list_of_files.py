import logging

from simplecrits import Crits


filelist = '/full/path/to/textfile/list.txt'

 
if __name__ == '__main__':
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    logger_handler = logging.StreamHandler()
    logger_handler.setLevel(logging.INFO)
    root_logger.addHandler(logger_handler)
    crits = Crits(uri='https://example.com/crits/api/v1/',
                  username='example',
                  apikey='keythatshouldnotbesentthroughemail',
                  verify_ssl=False)
 
    with open(filelist, "r") as files:
        for filename in files:
            filename = filename.strip()
            crits.samples.add(file_path=filename, upload_type='file',
                              source='CSIRT-CSA',
                              bucket_list='iIIDnumber,Mr Bucket',
                              file_format='raw')
            root_logger.info('Status of code of previous event: %s', crits.samples.request.status_code)
            root_logger.info('Headers from previous request: %s' % crits.samples.request.headers)
