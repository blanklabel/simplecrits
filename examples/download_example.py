from pprint import pprint
from simplecrits import Crits

username = 'apiuser'
api_key  = 'stopthatdoghehasmygum!'
base_uri = 'https://crits.example.com/api/v1'

def write_file(f_iter, filename):
    '''Write zip file

    See: https://github.com/crits/crits/wiki/Authenticated-API#api-urls
    
    From link above, Zip file passwd is: 'infected'
    '''
    filename = '%s.zip' % (filename,)
    with open(filename, 'wb') as f:
        for chunk in f_iter(chunk_size = 1024):
            if chunk:
                f.write(chunk)

if __name__ == '__main__':
    crits = Crits(base_uri, username, api_key, False)
 
    file_format = ''
    filters = {
        'only': 'md5,sha1,sha256,ssdeep,filetype,filename,size',
        'c-campaign.name': 'Test-Campaign'
    }
    meta = crits.samples.find(**filters)

    for obj in meta.get('objects', []):
        f_iter = crits.samples.find(
                    obj['_id'],
                    file = True,
                    file_format = file_format)
        write_file(f_iter, obj['filename'])

