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

	logger "LOG: Tasca afegida correctament"
elif [[ "$option" == "esborrar" ]]
then
	read web_ID
	varId=$(echo $web_ID | sed -e "s/web_ID=//g")
	varId=${varId::-1}

	sudo crontab -u root -l > ../tasques
	sudo sed -i.bak -e "${varId}d" ../tasques
	sudo crontab -u root ../tasques

	logger "LOG: Tasca esborrada correctament"
fi

readarray -t array < <(sudo crontab -u root -l | sed -e "s~*~‏‏‎* ~g")
out=""
for (( i=0; i<${#array[@]}; i++))
do
	out+="<tr><td>"$(echo "${array[i]}")"</td></tr>"
done

echo $(cat ../html/tasques.html | sed -e 's~{{codiHTML}}~'"$out"'~g')

