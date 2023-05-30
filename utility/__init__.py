"""
TODO: 回顾__init__.py的作用, 注意相对路径

from sys import path
path.append(r"/home/ubuntu/Academic/starlink")

将utility看作一个包
"""

from .util import (
    request_ipinfo_json,
    parse_json,
    dig_ip
)

from .starlink_sql import (
    starlink_db,
    test
)
