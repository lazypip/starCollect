#!/usr/bin/python3

# 第一阶段合并与去重
# cat () | python3 s_1.py src asn

from sys import path
path.append(r"/home/ubuntu/Academic/starlink")

from sys import stdout, stderr, argv
from utility import *
from typing import *


def read_stdin() -> List:
    ip_prefix_list = []  # [(ip, prefix), ]
    while True:
        try:
            text = input()
            _, ip, prefix = text.split(' ')

            ip_prefix_list.append((ip, prefix))
        except:
            break
    
    return ip_prefix_list


def expand_prefix_24(ip_prefix: tuple) -> List:
    """ 将prefix扩展至 /24 以去重
    仅操作第三组8bit数据
    
    example:
    ('64.9.224.0, 23') -> 
    ['64.9.224.0', '64.9.225.0'] prefix均为24
    """
    res = []  # [64.9.224.0, 64.9.225.0]

    ip, prefix = ip_prefix
    ip = ip.split('.')
    ip_g3_base = int(ip[2])

    expand_bit_num = 24 - int(prefix)
    if expand_bit_num < 0:  # TODO: 出现特殊prefix
        expand_bit_num = 0

    for add in range(2**expand_bit_num):
        ip_g3 = ip_g3_base + add
        ip[2] = str(ip_g3)
        res.append('.'.join(ip))
    
    return res


def upload(ip_list, src, asn, database, table='pro1') -> None:
    """ 将数据上传至数据表 pro1
    
    通过mysql数据表去重, prefix默认24
    """

    prefix = 24

    # 若ip地址重复，则仅更新数据来源
    query_base = "INSERT INTO {} (subnet, prefix, asn, {}) \
            VALUES ('{}', '{}', '{}', 1) \
            ON DUPLICATE KEY UPDATE {} = 1"
    
    for ip in ip_list:
        query = query_base.format(table, src, ip, prefix, asn, src)
        database.insert(query)
    
    return


def main():
    if len(argv) != 3:
        print("usage: python3 s_1.py src asn")
        exit(1)
    
    src, asn = 'src_' + argv[1], argv[2]
    # print('AS'+asn, 'from', src)
    database = starlink_db()

    ip_prefix_list = read_stdin()
    for ip_prefix in ip_prefix_list:
        ip_24_list = expand_prefix_24(ip_prefix)
        upload(ip_24_list, src, asn, database)

    # print('upload done')


if __name__ == "__main__":
    main()
