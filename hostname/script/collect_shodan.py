# shodan api -> hostname
#

"""
output - ip : hostname
"""

import shodan
from typing import List
from sys import stdout, stderr
from os import environ

SHODAN_API_KEY = environ.get('token_shodan')
if not SHODAN_API_KEY:
        print("source ./token")
        exit(1)

api = shodan.Shodan(SHODAN_API_KEY)


try:
        id = 0

        # hostnames 为必返回字段, 由于检索条件，一定有starlinkisp.net
        # 在backup中保留 ip : hostnames
        for host in api.search_cursor('hostname:starlinkisp.net'):
                id = id + 1
                ip = host['ip_str']
                hostnames: List = host['hostnames']
                hostnames = [hostname for hostname in hostnames if 'starlinkisp.net' in hostname]
                asn = host.get('asn', None)
                
                print(id, hostnames[0], ip, asn, file=stdout)

except shodan.APIError as e:
        print('Error: {}'.format(e))
        exit(1)
