# 格式化shodan hostname
# testfile - shodan-test

"""
input: 
    id hostname ipv4/ipv6 asn

output:
    id hostname
"""

from sys import path, stdout, stderr
path.append(r"/home/ubuntu/Academic/starlink")

from utility import *


def main():
    hostnames = []

    while True:
        try:
            text = input()
            text = text.split(' ')
            hostname = text[1]
            hostnames.append(hostname)

        except:
            break
    
    hostnames = list(set(hostnames))
    for id, hostname in enumerate(hostnames, start=1):
        print(id, hostname)


if __name__ == '__main__':
    main()
