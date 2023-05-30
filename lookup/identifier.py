#!/usr/bin/python3

# 填充每个网段的标识符(用途)
# table: pro2
# table: 将pro2的结果复制到hostinfo, 用以后续统计
# need: python3 -u

from sys import path
path.append(r"/home/ubuntu/Academic/starlink")

from sys import stdout, stderr, argv
from os import environ

from utility import *
from typing import *

# 依据 hostname, src_geoip, network 149.19.108/23 与 206.224.64/19
identifier = ['customer-pop', 'customer-mc', 'customer', 'network-devices', 'undefined']


def if_in_subnet(subnet: str):
    """
    判断subnet是否在 149.19.108/23 或 206.224.64/19中
    """
    ip_g3 = int(subnet.split('.')[2])
    if '149.19.' in subnet:
        if (ip_g3 & 254) == 108:
            return True
    
    if '206.224.' in subnet:
        if (ip_g3 & 224) == 64:
            return True
    
    return False


def mark(info) -> str:
    """
        若有多个标识, 按照优先级取第一个
        无标识 ret - ''
    """
    subnet, hostname, src_geoip = info
    iden = []

    # customer
    if "customer" in hostname:
        if 'pop' in hostname:
            iden.append(identifier[0])
        if 'mc' in hostname:
            iden.append(identifier[1])
    
    if src_geoip:
        iden.append(identifier[2])

    # network-devices
    # customer与network-devices原则上不能同时出现, 但经过测试二者不会同时出现
    if if_in_subnet(subnet):
        iden.append(identifier[3])

    if "undefined" in hostname:
        iden.append(identifier[4])
    
    if len(iden) == 0:
        iden.append('')

    return iden


def read_pro2(database: starlink_db, table='pro2'):
    """
    """
    query_base = "SELECT subnet, hostname, src_geoip from {}"
    res = database.select(query_base.format(table))

    return res


def upload(subnet, iden, database: starlink_db):
    """ 将iden上传至表hostinfo与pro2
    """
    query_base = "UPDATE {} set identifier='{}' where subnet='{}'"
    database.update(query_base.format('pro2', iden, subnet))

    res = database.select("SELECT 1 from {} where subnet='{}'".format('hostinfo', subnet))
    if res != []:
        database.update(query_base.format('hostinfo', iden, subnet))


def main():
    database = starlink_db()

    dataset = read_pro2(database)
    for subnet, hostname, src_geoip in dataset:
        iden = mark([subnet, hostname, src_geoip])[0]
        upload(subnet, iden, database)


if __name__ == "__main__":
    main()
