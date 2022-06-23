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

read web_option
option=$(echo $web_option | sed -e "s/web_option=//g")
option=${option::-1}

read web_pid
aux=$(echo $web_pid | sed -e "s/web_pid=//g")
declare -i pid=${aux::-1}

read web_time
aux=$(echo $web_time | sed -e "s/web_time=//g")
declare -i temps=${aux::-1}

if [[ "$option" == "matar" ]]
then
	sudo kill -9 $pid
#	logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>killed proccess $varPid"
elif [[ "$option" == "matarTemps" ]]
then
	sudo kill -STOP $pid
	(sleep $temps; sudo kill -CONT $temps) &
#	logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>paused proccess $varPid for $varTime seconds"
fi

#logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>loaded proccesses"
readarray -t array < <(ps aux)
out=""
for (( i=1; i<${#array[@]}; i++))
do
	aux=(${array[i]})
	out+="<tr> <td>"$(echo ${aux[1]})"</td><td>"$(echo ${aux[0]})"</td><td>"$(echo ${aux[7]})"</td><td>"$(echo ${aux[10]})"</td> </tr>"
done

echo $(cat ../html/processos.html | sed -e 's~{{codiHTML}}~'"$out"'~g' | sed -e "s~{{user}}~$user~g")


