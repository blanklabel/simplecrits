import logging

from simplecrits import Crits


def write_file(f, name):
    filename = name + '.zip'
    sample = open(filename, 'wb')
    for chunk in f(chunk_size=1024):
        if chunk:
            sample.write(chunk)
    sample.close()

if __name__ == '__main__':
    # Setup tons of debugging so we can see exactly how everything works
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    logger_handler = logging.StreamHandler()
    logger_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(logger_handler)

    # can be zlib,base64 or invert
    f_format = '' 
    
    # Connect to CRITS
    crits = Crits(uri='https://example.com/crits/api/v1/',
                  username='example',
                  apikey='supersecretapi',
                  verify_ssl=False)
    
    # Search all samples in a campaign
    file_meta = crits.samples.find(filters={'c-campaign.name': 'Savage Squirrel'},
                                   only='md5,sha1,sha256,ssdeep,filetype,filename,size')

    for l in file_meta['objects']:
        root_logger.info(l['_id'])
        root_logger.info(l['filename'])
        f = crits.samples.find(o_id=l['_id'], 
                               file=1, # request the file to be downloaded
                               file_format=f_format) # can be zlib,base64 or invert
        write_file(f, l['filename'])
