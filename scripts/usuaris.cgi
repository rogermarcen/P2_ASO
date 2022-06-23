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
option=$(echo $web_option | sed -e "s/web_option=//g")
option=${option::-1}

if [[ "$option" == "afegir" ]]
then
	read new_user
	varUsr=$(echo $new_user | sed -e "s/new_user=//g")
	varUsr=${varUsr::-1}

	read new_password
    varPas=$(echo $new_password | sed -e "s/new_password=//g")
    varPas=${varPas::-1}

	if [[ "$varUsr" != "" ]] && [[ "$varPas" != "" ]]
	then
		sudo useradd $varUsr
		echo -e "$varPas\n$varPas" | sudo passwd "$varUsr"
#		logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>Added user $varUsr"
	fi
elif [[ "$option" == "esborrar" ]]
then
	read new_user
    varUsr=$(echo $new_user | sed -e "s/new_user=//g")
    varUsr=${varUsr::-1}
	sudo userdel $varUsr

#	logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>Deleted usr $varUsr"
fi

echo $(cat ../html/menu.html | sed -e "s~{{user}}~$user~g")

