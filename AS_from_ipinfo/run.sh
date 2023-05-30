#!/bin/bash

# banner
echo '- ipinfo'


token=$token_ipinfo
time=`date -u +%m-%dT%H-%M%S`
as_list=(14593 36492 14597)


# 获取json文件并备份
mkdir backup/${time}
for as in ${as_list[@]}
do
	curl -s -o ${as} "https://ipinfo.io/AS${as}?token=${token}"
	line_num=`wc -l < ${as}`
	if [ $line_num -lt 5 ]; then
		echo '-- token is invalid'
		rm ${as}
		exit 1
	fi

	cp ${as} backup/${time}
done
echo '-- successfully download'


# format id, ip, prefix
for as in ${as_list[@]}
do
	jq .prefixes < ${as} | grep 'netblock' | python3 script/format.py > res/ipinfo_${as}
	rm ${as}
done

echo '-- successfully format'
echo '-- end'
