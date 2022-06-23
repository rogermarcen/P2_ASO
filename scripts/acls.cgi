#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

read web_user
user=$(echo $web_user | sed -e "s/web_user=//g")
user=${user::-1}
now=$(date +"%T")
varDate=$(date +"%d/%b/%Y")
#logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>Packet Filter Loaded"

read web_option
option=$(echo $web_option | sed -e "s/web_option=//g")
option=${option::-1}

if [[ "$option" == "modificar" ]]
then
	#INPUT/OUTPUT/FORWARD
	read web_direccio
	direccio=$(echo $web_direccio | sed -e "s/web_direccio=//g")
	direccio=${direccio::-1}

	#ADD/DELETE
	read web_estat
	estat=$(echo $web_estat | sed -e "s/web_estat=//g")
	estat=${estat::-1}

	if [[ "$direccio" == "" ]] || [[ "$estat" == "" ]]
        then
#		logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>Filter Error"
		break
	fi

	if [[ "$estat" == "add" ]]
	then
		read web_IPorigen
		IPorigen=$(echo $web_IPorigen | sed -e "s/web_IPorigen=//g")
		IPorigen=${IPorigen::-1}

		read web_IPdesti
		IPdesti=$(echo $web_IPdesti | sed -e "s/web_IPdesti=//g")
		IPdesti=${IPdesti::-1}

		read web_port
		port=$(echo $web_port | sed -e "s/web_port=//g")
		port=${port::-1}

		read web_protocol
		protocol=$(echo $web_protocol | sed -e "s/web_protocol=//g")
		protocol=${protocol::-1}

		#ACCEPT/DENY
		read web_tipo
		tipo=$(echo $web_tipo | sed -e "s/web_tipo=//g")
		tipo=${tipo::-1}

		if [[ "$tipo" == "" ]]
		then
#			logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>Accept or Drop were not selected"
			break
		fi

		comanda="sudo iptables -A $direccio"

		if [[ "$IPorigen" != "" ]]
		then
			comanda+=" -s $IPorigen"
		fi

		if [[ "$IPdesti" != "" ]]
		then
			comanda+=" -d $IPdesti"
		fi

		if [[ "$protocol" != "" ]]
		then
			comanda+=" -p $protocol"
		else
			comanda+=" -p all"
		fi

		if [[ "$port" != "" ]]
		then
			comanda+=" --dport $port"
		fi

		comanda+=" -j $tipo"

		bash -c "$comanda"
#		logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>Added or modified an ip filter"
	elif [[ "$estat" == "del" ]]
        then
		sudo iptables -D $direccio $varId
#		logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>Deleted ip filter"
	fi
fi

readarray -t in_array < <(sudo iptables -L INPUT --line-numbers)
readarray -t frw_array < <(sudo iptables -L FORWARD --line-numbers)
readarray -t out_array < <(sudo iptables -L OUTPUT --line-numbers)

aclsInput=""
for (( i=2; i<${#in_array[@]}; i++))
do
	aux=(${in_array[i]})
	aclsInput+="<tr> <td>"$(echo ${aux[1]})"</td><td>"$(echo ${aux[2]})"</td><td>"$(echo ${aux[4]})"</td><td>"$(echo ${aux[5]})"</td> </tr>"
done

aclsForward=""
for (( i=2; i<${#frw_array[@]}; i++))
do
	aux=(${frw_array[i]})
	aclsForward+="<tr> <td>"$(echo ${aux[1]})"</td><td>"$(echo ${aux[2]})"</td><td>"$(echo ${aux[4]})"</td><td>"$(echo ${aux[5]})"</td> </tr>"
done

aclsOut=""
for (( i=2; i<${#out_array[@]}; i++))
do
	aux=(${out_array[i]})
	aclsOut+="<tr> <td>"$(echo ${aux[1]})"</td><td>"$(echo ${aux[2]})"</td><td>"$(echo ${aux[4]})"</td><td>"$(echo ${aux[5]})"</td> </tr>"
done


echo $(cat ../html/acls.html | sed -e 's~{{codiHTML}}~'"$aclsInput"'~g' | sed -e 's~{{codiHTML2}}~'"$aclsForward"'~g' | sed -e 's~{{codiHTML3}}~'"$aclsOut"'~g' | sed -e "s~{{user}}~$user~g")

