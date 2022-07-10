#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

logger "LOG: Usuari ha entrat opcio mostrar LOGs"

readarray -t array < <(sudo cat /var/log/syslog | grep LOG)
out=""
#declare -p array

for (( i=1; i<${#array[@]}; i++)) 
do
    out+="<tr> <td>"$(echo ${array[i]})"</td> </tr>"
done
echo $(cat ../html/logs.html | sed -e 's~{{codiHTML}}~'"$out"'~g')
