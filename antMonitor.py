#!/usr/bin/env python2.7
def antMonitor(miner,dc):
	import socket
	import json
	import sys
	import re
	from datetime import date, datetime, timedelta
	import mysql.connector
	import secrets

	def linesplit(socket):
		buffer = socket.recv(4096)
		done = False
		while not done:
			more = socket.recv(4096)
			if not more:
				done = True
			else:
				buffer = buffer+more
		if buffer:
			return buffer

	api_command1 = 'summary'
	api_command2 = 'stats'
	api_command3 = 'pools'
	api_ip = miner
	api_port = 4028

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((api_ip,int(api_port)))

#Summary Command
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((api_ip,int(api_port)))
	s.send(json.dumps({"command":api_command1}))
	summary = linesplit(s)
	summary = summary.replace('\x00','')
	try:
		summary = json.loads(summary)
	except Exception:
	 	summary = re.sub('[}][{]','},{',summary)
		summary = json.loads(summary)
	summaryStatus = summary['STATUS'][0]
	summarySummary = summary['SUMMARY'][0]
	s.close()
	
#Stats Command
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((api_ip,int(api_port)))
	s.send(json.dumps({"command":api_command2}))
	stats = linesplit(s)
	stats = stats.replace('\x00','')
	try:
		stats = json.loads(stats)
	except Exception:
	 	stats = re.sub('[}][{]','},{',stats)
		stats = json.loads(stats)
	mType = stats['STATS'][0]
	stats = stats['STATS'][1]
	s.close()

#Pools Command
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((api_ip,int(api_port)))
	s.send(json.dumps({"command":api_command3}))
	pools = linesplit(s)
	pools = pools.replace('\x00','')
	try:
		pools = json.loads(pools)
	except Exception:
	 	pools = re.sub('[}][{]','},{',pools)
		pools = json.loads(pools)
	pools = pools['POOLS']
	i = 0
	poolDict = {}
	while i <= len(pools) - 1:
		d = i + 1
		poolDict["pool{0}".format(d)] = pools[i]['URL']
		poolDict["worker{0}".format(d)] = pools[i]['User']
		i += 1
	s.close()

	#Extract Data from API Return
	writeDate = datetime.now()
	minerIP = miner
	try:
		minerID = stats['ID']
	except Exception:
		pass
	try:
		minerID = stats['miner_id']
	except Exception:
		pass
#	try:
#		minerID = stats['ID']
#	except Exception as e:
#		print(e)
#		raise e
#	def id1():
#		try:
#			minerID = stats['ID']
#			return minerID
#		except Exception as e:
#			print(e)
#			raise e
#	def id2():
#		try:
#			minerID = stats['miner_id']
#			return minerID
#		except Exception as e:
#			print(e)
#			raise e
#	def idCheck():
#		try:
#			id1() or id2()
#		except:
#			print('No Miner ID\'s found')
#		else:
#			return None
#	minerID = str(idCheck())
	minerType = mType['Type']
	ghs_5s = summarySummary['GHS 5s']
	ghs_av = summarySummary['GHS av']
	uptime = summarySummary['Elapsed']
	pool1 = poolDict['pool1']
	pool2 = poolDict['pool2']
	pool3 = poolDict['pool3']
	worker1 = poolDict['worker1']
	worker2 = poolDict['worker2']
	worker3 = poolDict['worker3']
	temps = []

	i = int(0)
	while i <= 2:
		try:
			value = stats['temp1']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp2']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp3']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp4']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp5']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp6']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp7']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp8']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp9']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp10']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp11']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp12']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp13']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp14']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp15']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp16']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp17']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp18']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp19']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i
		try:
			value = stats['temp20']
			if value == 0:
				i = i
			else:
				temps.append(value)
				i += 1
		except Exception as e:
			i = i

	tempD = {}
	i = 1
	for x in temps:
		tempD["temp{0}".format(i)] = x
		i += 1
	try:
		temp1 = tempD['temp1']
	except Exception as e:
		temp1 = ''
	try:
		temp2 = tempD['temp2']
	except Exception as e:
		temp2 = ''
	try:
		temp3 = tempD['temp3']
	except Exception as e:
		temp3 = ''
	try:
		temp4 = tempD['temp4']
	except Exception as e:
		temp4 = ''

	#Open SQL Connection
	cnx = mysql.connector.connect(user='antMan', password=secrets.antManPass , database='antStore')
	cursor = cnx.cursor()

	add_antdata = ("INSERT INTO dc1 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")
	data_antdata = (writeDate, minerIP, minerID, minerType, ghs_5s, ghs_av, pool1, pool2, pool3, worker1, worker2, worker3, temp1, temp2, temp3, temp4, uptime, dc)

	cursor.execute(add_antdata, data_antdata)

	cnx.commit()

	cursor.close()
	cnx.close()
#	print(writeDate, minerIP, minerID, minerType, ghs_5s, ghs_av, pool1, pool2, pool3, worker1, worker2, worker3, temp1, temp2, temp3, temp4, uptime, dc)
#	print('this is working')
#import sys	
#antMonitor(sys.argv[1],sys.argv[2])
