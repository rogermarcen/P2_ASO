#!/bin/bash
#echo 'Content-Type: text/html'
#echo
#echo

read web_user
user=$(echo $web_user | sed -e "s/web_user=//g")
user=${user::-1}
now=$(date +"%T")
varDate=$(date +"%d/%b/%Y")

#logger -p local2.info "<<:$user $REMOTE_ADDR $now $varDate :>>restarted the server"

hostname=$(hostname -I)
hostname=${hostname::-1}
homepage=$(echo "http://"$hostname"/html/index.html")

echo "Location: $homepage"
echo
echo
sudo service apache2 restart
