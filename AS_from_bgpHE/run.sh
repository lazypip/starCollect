#!/bin/bash

# banner
echo '- bgp.he.net'


time=`date -u +%m-%dT%H-%M%S`
as_list=(14593 36492 14597)
retry=3

# echo 'start download and backup'
# TODO: 异常处理优化
mkdir backup/${time}
for as in ${as_list[@]}
do
    line_num=5
    retry_t=0
    while [ $line_num -gt 3 ]; do
        retry_t=`expr $retry_t + 1`
        if [ $retry_t -gt $retry ]; then echo > ${as}; echo "-- ${as} fail"; fi

        # 自动覆盖
        wget -q -O ${as} https://rt-bgp.he.net/api/v1/as/${as}/originated
        
        line_num=`wc -l < ${as}`
        sleep 3
    done

    cp ${as} backup/${time}
done
echo '-- successfully download'


# echo 'start format'
for as in ${as_list[@]}
do
    cat ${as} | jq '.ipv4' | grep '/' | python3 script/format.py > res/bgphe_${as}
    rm ${as}
done
echo '-- successfully format'
echo '-- end'
