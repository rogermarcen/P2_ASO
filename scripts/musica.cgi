#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

logger "LOG: Usuari entra opcio musica"

read web_option
option=$(echo $web_option | sed -e "s/web_option=//g")
option=${option::-1}

mypipe='/var/www/cmdMusic'

#read meta file to figure out current state
songNum=$(sed '1q;d' ../metaMusic)
varShuf=$(sed '2q;d' ../metaMusic | sed -e "s/1://g")
varRep=$(sed '3q;d' ../metaMusic | sed -e "s/2://g")
varState=$(sed '4q;d' ../metaMusic | sed -e "s/3://g")

readarray -t array < <(ls -1 ../music)

if [[ "$option" == "aleatori" ]]
then
	if [[ "$varShuf" == "ON" ]]
	then
		varShuf="OFF"
	else
		varShuf="ON"
	fi
	logger "LOG: Opcio musica aleatoria"
elif [[ "$option" == "repetir" ]]
then
	if [[ "$varRep" == "ON" ]]
        then
                varRep="OFF"
        else
                varRep="ON"
        fi
	logger "LOG: Opcio musica repetir"
elif [[ "$option" == "anterior" ]]
then
	if [[ "$varRep" == "OFF" ]]
        then
                if [[ "$varShuf" == "ON" ]]
	        then
	                songNum=$(echo $(($RANDOM % ${#array[@]})))
	        else
	                songNum=$(($songNum - 1))
			if [[ "$songNum" == "-1" ]]
			then
				songNum=$((${#array[@]} - 1))
			fi
	        fi

        fi
	#Play songNum
	sudo echo "load /var/www/music/${array[$songNum]}" >> "$mypipe"
	varState="PLAY"
	logger "LOG: Opcio musica anterior"
elif [[ "$option" == "seguent" ]]
then
        if [[ "$varRep" == "OFF" ]]
        then
                if [[ "$varShuf" == "ON" ]]
                then
                        songNum=$(echo $(($RANDOM % ${#array[@]})))
                else
                        songNum=$(($songNum + 1))
                        if [[ "$songNum" == "${#array[@]}" ]]
                        then
                                songNum="0"
                        fi
                fi

        fi
        #Play songNum
	sudo echo "load /var/www/music/${array[$songNum]}" >> "$mypipe"
	varState="PLAY"
	logger "LOG: Opcio musica seguent"
elif [[ "$option" == "pause" ]]
then
	if [[ "$varState" == "PLAY" ]]
	then
		sudo echo "pause" >> "$mypipe"
		varState="PAUSE"
	fi
	logger "LOG: Opcio musica pause"
elif [[ "$option" == "play" ]]
then
	sudo echo "load /var/www/music/${array[$songNum]}" >> "$mypipe"
	varState="PLAY"
	logger "LOG: Opcio musica play"
fi

out=""
for (( i=0; i<${#array[@]}; i++))
do
        out+="<tr"
	if [[ "$i" == "$songNum" ]]
	then
		out+=' class="selected"'
	fi
	out+="> <td>"$(echo ${array[i]})"</td> </tr>"
done

echo $(cat ../html/musica.html | sed -e 's~{{codiHTML}}~'"$out"'~g' | sed -e "s~{dis_shuffle}~$varShuf~g" | sed -e "s~{dis_replay}~$varRep~g")

echo $songNum > ../metaMusic
echo "1:$varShuf" >> ../metaMusic
echo "2:$varRep" >> ../metaMusic
echo "3:$varState" >> ../metaMusic




#echo 'load /var/www/phase2/music/Enemy.mp3' >> "$mypipe"
#echo 'silence' >> "$mypipe"
