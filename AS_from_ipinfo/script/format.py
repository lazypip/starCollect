# 格式化prefix origin
# cat 14593 | jq '.ipv4' | grep '/' | python3 fromat.py
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
            
            text = text.split('"')[3]
            ip, prefix = text.split('/')

            print(id, ip, prefix)
        except:
            break


if __name__ == '__main__':
    main()
