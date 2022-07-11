#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

logger "LOG: Usuari entra opcio musica"

read web_option
option=$(echo $web_option | sed -e "s/web_option=//g")
option=${option::-1}

read web_id
id=$(echo $web_id | sed -e "s/web_id=//g")
id=${id::-1}

read web_aleatori
aleatori=$(echo $web_aleatori | sed -e "s/web_aleatori=//g")
aleatori=${aleatori::-1}

read web_repetir
repetir=$(echo $web_repetir | sed -e "s/web_repetir=//g")
repetir=${repetir::-1}

read web_estat
estat=$(echo $web_estat | sed -e "s/web_estat=//g")
estat=${estat::-1}

readarray -t array < <(ls -1 ../music)

if [[ "$option" == "aleatori" ]]
then
	if [[ "$aleatori" == "1" ]]
	then
		aleatori="0"
	else
		aleatori="1"
	fi
	logger "LOG: Opcio musica aleatoria"
elif [[ "$option" == "repetir" ]]
then
	if [[ "$repetir" == "1" ]]
        then
                repetir="0"
        else
                repetir="1"
        fi
	logger "LOG: Opcio musica repetir"
elif [[ "$option" == "anterior" ]]
then
	if [[ "$repetir" == "0" ]]
        then
                if [[ "$aleatori" == "1" ]]
	        then
	                id=$(echo $(($RANDOM % ${#array[@]})))
	        else
	                id=$(($id - 1))
			if [[ "$id" == "-1" ]]
			then
				id=$((${#array[@]} - 1))
			fi
	        fi
        fi
	sudo pkill mpg123
#	echo "mpg123 /var/www/music/${array[id]}"
	sudo mpg123 /var/www/music/${array[id]}
	estat="1"
	logger "LOG: Opcio musica anterior"
elif [[ "$option" == "seguent" ]]
then
        if [[ "$repetir" == "0" ]]
        then
                if [[ "$aleatori" == "1" ]]
                then
                        id=$(echo $(($RANDOM % ${#array[@]})))
                else
                        id=$(($id + 1))
                        if [[ "$id" == "${#array[@]}" ]]
                        then
                                id="0"
                        fi
                fi
        fi
        sudo pkill mpg123
#	echo "mpg123 /var/www/music/${array[id]}"
        sudo mpg123 /var/www/music/${array[id]}
	varState="1"
	logger "LOG: Opcio musica seguent"
elif [[ "$option" == "pause" ]]
then
	if [[ "$estat" == "1" ]]
	then
		sudo echo " "
		estat="0"
	fi
	logger "LOG: Opcio musica pause"
elif [[ "$option" == "play" ]]
then
	sudo pkill mpg123
        sudo mpg123 /var/www/music/${array[id]}
	estat="1"
	logger "LOG: Opcio musica play"
fi

out=""
for (( i=0; i<${#array[@]}; i++))
do
        out+="<tr"
	if [[ "$i" == "$id" ]]
	then
		out+=' class="selected"'
	fi
	out+="> <td>"$(echo ${array[i]})"</td> </tr>"
done

echo $(cat ../html/musica.html | sed -e 's~{{codiHTML}}~'"$out"'~g' | sed -e "s~{{id}}~$id~g" | sed -e "s~{{aleatori}}~$aleatori~g" | sed -e "s~{{repetir}}~$repetir~g" | sed -e "s~{{estat]}~$estat~g")
