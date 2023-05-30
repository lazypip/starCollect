# 格式化ipinfo hostname
# testfile - ipinfo-test

"""
input: 
    ip prefix of starlinkisp.net

output:
    id hostname
"""

from sys import path, stdout, stderr
path.append(r"/home/ubuntu/Academic/starlink")

from utility import *


def main():
    hostnames = []

    id = 0
    
    while True:
        id += 1
        try:
            text = input()
            text = text.split('"')[1]

            ip, prefix = text.split('/')
            hostname = dig_ip([ip])[0]
            
            if not hostname or ('starlinkisp.net' not in hostname):
                continue

            hostnames.append(hostname)
        except:
            break
    
    hostnames = list(set(hostnames))
    for id, hostname in enumerate(hostnames, start=1):
        print(id, hostname, file=stdout)


if __name__ == '__main__':
    main()
