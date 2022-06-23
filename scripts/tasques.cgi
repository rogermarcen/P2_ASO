#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

read web_user
user=$(echo $web_user | sed -e "s/web_user=//g")
user=${user::-1}
now=$(date +"%T")
varDate=$(date +"%d/%b/%Y")

read web_option
tmp=$(echo $web_option | sed -e "s/web_option=//g")
option=${tmp::-1}

#logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>Opened programmed tasks"

if [[ "$option" == "afegir" ]]
then
	read new_min
	varMin=$(echo $new_min | sed -e "s/new_min=//g")
	varMin=${varMin::-1}

	read new_hora
    varHour=$(echo $new_hora | sed -e "s/new_hora=//g")
    varHour=${varHour::-1}

	read new_dia
    varDay=$(echo $new_dia | sed -e "s/new_dia=//g")
    varDay=${varDay::-1}

	read new_mes
    varMonth=$(echo $new_mes | sed -e "s/new_mes=//g")
    varMonth=${varMonth::-1}

	read new_any
    varWday=$(echo $new_any | sed -e "s/new_any=//g")
    varWday=${varWday::-1}

	read new_comanda
    varPath=$(echo $new_comanda | sed -e "s/new_comanda=//g")
    varPath=${varPath::-1}

	sudo crontab -u root -l > ../tasques
	echo "$varMin $varHour $varDay $varMonth $varWday $varPath" >> ../tasques
	sudo crontab -u root ../tasques

#	logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>Added a programmed task"
elif [[ "$option" == "esborrar" ]]
then
	read web_ID
    varId=$(echo $web_ID | sed -e "s/web_ID=//g")
    varId=${varId::-1}

	sudo crontab -u root -l > ../tasques
	sudo sed -i.bak -e "${varId}d" ../tasques
	sudo crontab -u root ../tasques

#	logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>Removed programmed task"
fi

#logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>loaded proccesses"
readarray -t my_array < <(sudo crontab -u root -l | sed -e "s~*~‏‏‎* ~g")
out=""
for (( i=0; i<${#my_array[@]}; i++))
do
	aux=(${my_array[i]})
	#out+="<tr> <td>"$(($i + 1))"</td><td>"$(echo "${aux[*]}")"</td></tr>"
	out+="<tr> <td>"$(($i + 1))"</td><td>"$(echo "${aux[0]}")"</td><td>"$(echo "${aux[1]}")"</td><td>"$(echo "${aux[2]}")"</td><td>"$(echo "${aux[3]}")"</td><td>"$(echo "${aux[4]}")"</td><td>"$(echo "${aux[5]}")"</td> </tr>"
done

echo $(cat ../html/tasques.html | sed -e 's~{{codiHTML}}~'"$out"'~g' | sed -e "s~{{user}}~$user~g")

