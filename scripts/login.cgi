#!/bin/bash
echo 'Content-Type: text/html'
echo

#Llegim i guardem els valors entrats en el html de Login
read web_username
read web_password
user=$(echo $web_username | sed -e "s/web_username=//g")
pass=$(echo $web_password | sed -e "s/web_password=//g")
#Trec el \n del final
user=${user::-1}
pass=${pass::-1}
#Comprovo que l'usuari existeixi


#Guardo la data actual
hour=$(date + "%T")
date=$(date + "%d/%b/%Y")

#if [$flag_ok -eq 1] then
	#Mostro al html les opcions segons els permisos
	echo $(cat ../html/menu.html | sed -e "s~{{user}}~$user~g")
	#Falta fer el logg
#else
#	echo $(cat ../html/index.html | sed -e "s/display:none;/display:initial;/g")
#fi
