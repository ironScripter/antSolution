##! /usr/bin/env python
## vim: set fenc=utf8 ts=4 sw=4 et :
import sys
import antMonitor
import socket
import multiprocessing
import time

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
	port = 4028  # port number is a number, not string
	try:
		s.connect((address,int(port)))
		sMiners.append(miners[i])
	    # originally, it was 
	    # except Exception, e: 
	    # but this syntax is not supported anymore. 
	except Exception as e: 
		x = 0
	finally:
	    s.close()
	i += 1
	s.close()
print('----------------------------Gathering Data--------------------------')
i = 0
while i < len(sMiners):
	print('Gathering Data for: ' + sMiners[i])
	try:
		p = multiprocessing.Process(target=antMonitor.antMonitor, args=(sMiners[i],sys.argv[2]))
		p.start()
		time.sleep(.2)
		if p.is_alive():
			time.sleep(2)
		if p.is_alive():
			p.terminate()
	except Exception as e:
		print("Miner: %s Error: %s" % (sMiners[i], e))
	i += 1
