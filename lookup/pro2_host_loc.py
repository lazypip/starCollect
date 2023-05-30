#!/usr/bin/python3

# 补充table pro2的hostname, country, city
# hostname仅限于starlinkisp.net与undefined.hostname.localhost
# python3 pro_4.py

from sys import path
path.append(r"/home/ubuntu/Academic/starlink")

from sys import stdout, stderr, argv
from utility import *
from typing import *


src = ['bgpHE', 'ipinfo', 'Rtable', 'geoip']
src = ['src_' + ele for ele in src]


def read_pro2(database: starlink_db, table='pro2') -> List:
    """ 从数据表pro2读取数据 约15k条
    
    读取ip, country

    ret example:
    [ ('102.215.56.0', 'NG'), 
    ('102.215.56.112', 'NG') ]

    TODO: 减少内存开销
    """
    
    query = "SELECT \
            subnet, country \
            from {}".format(table)
    
    res = database.select(query)

    return res


def lookup_location_host(ip: str) -> List:
    """ ipinfo 查询country, city
    
    ret:
        count, city, hostname (str / '')
    """
    filter_list = ['country', 'city', 'hostname']
    res = []

    ipinfo_json = request_ipinfo_json(ip)
    if not ipinfo_json:
        return [''] * len(filter_list)
    
    for filter in filter_list:
        res_filter = ipinfo_json.get(filter, '')
        res.append(res_filter)

    return res


def upload(ip, hostname, country, city, database: starlink_db, table='pro2'):
    """ 上传hostname与loc
    
    """
    # 若无country或hostname, 直接上传空字符

    if "'" in city:
        city = city.split("'")
        city = city[0] + r"\'" + city[1]

    query_base = "UPDATE {} \
        set hostname='{}', country='{}', city='{}' \
        where subnet='{}';"
    query = query_base.format(table, hostname, country, city, ip)

    try:
        database.update(query)
    except:
        print(query)
        # 继续运行，抛弃错误数据
        # exit(1)


def upload_noloc(ip, hostname, database, table='pro2'):
    """ 已有loc信息, 仅上传hostname
    
    """
    # 若无hostname, 直接上传空字符
    query_base = "UPDATE {} \
        set hostname='{}' \
        where subnet='{}';"
    
    query = query_base.format(table, hostname, ip)

    try:
        database.update(query)
    except:
        print(query)
        # 继续运行，抛弃错误数据
        # exit(1)


def hostname_filter(hostname: str):
    """ 仅保留starlinkisp.net与undefined.hostname.localhost
    """
    if ('starlinkisp.net' not in hostname) \
        and (hostname != 'undefined.hostname.localhost'):
        return ''
    
    return hostname


def main():
    # print('lookup hostname and city')
    database = starlink_db()

    info_list = read_pro2(database)
    print('--- data set: ', len(info_list))
    count = 0

    for ip, country in info_list:
        count += 1
        if count % 1000 == 0:
            print("---", count, '/', len(info_list))

        if country: 
            # 已有country信息, 非None/''; 使用dig减少ipinfo调用
            hostname = dig_ip([ip])[0]
            hostname = '' if hostname == None else hostname
            upload_noloc(ip, hostname_filter(hostname), database)
        else:
            # 无country信息
            country_r, city_r, hostname = lookup_location_host(ip)
            upload(ip, hostname_filter(hostname), country_r, city_r, database)

    # print('upload done')


if __name__ == "__main__":
    main()
