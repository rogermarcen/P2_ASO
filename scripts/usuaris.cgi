#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

read new_username
user=$(echo $new_username | sed -e "s/new_username=//g")
user=${user::-1}

read new_password
pass=$(echo $new_password | sed -e "s/new_password=//g")
pass=${pass::-1}

read web_option
option=$(echo $web_option | sed -e "s/web_option=//g")
option=${option::-1}

if [[ "$option" == "afegir" ]]
then
	if [[ "$user" != "" ]] && [[ "$pass" != "" ]]
	then
		sudo useradd $user
		echo -e "$pass\n$pass" | sudo passwd "$user"
		logger "LOG: Usuari creat correctament"
	else
		logger "LOG: Error creant usuari"
	fi
elif [[ "$option" == "esborrar" ]]
then
	#Comprovar que l'usuari existeix
	if id -u "$user" >/dev/null 2>&1
	then
		sudo userdel $user
		logger "LOG: Usuari esborrat correctament"
	else
		logger "LOG: Error esborrant usuari"
	fi
fi

echo $(cat ../html/menu.html)

