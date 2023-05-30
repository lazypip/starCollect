#!/usr/bin/python3

# 备份结果数据表

from sys import path
path.append(r"/home/ubuntu/Academic/starlink")

from sys import stdout, stderr, argv
from utility import *
from typing import *

from datetime import datetime

table_res = ['hostname', 'hostinfo', 'pro2']
table_mid = ['pro1']


def main():
    database = starlink_db()

    now = datetime.now()
    date_time = now.strftime("%Y%m%d_%H%M%S_")
    print("--- time:", date_time)
    # print("start backup database")

    for table in table_res:
        # 将现有的表重命名为 backup_
        # 复制表结构, 构造新表
        name = 'backup_' + date_time + table
        database.rename(table, name)
        database.table_struct_cp(name, table)

    for table in table_mid:
        # 清空此表即可, 无需备份
        database.clear(table)
    
    # print("backup database done")


if __name__ == "__main__":
    main()
