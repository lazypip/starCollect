#!/bin/bash


# echo '- bgp.he.net'


# source ./token
if [ ! $token_ipinfo ]; then
        echo 'no token env'
        echo -e 'usage: source ./token \n./starCollect'
        exit 1
fi


# 数据合并与去重
src_list=(bgpHE ipinfo Rtable)
asn_list=(14593 14597 36492)

# 扩展as ip并去重上传
dir='AS_from_'
for asn in ${asn_list[@]}
do
    for src in ${src_list[@]}
    do
        cat ../${dir}${src}/res/*${asn} | python3 s_1.py ${src} ${asn}
    done
done
echo "-- successfully AS data from starlink"


# echo 'step2 - geoip'
dir='geoip_from_starlink'
cat ../${dir}/res/* | python3 s_2.py
echo "-- successfully geoip from starlink"


# echo 'step3 - table pro1 -> pro2'
python3 s_3.py
echo "-- successfully pull pro1 to pro2"
