

"""
## Note: 
1. 创建对象怎么可能返回一个值, 析构只有类支持吗? - 面向对象
2. 可变参数与@..方法
3. 注意加入类型审核
4. 类中的函数不带self,就无法用self访问
5. http请求, 数据读写, 字典字段解析等高概率出错[理应]带异常处理 找下参考
6. subprocess的原理
"""


import requests

from sys import stdout, stderr, path
import subprocess
from os import environ

import json
from typing import *


ipinfo_token = environ.get('token_ipinfo_free')
if not ipinfo_token:  # None
    print("warning: better usage: source token")
    ipinfo_token = ''


def request_ipinfo_json(target: str):
    url = 'http://ipinfo.io/{}?token=' + ipinfo_token

    try:
        res = requests.get(url.format(target))
        res = res.json()
        return res
    except:
        return None


def parse_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    return data

# ----------------------------------------------

def dig_ip(ipList: List) -> List:
    """ 通过dig反查ip的域名

    ret:
        未查找到ip返回None
        
    """
    res = []
    for ip in ipList:
        domain = subprocess.run(
            ['dig', '-x', ip, '+short'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        domain = domain.stdout

        # 无结果
        if len(domain) < 5:  # .与换行符
            res.append(None)
            continue
        
        # 保留 undefined.hostname.localhost
        domain = domain[:-2]
        res.append(domain)
    
    return res


def stdin_to_list() -> List:
    """ 将stdin的数据转化为List, 以换行符分隔
    与直接使用stdin一样, 均存储在内存中
    
    """
    res = []
    while True:
        try:
            text = input()
            res.append(text)
        except:
            break
    
    return res

if __name__ == "__main__":
    # test
    # print(dig_ip(['8.8.8.8', '1.2.3.4']))
    pass
