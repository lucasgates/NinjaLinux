#!/bin/bash

killall /usr/lib/deja-dup/deja-dup/deja-dup-monitor
killall update-notifier
killall /usr/lib/ubuntuone-client/ubuntuone-syncdaemon
kill `ps aux |grep ubuntuone-client |grep -v grep | awk '{print $2}'` 
killall /usr/lib/gnome-online-accounts/goa-daemon
killall /usr/lib/telepathy/mission-control-5

