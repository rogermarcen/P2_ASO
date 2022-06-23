#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

#Agafo l'usuari actual i la data
read web_user
user=$(echo $web_user | sed -e "s/web_user=//g")
user=${user::-1}
now=$(date +"%T")
varDate=$(date +"%d/%b/%Y")

#logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>started monitoring"

cpu="CPU: "$(grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage "%"}')
mem=$(free -m | awk 'NR==2{printf "Memòria: %s/%sMB (%.2f%%)\n", $3,$2,$3*100/$2 }')
disk=$(df -h | awk '$NF=="/"{printf "Disk: %d/%dGB (%s)\n", $3,$2,$5}')
readarray -t my_array < <(sudo cat /var/log/apache2/access.log | grep "POST /scripts/login.cgi" | tail -10)

out=""
for (( i=0; i<${#my_array[@]}; i++)) do
    curr=(${my_array[i]})
	currTime=${curr[3]}
	currTime=${currTime#*:}
	currDate=${curr[3]}
	currDate=${currDate:1}
	currDate=${currDate%%:*}
	currDevice=${my_array[i]}
	currDevice=${currDevice#*(}
	currDevice=${currDevice%%;*}
	out+="<tr> <td>"$(echo $currTime)"</td><td>"$(echo $currDate)"</td><td>"$(echo ${curr[0]})"</td><td>"$(echo $currDevice)"</td> </tr>"
done
echo $(cat ../html/monitor.html | sed -e "s~{cpu}~$cpu~g" | sed -e "s~{mem}~$mem~g" | sed -e "s~{disk}~$disk~g" | sed -e "s~{{codiHTML}}~$out~g" | sed -e "s~{{user}}~$user~g")

