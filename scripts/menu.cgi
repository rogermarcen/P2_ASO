#!/bin/bash
echo 'Content-Type: text/html'
echo

#Guardem usuari actual
read new_user
user=$(echo $new_user | sed -e "s/new_user=//g")
user=${user::-1}
#Guardem la data actual
now=$(date +"%T")
varDate=$(date +"%d/%b/%Y")

#logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>went to menu"

#Mostro per pantalla les opcions disponibles per el user loggejat
echo $(cat ../html/menu.html | sed -e "s~{{user}}~$user~g")
