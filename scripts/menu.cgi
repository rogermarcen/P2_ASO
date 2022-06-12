#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

#Guardem usuari actual
read POSTuser
user=$(echo $POSTuser | sed -e "s/POSTuser=//g")
user=${user::-1}
#Guardem la data actual
now=$(date +"%T")
varDate=$(date +"%d/%b/%Y")

#logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>went to menu"

#Creo 2 estructures amb les diferents opocions possibles i el seu nivell de permisos
varHide='style="visibility:hidden;"'
varTargets=('class="procMang"')
varPerms=("1")
usrLvl=$(grep "$user" ../tmp/usr | awk '{print $3}')

#Mostro per pantalla les opcions disponibles per el user loggejat
out=$(cat ../html/menu.html | sed -e "s~{{user}}~$user~g")
for (( i=0; i<${varTargets[@]}; i++))
do
	if [ $usrLvl -gt ${varPerms[i]} ] then
        out=$(echo $out | sed -e "s~${varTargets[i]}~$varHide~g")
	fi
done

echo "$out"
