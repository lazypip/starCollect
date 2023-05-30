#!/bin/bash

# todo: zoomeye错误重传


echo '- hostname collection'


time=`date -u +%m-%dT%H-%M%S`
mkdir backup/${time}


# zoomeye
page=1
end=1
file1='zoomeye'
res1='hostname_zoomeye'
echo '' > $file1

while [ $end -eq 1 ];
do
    count=`curl -s -X GET \
    "https://api.zoomeye.org/domain/search?q=starlinkisp.net&type=1&page=${page}" \
    -H "API-KEY:5137A4C1-e284-52067-a649-2106cfd02e7" | jq \
    | tee >(grep 'name' | wc -l) >>$file1`
    
    if [ $count -lt 30 ]; then end=0; fi
    page=`expr $page + 1`
    # sleep 1
done
echo '-- zoomeye successfully download'

cp $file1 backup/${time}
cat $file1 | grep 'name' | python3 script/format_zoomeye.py > res/$res1
rm $file1
echo '-- zoomeye successfully format'


# theHarvester
# 【需要代理】，暂时以 /backup/theHarvester为数据来源
file2='theHarvester'
res2='hostname_theHarvester'
echo '-- theHarvester successfully download'

cat backup/$file2 | grep 'starlinkisp.net' | python3 script/format_theHarvester.py > res/$res2
echo '-- theHarvester successfully format'

# shodan
file3='shodan'
res3='hostname_shodan'

python3 script/collect_shodan.py > $file3
cp $file3 backup/${time}
echo '-- shodan successfully download'

cat $file3 | python3 script/format_shodan.py > res/$res3
rm $file3
echo '-- shodan successfully format'


# ipinfo
file4='ipinfo'
res4='hostname_ipinfo'

curl -s -o $file4 "https://ipinfo.io/ranges/starlinkisp.net?token=${token_ipinfo}"
cp $file4 backup/${time}
echo '-- ipinfo successfully download'

cat $file4 | grep '/' | grep -v ':'| python3 script/format_ipinfo.py > res/$res4
rm $file4
echo '-- ipinfo successfully format'
