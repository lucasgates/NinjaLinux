#!/bin/bash

echo "Hiding my identity..."
echo "AIX 5.0" > /etc/issue.net
echo "AIX-backup" > /etc/hostname

echo "Fixing Nikto USERAGENT"
sed -i -n 's/USERAGENT=.*/USERAGENT=Mozilla\/5\.0 (Windows NT 6\.1\; rv\:21\.0) Gecko\/20100101 Firefox\/21.0/g' /etc/nikto/config.txt 

echo "Starting postgres by default"
update-rc.d  postgresql enable
service postgresql start

#echo "Updating Metasploit"
#msfupdate


echo "Done"

