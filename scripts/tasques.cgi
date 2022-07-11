#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

read web_option
tmp=$(echo $web_option | sed -e "s/web_option=//g")
option=${tmp::-1}

logger "LOG: Usuari entre opcio tasques"

if [[ "$option" == "afegir" ]]
then
	read new_min
	min=$(echo $new_min | sed -e "s/new_min=//g")
	min=${min::-1}

	read new_hora
    	hora=$(echo $new_hora | sed -e "s/new_hora=//g")
    	hora=${hora::-1}

	read new_dia
	 dia=$(echo $new_dia | sed -e "s/new_dia=//g")
	 dia=${dia::-1}

	read new_mes
	mes=$(echo $new_mes | sed -e "s/new_mes=//g")
	mes=${mes::-1}

	read new_diaSet
	diaSet=$(echo $new_diaSet | sed -e "s/new_diaSet=//g")
	diaSet=${diaSet::-1}

	read new_comanda
	comanda=$(echo $new_comanda | sed -e "s/new_comanda=//g")
	comanda=${comanda::-1}

	sudo crontab -u root -l > cron
	echo "$min $hora $dia $mes $diaSet $comanda" >> cron
	sudo crontab -u root cron

	logger "LOG: Tasca afegida correctament"
elif [[ "$option" == "esborrar" ]]
then
	read web_ID
	id=$(echo $web_ID | sed -e "s/web_ID=//g")
	id=${id::-1}

	sudo crontab -u root -l > cron
	sudo sed $id,$id"d" cron >> cronbckp
	sudo rm cron
	sudo cp cronbckp cron
	sudo rm cronbckp
	sudo crontab -u root cron

	logger "LOG: Tasca esborrada correctament"
fi

readarray -t array < <(sudo crontab -u root -l | sed -e "s~*~‏‏‎* ~g")
out=""
for (( i=0; i<${#array[@]}; i++))
do
	out+="<tr><td>"$(echo "${array[i]}")"</td></tr>"
done

echo $(cat ../html/tasques.html | sed -e 's~{{codiHTML}}~'"$out"'~g')

