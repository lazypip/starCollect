#!/usr/bin/python3

# 第二阶段 数据载入
# geoip扩展到/28写入table pro2

from sys import path
path.append(r"/home/ubuntu/Academic/starlink")

from sys import stdout, stderr, argv
from utility import *
from typing import *


def read_stdin() -> List:
    """
    input example:
    1 14.1.64.0 24 PH ,Manila

    output:
    [(ip, prefix, country, city), ]
    """
    info_list = []  # [(ip, prefix, country, city), ]

    while True:
        try:
            text = input()
            info, city = text.split(',')
            _, ip, prefix, country, __ = info.split(' ')

            info_list.append((ip, prefix, country, city))
        except:
            break
    
    return info_list


def expand_prefix_28(ip: str, prefix) -> List:
    """ 将prefix扩展到28
    geoip prefix在24-28间, 处理第四段8bit即可
    注意要先右移动四位再，左移四位
    
    """
    prefix = int(prefix)
    res = []  # [64.9.224.0, 64.9.225.0]

    ip = ip.split('.')
    ip_g4_base = int(ip[3])

    expand_bit_num = 28 - int(prefix)
    if expand_bit_num < 0:  # TODO: 出现特殊prefix
        expand_bit_num = 0

    for add in range(2**expand_bit_num):
        ip_g4 = ((ip_g4_base >> 4) + add) << 4
        ip[3] = str(ip_g4)
        res.append('.'.join(ip))
    
    return res


def ip_to_asn(ip:str):
    """ 由于geoip数据没有对应asn, 因此通过ipinfo查询加入

    geoip free plan中, asn以org的形式展现 "org": "AS15169 Google LLC"
    
    ret:
        str / None
    """

    ip_json: Dict = request_ipinfo_json(ip)
    if not ip_json:
        return ''

    asn = ip_json.get('org', '')
    if not asn:
        return ''
    
    return asn.split(' ')[0][2:]


def upload(ip_list, city, country, src, asn, database, table='pro2') -> None:
    """
    
    """
    prefix = 28
    if "'" in city:
        city = city.split("'")
        city = city[0] + r"\'" + city[1]

    query_base = "INSERT INTO {} (subnet, prefix, asn, country, city, {}) \
            VALUES ('{}', '{}', '{}', '{}', '{}', 1) \
            ON DUPLICATE KEY UPDATE {} = 1"

    for ip in ip_list:
        query = query_base.format(table, src, ip, prefix, asn, country, city, src)

        try:
            database.insert(query)
        except:
            print(query)
            # 继续运行，抛弃错误数据
            # exit(1)


def main():
    src = 'src_geoip'
    # print('info from', src)

    database = starlink_db()
    info_list = read_stdin()

    for ip, prefix, country, city in info_list:
        asn = ip_to_asn(ip)
        ip_list = expand_prefix_28(ip, prefix)
        upload(ip_list, city, country, src, asn, database)

    # print('upload done')


if __name__ == "__main__":
    main()

    # print(ip_to_asn('65.181.0.0'))
    # print(ip_to_asn('135.129.247.0'))

    # res = expand_prefix_28('14.1.64.0', 24)
    # print('\n\n')
    # res = expand_prefix_28('135.129.120.128', 26)
    # print('\n\n')
    # res = expand_prefix_28('98.97.73.208', 28)
