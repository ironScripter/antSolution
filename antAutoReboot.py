##! /usr/bin/env python
## vim: set fenc=utf8 ts=4 sw=4 et :

import antReboot
import mysql.connector
from datetime import datetime
import multiprocessing, time
import secrets

rebootDate = datetime.now()

cnx = mysql.connector.connect(user='antMan', password=secrets.antManPass, database='antStore')
cursor = cnx.cursor()

query = "SELECT B.ip as minerIP, B.id as minerID, B.dc as minerDC FROM ( select ip, max(writeDate) writeDate from dc1 group by ip ) A INNER JOIN dc1 B USING (ip,writeDate) WHERE B.writeDate >= DATE_SUB(NOW(), INTERVAL 1 HOUR) AND B.ghs_5s = 0"

cursor.execute(query)

for (minerIP, minerID, minerDC) in cursor:
	minerIP = str(minerIP)
	print('Miner: ' + minerIP + ' ID: ' + minerID + ' Datacenter: ' + minerDC + ' is being rebooted due to low hash rate.')
	try:
		try:
			p = multiprocessing.Process(target=antReboot.reboot, args=minerIP)
			p.start()
			print ('Reboot has been initiated')
			time.sleep(60)
			if p.is_alive():
				print('Reboot took to long to initiate and is being terminated')
				p.terminate()
			else:
				cnx = mysql.connector.connect(user='antMan', password=secrets.antManPass, database='antStore')
				cursor = cnx.cursor()

				add_antdata = ("INSERT INTO reboot VALUES (%s, %s, %s, %s);")
				data_antdata = (rebootDate, minerIP, minerID, minerDC)

				cursor.execute(add_antdata, data_antdata)

				cnx.commit()

				cursor.close()
				cnx.close()

		except Exception as e:
			print(' An error has occured \nError: ' + str(e))
				
	except Exception as e:
		print(' An error has occured \nError: ' + str(e))
	
