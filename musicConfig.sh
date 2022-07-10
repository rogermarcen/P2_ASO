#!/bin/bash

sudo echo "silence" >> /var/www/cmdMusic
sudo chmod 777 /var/www/cmdMusic
sudo echo "0" > ./metaMusic
sudo echo "1:OFF" >> ./metaMusic
sudo echo "2:OFF" >> ./metaMusic
sudo echo "3:OFF" >> ./metaMusic
