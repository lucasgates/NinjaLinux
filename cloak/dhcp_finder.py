#!/usr/bin/python

from scapy.all import *

print "This application is used to sniff the wire to discover what the following:"
print "    * Mac addresses"
print "    * Local IP addresses"
print "    * Network mask"
print "    * Gateway"
print "    * Domain (if in a Windows environment)"
print "    * General hostnames"
print
print
print "Looking for Mac addresses"

"""Notes: If you are in a wireless network, you can simply listen for DHCP ACK responses.
However, that won't work if you are in wired network. Should add options for both."""

conf.checkIPaddr = 0
fa, hw = get_if_raw_hwaddr(conf.iface)

for i in range(0,5):
  response = dhcp_request(timeout=10)
  if response:
    break

if not response:
  print "Couldn't find a DHCP server..."
  print "Quitting!!"
  exit()

print "Suggested IP:        ",response[0][BOOTP].yiaddr
print "Suggested router:    ",response[0][DHCP].options[6] 
print "Suggested netmask:   ",response[0][DHCP].options[7] 
print "Suggested nameserver:",response[0][DHCP].options[5] 
