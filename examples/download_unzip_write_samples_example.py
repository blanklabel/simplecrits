from zipfile import ZipFile, BadZipfile
from simplecrits import Crits
from cStringIO import StringIO
import os
import logging

crits_uri = '<base URI>'
crits_user = '<username>'
crits_api = '<API KEY>'

def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start

@coroutine
def write_file():
    while True:
        f, name = yield
        filename = name + '.zip'
        zipped = StringIO()
        # turn into buffered object
        for l in f(chunk_size=1024):
            zipped.write(l)
        # Extract and rename
        try:
            with ZipFile(zipped) as zf:
                extracted_file_name = zf.namelist()[0]
                zf.extract(member=extracted_file_name, pwd='infected')
                os.rename(extracted_file_name,
                          u'./{file_name}'.format(file_name=filename[:-4]))
        except OSError, BadZipFile:
            yield None
        except UnicodeEncodeError as e:
            yield None
        else:
            yield filename[:-4]

@coroutine
def get_files(crits, target, f_format=''):
    while True:
        file_id, filename = yield
        f = crits.samples.find(o_id=file_id,
                               file=1,
                               file_format=f_format)

        t = target.send((f, filename))
        yield t
        

if __name__ == '__main__':
    # Setup tons of debugging so we can see exactly how everything works
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.ERROR)
    logger_handler = logging.StreamHandler()
    logger_handler.setLevel(logging.ERROR)
    root_logger.addHandler(logger_handler)

    # can be zlib,base64 or invert
    # f_format = ''

    # Connect to CRITS
    crits = Crits(base_uri=crits_uri,
                  username=crits_user,
                  api_key=crits_api,
                  verify_ssl=False)

    # Search all samples in a campaign
    file_meta = crits.samples.find(only='md5,sha1,sha256,ssdeep,filetype,filename,size',
                                   filters={'c-bucket_list__in':'web shell'}, limit=5)
    for l in file_meta['objects']:
        g = get_files(crits,write_file())
        n = g.send((l['_id'], l['filename']))
        print n
