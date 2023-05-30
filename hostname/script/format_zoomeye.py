# 格式化zoomeye hostname
# cat $file1 | grep 'name' | python3 script/format_zoomeye.py > res/$res1
# testfile - zoomeye-test

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

            hostname = text[3]
            
            print(id, hostname)
        except:
            break


if __name__ == '__main__':
    main()
