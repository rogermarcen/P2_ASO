#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

logger "LOG: Usuari entra opcio ACLs"

read web_option
option=$(echo $web_option | sed -e "s/web_option=//g")
option=${option::-1}

if [[ "$option" == "modificar" ]]
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

	read web_id
        id=$(echo $web_id | sed -e "s/web_id=//g")
        id=${id::-1}

        #ACCEPT/DENY
        read web_tipo
        tipo=$(echo $web_tipo | sed -e "s/web_tipo=//g")
        tipo=${tipo::-1}

        #ADD/DELETE
        read web_estat
        estat=$(echo $web_estat | sed -e "s/web_estat=//g")
        estat=${estat::-1}

	#INPUT/OUTPUT/FORWARD
	read web_direccio
	direccio=$(echo $web_direccio | sed -e "s/web_direccio=//g")
	direccio=${direccio::-1}

	if [[ "$direccio" == "" ]] || [[ "$estat" == "" ]]
        then
		logger "LOG: Error al intentar modificar ACLs"
		break
	fi

	if [[ "$estat" == "add" ]]
	then
		if [[ "$tipo" == "" ]]
		then
			logger -p local2.info "LOG: Error al intentar modificar ACLs"
			break
		fi

		comanda="sudo iptables -A $direccio"

		if [[ "$protocol" != "" ]]
                then
                        comanda+=" -p $protocol"
                else
                        comanda+=" -p all"
                fi

		if [[ "$IPorigen" != "" ]]
		then
			comanda+=" -s $IPorigen"
		fi

		if [[ "$IPdesti" != "" ]]
		then
			comanda+=" -d $IPdesti"
		fi

		if [[ "$port" != "" ]]
		then
			comanda+=" --dport $port"
		fi

		comanda+=" -j $tipo"

		bash -c "$comanda"
		logger "LOG: ACL modificada correctament"
	elif [[ "$estat" == "del" ]]
        then
		sudo iptables -D $direccio $id
		logger "LOG: ACL esborrada correctament"
	fi
fi

readarray -t in_array < <(sudo iptables -L INPUT --line-numbers)
readarray -t frw_array < <(sudo iptables -L FORWARD --line-numbers)
readarray -t out_array < <(sudo iptables -L OUTPUT --line-numbers)

aclsInput=""
for (( i=2; i<${#in_array[@]}; i++))
do
	aclsInput+="<tr><td>"$(echo ${in_array[i]})"</td></tr>"
done

aclsForward=""
for (( i=2; i<${#frw_array[@]}; i++))
do
	aclsForward+="<tr><td>"$(echo ${frw_array[i]})"</td></tr>"
done

aclsOut=""
for (( i=2; i<${#out_array[@]}; i++))
do
	aclsOut+="<tr><td>"$(echo ${out_array[i]})"</td></tr>"
done


echo $(cat ../html/acls.html | sed -e 's~{{codiHTML}}~'"$aclsInput"'~g' | sed -e 's~{{codiHTML2}}~'"$aclsForward"'~g' | sed -e 's~{{codiHTML3}}~'"$aclsOut"'~g')

