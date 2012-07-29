#!/bin/bash

apt-get -y install kismet
apt-get -y install nikto
apt-get -y install python-scapy
apt-get -y install python-twisted
#apt-get -y install snort snort-doc suricata oinkmaster
apt-get -y install psad
apt-get -y install john john-data ophcrack ophcrack-cli
apt-get -y install hydra hydra-gtk
apt-get -y install hydra hydra-gtk
apt-get -y install labrea
apt-get -y install subversion
apt-get -y install libssl-dev
apt-get -y install upx
apt-get -y install python-twisted-conch
svn co http://trac.aircrack-ng.org/svn/trunk/ tools/aircrack-ng
cd tools/aircrack-ng 
make
make install
cd ../..
mkdir docs
cd docs
wget http://vulnerabilityassessment.co.uk/Penetration%20Test.html
wget http://ha.ckers.org/xss.html
cd ../tools
wget http://downloads.sourceforge.net/sqlmap/sqlmap-0.9.tar.gz
cd ..
