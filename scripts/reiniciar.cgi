#!/bin/bash
#echo 'Content-Type: text/html'
#echo
#echo

logger "LOG: Usuari ha reiniciat el servidor"

hostname=$(hostname -I)
hostname=${hostname::-1}
homepage=$(echo "http://"$hostname"/html/index.html")

echo "Location: $homepage"
echo
echo
sudo service apache2 restart
