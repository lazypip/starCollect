#!/bin/bash

# backup与format
# format暂时不考虑roa文件 raw

echo '- routing table'


time=`date -u +%m-%dT%H-%M%S`
as_list=(14593 36492 14597)
src_raw='raw'
src_roa='roa'
res_raw='routingTable'


if [ ! -f $src_raw ]; then
    echo '-- '${src_raw}' not exist'
    exit 1
fi


mkdir backup/${time}
for as in ${as_list[@]}
do
    cat $src_raw | grep ${as} > ${as}
done
cp ${src_raw} ${src_roa} backup/${time}

echo '-- successfully download'


rm -rf res/*
for as in ${as_list[@]}
do
    cat ${as} | python3 script/format_raw.py > res/${res_raw}_${as}
    rm ${as}
done

echo '-- successfully format'
echo '-- end'
