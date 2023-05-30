#!/bin/bash

# banner
echo '- data lookup'

# source ./token
if [ ! $token_ipinfo ]; then
        echo 'no token env'
        echo -e 'usage: source ./token \n./starCollect'
        exit 1
fi


python3 -u pro2_host_loc.py
echo "-- successfully lookup hostname and location"


# 一部分来源在hostname文件夹
cat ../hostname/res/hostname* | python3 -u hostname.py
echo '-- successfully parse hostname'

# 每个主机的扫描结果
python3 -u hostinfo.py
echo '-- successfully shodan scan'

# 填充每个ip对应的identifier
python3 -u identifier.py
echo '-- successfully fill in identifier'
