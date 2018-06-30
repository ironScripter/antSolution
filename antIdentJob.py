#!/usr/bin/env python2.7
import sys
import antIdent
import socket
import multiprocessing
import time
from termcolor import colored

f = open(sys.argv[1], 'r')
miners  = f.read().splitlines()
f.close()

sMiners = []
print('--------------------Discovering Miners-------------------------')
i = 0
while i < len(miners):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.settimeout(.05)
	address = miners[i]
	port = 4028
	try:
		s.connect((address,int(port)))
		sMiners.append(miners[i])
	except Exception as e: 
		x = 0
	finally:
	    s.close()
	i += 1
	s.close()
print('----------------------------Gathering Indentity Data--------------------------')
i = 0
jobs = []
while i < len(sMiners):
	print colored('Gathering Indentity Data for: ' + sMiners[i], 'blue')
	try:
		for i in range(40):
			p = multiprocessing.Process(target=antIdent.antIdent , args=(sMiners[i],))
			jobs.append(p)
			p.start()
		for job in jobs:
			job.join()
	except Exception as e:
		print("Miner: %s Error: %s" % (sMiners[i], e))
	i += 1
