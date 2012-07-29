#!/usr/bin/python

import re

myfile      = open('sample_log.txt', 'r')

for item in myfile.readlines():
  print item


message     = re.compile(r'address (.*)')
priority    = re.compile(r' (.*)')
attacker    = re.compile(r'nameserver (.*)')

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
