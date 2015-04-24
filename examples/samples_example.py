from pprint import pprint
from simplecrits import Crits

username = 'apiuser'
api_key  = 'stopthatdoghehasmygum!'
base_uri = 'https://crits.example.com/api/v1'

if __name__ == '__main__':
    crits = Crits(base_uri, username, api_key, False)
  
    # Add new Sample 
    r = crits.samples.add(
            file_path = 'testfile.txt',
            source = 'My Test Org',
            method = 'samples_example.py',
            upload_type = 'file',
            file_format = 'raw',
            file_type = 'text',
            campaign = 'Test-Campaign',
            confidence = 'high')     
    pprint(r)

    # Retrieve Sample by object ID
    oid = r['id']
    r = crits.sample.find(oid)
    pprint(r)
    
    # Iterate over all Samples 
    for sample in crits.samples:
        pprint(sample)

