#!/usr/bin/python3

# 将所有hostname 去重集合于 hostname数据表并填充标识
# 数据来源: pro2与hostname/res目录
# 只提取与starlink相关的starlinkisp.net与undefined...
# cat ../hostname/res/hostname* | python3 -u hostinfo.py


from sys import path
path.append(r"/home/ubuntu/Academic/starlink")

from utility import *
from typing import *


def read_stdin() -> List:
    """ """
    res = []
    while True:
        try:
            text = input()
            hostname = text.split(' ')[1]
            res.append(hostname)
        except:
            break
    
    res = list(set(res))
    try:
        res.remove(None)
    except:
        pass
    
    return res


def read_pro2(database: starlink_db, table='pro2'):
    """ 
    null数据返回 None

    """
    query = "SELECT hostname from {}".format(table)
    res = database.select(query)

    res = [ele[0] for ele in res]
    res = list(set(res))
    try:
        res.remove('')
        res.remove(None)
    except:
        pass

    return res


def parse(hostname) -> str:
    """
    
    """

    if 'customer' in hostname:
        if 'mc' in hostname:
            return 'customer-mc'
        if 'pop' in hostname:
            return 'customer-pop'
    
    if 'undefined' in hostname:
        return 'undefined'
    
    return ''


def upload(hostname, id, database: starlink_db, table='hostname'):
    """ """
    query_base = "INSERT IGNORE into {} \
        (identifier, hostname) values \
        ('{}', '{}')"
    query = query_base.format(table, id, hostname)

    try:
        database.insert(query)
    except:
        print(query)
        # 继续运行，抛弃错误数据
        # exit(1)


def main():
    database = starlink_db()

    stdin_list = read_stdin()
    pro2_list = read_pro2(database)

    hostnames = stdin_list + pro2_list
    hostnames = list(set(hostnames))

    print('--- num of hostnames:', len(hostnames))

    hostname = 'undefined.hostname.localhost'
    id = parse(hostname)
    upload(hostname, id ,database)

    for hostname in hostnames:
        id = parse(hostname)
        upload(hostname, id ,database)


if __name__ == "__main__":
    main()
