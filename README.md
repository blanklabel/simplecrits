Simple Crits
=========================

Simple Crits is an easy-to-use package for interacting with the Crits Authenticated REST API documented at https://github.com/crits/crits/wiki/Authenticated-API

Examples
--------
**Add an IP**
```python
from pprint import pprint
from simplecrits import Crits

username = 'apiuser'
api_key  = 'stopthatdoghehasmygum!'
base_uri = 'https://crits.example.com/api/v1'

crits = Crits(base_uri, username, api_key, True)
r = crits.ips.add(
        source = 'My Test Org',
        method = 'ips_example.py',
        ip = '1.0.0.0',
        ip_type = 'Address -ipv4-addr',
        campaign = 'Test-Campaign',
        add_indicator = True)
pprint(r)
```

**Search for IPs**
```python
filters = {
    'c-source.name': 'My Test Org',
    'c-campaign.name': 'Test-Campaign',
}
r = crits.ips.find(limit = 3, **filters)
pprint(r)
```

**Iterate over IP resources**
```python
# Iterate over all IPs
for ip in crits.ips:
    print '%s\t' % (ip.get('ip'),),

# Example of filtering while iterating
# with list comprehension just for fun
ips = [ ip for ip in crits.ips if int(ip['ip'].split('.')[-1]) % 2 == 0 ]
pprint(ips)
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
- Implementation of all filters/modifiers presented here: https://github.com/crits/crits/wiki/Authenticated-API

Installation
------------

To install simplecrits, simply:  
```bash
$ pip install git+https://github.com/blanklabel/simplecrits.git#egg=simplecrits
```
Or if you're the setup type:  
```bash
$ python setup.py install
```

Contribute
----------
No seriously -- DO IT! Most changes will probably make it into a merge
