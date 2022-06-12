#!/bin/bash
echo 'Content-Type: text/html'
echo

#Llegim i guardem els valors entrats en el Login
read web_username
read web_password
user=$(echo $web_username | sed -e "s/web_username=//g")
pass=$(echo $web_password | sed -e "s/web_password=//g")
#Trec el \n del final
target=${user::-1}
pass=${pass::-1}
#Comprovo que l'usuari existeix
check=$(echo $pass | md5sum | sed -e "s~ -~~g")
succ=$(grep -c "$target $check" ../tmp/usr)
#Guardo la data actual
now=$(date +"%T")
varDate=$(date +"%d/%b/%Y")

if [ $succ -eq 1 ] then
    #Creo 2 estructures amb les diferents opocions possibles i el seu nivell de permisos
    varHide='style="visibility:hidden;"'
    varTargets=('class="procMang"')
    varPerms=("1")
    usrLvl=$(grep "$target" ../tmp/usr | awk '{print $3}')
    #Mostro per pantalla les opcions disponibles per el user loggejat
    out=$(cat ../html/menu.html | sed -e "s~{{user}}~$user~g")
    for (( i=0; i<${varTargets[@]}; i++))
    do
        if [ $usrLvl -gt ${varPerms[i]} ] then
            out=$(echo $out | sed -e "s~${varTargets[i]}~$varHide~g")
        fi
    done
    echo "$out"
#	logger -p local2.info "<<:$target $REMOTE_ADDR $now $varDate :>>login successful"
else
    echo $(cat ../html/index.html | sed -e "s/display:none;/display:initial;/g")
#   logger -p local2.info "<<:$target $REMOTE_ADDR $now $varDate :>>login unsuccessful"
fi