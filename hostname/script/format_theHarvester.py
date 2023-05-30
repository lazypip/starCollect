# 格式化theHarvester hostname
# testfile - theHarvester-test

"""
input: 
    

output:
    id hostname
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
            text = text.split('"')
            hostname = text[1]

            if ':' in hostname:
                hostname = hostname.split(':')[0]

            print(id, hostname)
        except:
            break


if __name__ == '__main__':
    main()
