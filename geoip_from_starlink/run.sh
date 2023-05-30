#!/bin/bash

# TODO: 自动处理wget报错(频繁请求会不响应)


echo '- geoip from starlink'


time=`date -u +%m-%dT%H-%M%S`
file='geoip'
file_ipv4='geoipv4'
res='geoip_ipv4'


# 数据获取与备份
mkdir backup/${time}
wget -q -O ${file} https://geoip.starlinkisp.net/feed.csv
wget_ret=$?

if [ $wget_ret -ne 0 ];then
    echo "wget error - ${wget_ret}" ; exit 1
fi
cp ${file} backup/${time}

echo '-- successfully download'


# 提取ipv4, 通过判断ipv6 分号的行数
echo '-- extract ipv4'
tmp=`cat $file | grep ':' -n | head -n 1`
tmp1=${tmp:0:4}
line=`expr $tmp1 - 1`

cat $file | head -n $line > $file_ipv4
rm $file


# format
cat $file_ipv4 | python3 script/format.py > res/$res
rm $file_ipv4

echo '-- successfully format'
echo '-- end'
