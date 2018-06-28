##! /usr/bin/env python
## vim: set fenc=utf8 ts=4 sw=4 et :

import socket

f = open('servers.txt', 'r')
miners  = f.read().splitlines()
f.close()

sMiners = []
i = 0
while i < len(miners):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.settimeout(.01)
	address = miners[i]
	port = 4028  # port number is a number, not string
	try:
		s.connect((address,int(port)))
		print(miners[i])
		sMiners.append(miners[i])
	    # originally, it was 
	    # except Exception, e: 
	    # but this syntax is not supported anymore. 
	except Exception as e: 
		x = 0
	finally:
	    s.close()
	i += 1
print(sMiners)