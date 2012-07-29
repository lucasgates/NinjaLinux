#!/usr/bin/python

import re

lines = [
    "Jul 12 20:17:24 Netgear NetworkManager[860]: <info> (wlan0): DHCPv4 state changed preinit -> reboot",
    "Jul 12 20:17:24 Netgear NetworkManager[860]: <info>   address 192.168.1.68",
    "Jul 12 20:17:24 Netgear NetworkManager[860]: <info>   prefix 24 (255.255.255.0)",
    "Jul 12 20:17:24 Netgear NetworkManager[860]: <info>   gateway 192.168.1.254",
    "Jul 12 20:17:24 Netgear NetworkManager[860]: <info>   nameserver '192.168.1.254'",
]

reg_address = re.compile(r'address (.*)')
reg_gateway = re.compile(r'gateway (.*)')
reg_nmsever = re.compile(r'nameserver (.*)')

for item in lines:
  m_addy    = reg_address.search(item)
  if m_addy:
    print "Found address:",    m_addy.group(1)
    
  m_gatew   = reg_gateway.search(item)
  if m_gatew:
    print "Found gateway:",    m_gatew.group(1)

  m_nmsvr   = reg_nmsever.search(item)
  if m_nmsvr:
    print "Found nameserver:", m_nmsvr.group(1)
