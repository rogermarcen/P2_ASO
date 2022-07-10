#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

logger "LOG: Usuari ha entrat a l'opcio monitor"

cpu="CPU: "$(grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage "%"}')
mem=$(free -m | awk 'NR==2{printf "Memòria: %s/%sMB (%.2f%%)\n", $3,$2,$3*100/$2 }')
disk=$(df -h | awk '$NF=="/"{printf "Disk: %d/%dGB (%s)\n", $3,$2,$5}')

readarray -t array < <(sudo cat var/log/apache2/access.log | tail -10)
#readarray -t array < <(ps aux)
#declare -p array
out=""

for ((i=0; i<${#array[@]}; i++))
do
	curr=(${array[i]})
	currTime=${curr[3]}
	currTime=${currTime#*:}
	currDate=${curr[3]}
	currDate=${currDate:1}
	currDate=${currDate%%:*}
	currDevice=${my_array[i]}
	currDevice=${currDevice#*(}
	currDevice=${currDevice%%;*}
	out+="<tr> <td>"$(echo ${array[i]})"</td></tr>"
#	out+="<tr> <td>"$(echo $currTime)"</td><td>"$(echo $currDate)"</td><td>"$(echo ${curr[0]})"</td><td>"$(echo $currDevice)"</td> </tr>"
done
echo $(cat ../html/monitor.html | sed -e "s~{cpu}~$cpu~g" | sed -e "s~{mem}~$mem~g" | sed -e "s~{disk}~$disk~g" | sed -e "s~{{codiHTML}}~$out~g")
