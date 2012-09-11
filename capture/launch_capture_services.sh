#!/bin/bash

echo "Launching fake services to capture:"
echo "    * SSH"
echo "    * FTP"
echo "    * Telnet"
echo "    * SMB"
echo "    * SMTP"
echo "    * HTTP (Basic Auth)"
echo "    * HTTP_NTLM"
echo "    * IMAP"
echo "    * MSSQL"
echo "    * MySQL"
echo "    * sip"
echo "    * telnet"
echo "    * vnc"

echo "This isn't useful yet..."
exit


use auxiliary/server/capture/pop3
set SRVPORT 110
set SSL false
run

use auxiliary/server/capture/pop3
set SRVPORT 995
set SSL true
run

use auxiliary/server/capture/ftp
run

use auxiliary/server/capture/imap
set SSL false
set SRVPORT 143
run

use auxiliary/server/capture/imap
set SSL true
set SRVPORT 993
run

use auxiliary/server/capture/smtp
set SSL false
set SRVPORT 25
run

use auxiliary/server/capture/smtp
set SSL true
set SRVPORT 465
run
