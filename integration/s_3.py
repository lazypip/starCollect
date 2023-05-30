#!/usr/bin/python3

# 第三阶段: 数据/28去重
# table pro1扩展到/28写入table pro2

from sys import path
path.append(r"/home/ubuntu/Academic/starlink")

from sys import stdout, stderr, argv
from utility import *
from typing import *


src = ['bgpHE', 'ipinfo', 'Rtable', 'geoip']
src = ['src_' + ele for ele in src]

expand_g4 = [str(v << 4) for v in range(2**4)]

def read_pro1(database: starlink_db, table='pro1') -> List:
    """ 从数据表pro1读取数据 约960条
    
    pro1的prefix均为24

    ret example:
    [ ('102.215.56.0', '14593', 1, 1, 1), 
    ('102.215.57.0', '14593', 1, 1, 1) ]
    """
    
    src_pro1 = src[:3]
    query = "SELECT \
            subnet, asn, {} \
            from {}".format(", ".join(src_pro1), table)
    
    res = database.select(query)

    return res


def expand_prefix24_28(ip: str) -> List:
    """ 将prefix 24 扩展到多个 prefix 28
    
    """
    ip = ip.split('.')
    res = []

    for i in expand_g4:
        ip[3] = i
        res.append(".".join(ip))

    # print(res)
    return res


def upload(ip_list, asn, bgpHE, ipinfo, Rtable, database: starlink_db, table='pro2') -> List:
    """ 上传数据至pro2, 由此完成去重
    
    prefix均为28
    """

    prefix = 28

    # None值的处理 直接写入空字符
    bgpHE = 0 if not bgpHE else 1
    ipinfo = 0 if not ipinfo else 1
    Rtable = 0 if not Rtable else 1

    query_base = "INSERT INTO {} (subnet, prefix, asn, src_bgpHE, src_ipinfo, src_Rtable, src_geoip) \
            VALUES ('{}', '{}', '{}', {}, {}, {}, 0) \
            ON DUPLICATE KEY UPDATE src_bgpHE = {}, src_ipinfo = {}, src_Rtable = {}"
    
    for ip in ip_list:
        query = query_base.format(table, ip, prefix, asn, bgpHE, ipinfo,Rtable, bgpHE, ipinfo,Rtable)
        try:
            database.insert(query)
        except:
            print(query)
            # 继续运行，抛弃错误数据
            # exit(1)


def main():
    # print('pro1 -> pro2 /28')
    database = starlink_db()
    
    info_list = read_pro1(database)

    for ip, asn, bgpHE, ipinfo, Rtable in info_list:
        ip_list = expand_prefix24_28(ip)
        upload(ip_list, asn, bgpHE, ipinfo, Rtable, database)

    # print('upload done')


if __name__ == "__main__":
    main()
