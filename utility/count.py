#!/usr/bin/python3

# 生成report并写入

from sys import path
path.append(r"/home/ubuntu/Academic/starlink")

from sys import stdout, stderr, argv
from utility import *
from typing import *
from collections import Counter


def read_shodan(database, table='hostinfo'):
    query = "SELECT ip, subnet from {}".format(table)
    res = database.select(query)  # [(ip, subnet)]

    return res


def count_hostinfo_part1(data):
    """
    # TODO: 算法优化 (换用select count / 重整条件与目的-直接去重即可 /字典)
    # 提取每个subnet拥有活跃ip的数量
    """
    data_num = len(data)
    # 去重 -> 唯一ip
    data = list(set(data))

    host_nums = len(data)
    subnet_list = [host[1] for host in data]

    subnet_hostnum_dict = {}

    for subnet in list(set(subnet_list)):
        subnet_hostnum_dict[subnet] = subnet_list.count(subnet)

    print('shodan scan')
    print('data nums: ', data_num)
    print('host nums: ', host_nums)  # ip数量
    print('related subnet nums', len(subnet_hostnum_dict))
    print('host nums per subnet: ')
    # for subnet, nums in subnet_hostnum_dict.items():
    #     print('- ', subnet, ':', nums)


def count_hostinfo(database: starlink_db, table='hostinfo'):
    """ hostinfo表中的统计信息
    
    """
    data = read_shodan(database, table)
    count_hostinfo_part1(data)

    query_base = "SELECT count(*) from {} where transport='{}'"
    tcp_num = database.select(query_base.format(table, 'tcp'))
    tcp_num = tcp_num[0][0]
    udp_num = database.select(query_base.format(table, 'udp'))
    udp_num = udp_num[0][0]
    print('tcp host nums:', tcp_num)
    print('udp host nums:', udp_num)

    query_base = "select count(*) from {} where tls_version != ''"
    tls_num = database.select(query_base.format(table))
    tls_num = tls_num[0][0]
    print('host with tls:', tls_num)

    query_base = "select hostname_public from {} where hostname_public != ''"
    hostname_public = database.select(query_base.format(table))
    hostname_public = [ele[0] for ele in hostname_public]
    hostname_public = list(set(hostname_public))
    print('host with public hostnames:', len(hostname_public))


if __name__ == "__main__":
    database = starlink_db()
    count_hostinfo(database)

    count_hostinfo(database, 'backup_20230429_215707_hostinfo')







"""
def count_shodan_host(data):
    data_num = len(data)
    # 去重 -> 唯一ip
    data = list(set(data))
    host_nums = len(data)
    subnet_list = [host[1] for host in data]
    subnet_hostnum_dict = {}

    for subnet in list(set(subnet_list)):
        subnet_hostnum_dict[subnet] = subnet_list.count(subnet)


    print('data nums: ', data_num)
    print('host nums: ', host_nums)  # ip数量
    print('related subnet nums', len(subnet_hostnum_dict))
    print('host nums per subnet: ')
    for subnet, nums in subnet_hostnum_dict.items():
        print('- ', subnet, ':', nums)

    # data_num = len(data)

    # # 去重 -> 唯一ip
    # data = list(set(data))
    # host_nums = len(data)
    # # 唯一subnet
    # subnet_hostnum_dict = {}

    # for _, subnet in data:
    #     subnet_hostnum_dict[subnet] = subnet_hostnum_dict.get(subnet, 0) + 1


    # ip_list = []  # 用于去重
    # subnet_hostnum_dict = {}  # subnet: ip_nums
    # for ip, subnet in data:
    #     if ip not in ip_list:
    #         ori_num = subnet_hostnum_dict.get(subnet, 0)
    #         subnet_hostnum_dict[subnet] = ori_num + 1

    #         ip_list.append(ip)
"""


"""
my_list = [1, 2, 3, 2, 1, 2, 3, 1, 4, 2]
count_dict = {}

for item in my_list:
    if item in count_dict:  # keys
        count_dict[item] += 1
    else:
        count_dict[item] = 1

print(count_dict)


---
from collections import Counter

my_list = [1, 2, 3, 2, 1, 2, 3, 1, 4, 2]
count_dict = Counter(my_list)
print(count_dict)

"""
