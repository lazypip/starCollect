#!/usr/bin/python3

# 收集主机信息并写入数据库hostinfo
# need: python3 -u

from sys import path
path.append(r"/home/ubuntu/Academic/starlink")

import shodan
import json

from sys import stdout, stderr, argv
from os import environ

from utility import *
from typing import *


SHODAN_API_KEY = environ.get('token_shodan')
if not SHODAN_API_KEY:  # None
    print("usage: source token")
    exit(1)

api = shodan.Shodan(SHODAN_API_KEY)


# 需要提取的shodan信息
# TODO
res_filter = ['transport', 'port', 'os', 'product', 'module', 'tls_version', 'hostname_public']

def read_db(database: starlink_db, table='pro2') -> List:
    """ 读取ip即可

    """
    query = "SELECT subnet from {}".format(table)
    res = database.select(query)
    ip_list = [ele[0] for ele in res]

    return ip_list


def shodan_parser_uni(host: Dict) -> List:
    """ 在shodan返回数据中提取指定的信息

    TODO: 做成指定的接口; 如何简化 - 关键词的特殊性
    """
    ip_str = host["ip_str"]

    transport = host.get("transport", '')
    port = str(host.get("port", ''))
    os = host.get("os", '')
    os = '' if not os else os  # null
    product = host.get("product", '')
    module = host["_shodan"]["module"]

    try:
        # 可能不存在
        tls_version = host["ssl"]["cipher"]["version"]
    except:
        tls_version = ''

    # TODO: 改进
    hostname_public_list = host.get("hostnames", [])  # list
    hostname_public = ''
    for hostname in hostname_public_list:
        if 'starlinkisp.net' not in hostname:
            hostname_public = hostname
            break

    info = [transport, port, os, product, module, tls_version, hostname_public]
    
    return ip_str, info


def upload(subnet, ip_str, info, database: starlink_db, table='hostinfo'):
    """ 将指定信息上传至数据表

    TODO:
    ip_str, [transport, port, os, product, module, tls_version]
    """

    prefix = '28'
    info = ["'" + ele + "'" for ele in info]

    query_base = "INSERT IGNORE into {} \
        (ip, subnet, prefix, {}) \
        values \
        ('{}', '{}', '{}', {});"
    query = query_base.format(table, ', '.join(res_filter), ip_str, subnet, prefix, ", ".join(info))

    try:
        database.insert(query)
    except:
        print(query)
        # 继续运行，抛弃错误数据
        # exit(1)


def collect_shodan(subnet, database):
    prefix = '28'
    filter = 'net:' + subnet + '/' + prefix

    try:
        for host in api.search_cursor(filter):
            # 转为json
            # host_json = json.dumps(host)
            # print(host_json)
            # host['ip_str']

            ip_str, info = shodan_parser_uni(host)
            upload(subnet, ip_str, info, database)

    except shodan.APIError as e:
        print('Error: {}'.format(e))
        exit(1)


def main():
    database = starlink_db()
    ip_list = read_db(database)
    ip_list_len = len(ip_list)
    count = 0

    print('--- start shodan lookup')
    print('--- subnet nums: ', ip_list_len)
    
    for subnet in ip_list:
        count += 1
        collect_shodan(subnet, database)

        if count % 1000 == 0:
            print('---', count, '/', ip_list_len)
    
    # print('shodan lookup done')


if __name__ == "__main__":
    main()
