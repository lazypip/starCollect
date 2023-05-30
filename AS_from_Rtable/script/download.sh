#!/bin/bash

# 下载目标文件
# contrab
# $1 = raw roa

src_raw='https://thyme.apnic.net/current/data-raw-table'
src_roa='https://thyme.apnic.net/rpki/bgp.roas.ipv4'

target='src_'${1}
eval target='$'$target

run_path='/home/ubuntu/Academic/starlink/AS_from_Rtable'
cd $run_path

if [ $# -ne 1 ];then
    exit 1
fi

# echo 'downloading '
rm -f ${1}

wget_ret=1
retry=0

while [ $wget_ret -ne 0 ]
do
    wget -q -O ./${1} $target
    wget_ret=$?
    retry=`expr $retry + 1`
    
    if [ $retry -eq 5 ];then
        echo ${1}-`date`-'fail' >> download.log
        exit 1
    fi
done
