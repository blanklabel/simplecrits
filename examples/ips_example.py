from pprint import pprint
from simplecrits import Crits

username = 'apiuser'
api_key  = 'stopthatdoghehasmygum!'
base_uri = 'https://crits.example.com/api/v1'

if __name__ == '__main__':
    crits = Crits(base_uri, username, api_key, True)
    
    # Add new IPs
    for x in range(1, 9):
        r = crits.ips.add(
                source = 'My Test Org',
                method = 'ips_example.py',
                ip = '1.0.0.%d' % (x,),
                ip_type = 'Address -ipv4-addr',
                campaign = 'Test-Campaign',
                add_indicator = True)
        pprint(r)

    # Search for IPs
    filters = {
        'c-source.name': 'My Test Org',
        'c-campaign.name': 'Test-Campaign',
    }
    r = crits.ips.find(limit = 3, **filters)
    pprint(r)

    # Iterate over all IPs
    for ip in crits.ips:
        print '%s\t' % (ip.get('ip'),),

    # Example of filtering while iterating
    # with list comprehension just for fun
    ips = [ ip for ip in crits.ips if int(ip['ip'].split('.')[-1]) % 2 == 0 ]
    pprint(ips) 

