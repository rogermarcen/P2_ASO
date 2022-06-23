#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

read web_user
user=$(echo $web_user | sed -e "s/web_user=//g")
user=${user::-1}
now=$(date +"%T")
varDate=$(date +"%d/%b/%Y")

#logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>requested unmodified log"
readarray -t my_array < <(sudo tail -10 /var/log/apserver.log)
out=""
for (( i=0; i<${#my_array[@]}; i++)) do
    curr=(${my_array[i]#*<<:})
    msg=${my_array[i]}
    msg=${msg#*:>>}
    out+="<tr> <td>"$(echo ${curr[0]})"</td><td>"$(echo ${curr[1]})"</td><td>"$(echo ${curr[2]})"</td><td>"$(echo ${curr[3]})"</td><td>"$(echo $msg)"</td> </tr>"
done
readarray -t serv_array < <(sudo tail /var/log/apache2/access.log)
out2=""
for (( i=0; i<${#serv_array[@]}; i++)) do
    out2+="<tr> <td>"$(echo ${serv_array[i]%%(*})"</td> </tr>"
done
echo $(cat ../html/logs.html | sed -e 's~{{codiHTML}}~'"$out"'~g' | sed -e "s~{{user}}~$user~g" | sed -e 's~{{codiHTML2}}~'"$out2"'~g')