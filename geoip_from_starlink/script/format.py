# 格式化geoip
# testfile - format-test

"""
input: 
    prefix

output:
    id ip prefix
"""

from sys import path, stdout, stderr
path.append(r"/home/ubuntu/Academic/starlink")

from utility import *


def main():
    id = 0
    
    while True:
        id += 1
        try:
            text = input()
            
            text = text.split(',')
            ip_prefix, country, _, city, _ = text
            ip, prefix = ip_prefix.split('/')

            print(id, ip, prefix, country, ',' + city, file=stdout)
        except:
            break


if __name__ == '__main__':
    main()
