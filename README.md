simplecrits: Crits Client API interaction for everyone
=========================

Crits currently does not have a client module for interacting with the api.
simplecrits aims to make this libary simple to use in a manner that
is extensable without additional code required to be written.
the HTTP capabilities you should need, but the api is thoroughly broken.


Search for an IP
```python
from simplecrits import Crits
from pprint import pprint

crits = Crits(uri='https://example.com/crits/api/v1/',
              username='joesixpack',
              apikey='soooomanynumbers',
              verify_ssl=False)

pprint(crits.ips.find(filters={'c-campaign.name': 'IsItMalicious',
                               'c-source.name': 'IsItMalicious'},
                      only='ip',
                      limit=5))
```

Add an IP (Assuming already authenticated)
```python
# Add a new ip
crits.ips.add(source='CSIRT',
              ip='127.0.0.127',
              ip_type='Address - ipv4-add',
              bucket_list='zomgdeleteme,notreal,tagsforlife',
              confidence='high')
```

Add an IP and treat it as an indicator
```python
# Add a new ip
crits.ips.add(source='CSIRT',
              ip='127.0.0.127',
              ip_type='Address - ipv4-add',
              bucket_list='zomgdeleteme,notreal,tagsforlife',
              add_indicator=True,
              confidence='high')
```

Add a file to samples resource
```python
# Add a new file
crits.samples.add(file_path='testfile.txt', source='CSIRT', 
                  upload_type='file',
                  bucket_list='zomgdeleteme,notreal,tagsforlife',
                  file_format='raw',
                  file_type='text',
                  confidence='high')
```

Features
--------

- Keep-Alive & Connection Pooling
- Sessions with Cookie Persistence
- Browser-style SSL Verification
- Automatic Decompression
- Unicode Response Bodies
- Multipart File Uploads
- Connection Timeouts
- Thread-safety
- implimentation of all filters/modifiers presented here: https://github.com/crits/crits/wiki/Authenticated-API

Installation
------------

To install simplecrits, simply:

```bash

    $ pip install -e simplecrits/
```
Or if you're the setup type

```bash

    $ python setup.py install
```

Contribute
----------

No seriously -- DO IT! Most changes will probably make it into a merge
