#! /usr/bin/python

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import mysql.connector
import secrets

now = datetime.datetime.now().strftime("%m-%d-%y %l:%M %p")
 
def query_mysql(query):
	cnx = mysql.connector.connect(user='antMan', password=secrets.antManPass , database='antStore')
	cursor = cnx.cursor()
	cursor.execute(query)
	#get header and rows
	header = [i[0] for i in cursor.description]
	rows = [list(i) for i in cursor.fetchall()]
	#append header to rows
	rows.insert(0,header)
	cursor.close()
	cnx.close()
	return rows
 
def nlist_to_html(list2d):
	htable=u'<table border="1" bordercolor=000000 cellspacing="0" cellpadding="1" style="table-layout:fixed;vertical-align:bottom;text-align:right;font-size:13px;font-family:verdana,sans,sans-serif;border-collapse:collapse;border:1px solid rgb(130,130,130)" >'
	list2d[0] = [u'<b>' + i + u'</b>' for i in list2d[0]] 
	for row in list2d:
		newrow = u'<tr>' 
		newrow += u'<td align="left" style="padding:1px 4px">'+unicode(row[0])+u'</td>'
		row.remove(row[0])
		newrow = newrow + ''.join([u'<td align="right" style="padding:1px 4px">' + unicode(x) + u'</td>' for x in row])  
		newrow += '</tr>' 
		htable+= newrow
	htable += '</table>'
	return htable
 
def sql_html(query):
	return nlist_to_html(query_mysql(query))

#################################################################
#																#
#                   Thresholds and Variables					#
#																#
#################################################################

tempThreshold = str(80)

#Email alerts are from this address
sender = secrets.antAlertSender
#Alert recipients
recipient = secrets.antAlertRecipient
#SMTP Settings for sendmail
smtp_server = secrets.antAlertSMTP

#Alert for devices not pinging
def dev_not_pinging_alert():
	email_subject = "AntMonitor Network Alert - Miners Not Pinging - "
	query = "SELECT DATE_FORMAT(B.writeDate, \"%M %d %Y %l:%i %p\") as 'Last Ping Date', B.ip as 'Miner IP', B.type as 'Device Type' FROM ( select ip, max(writeDate) writeDate from dc1 group by ip ) A INNER JOIN dc1 B USING (ip,writeDate) WHERE B.writeDate <= DATE_SUB(NOW(), INTERVAL 1 HOUR)"
	msg = MIMEMultipart('alternative')
	msg['Subject'] = email_subject + now
	msg['From'] = sender
	msg['To'] = recipient
	html = sql_html(query)
	htmlBody= MIMEText(html, 'html')
	msg.attach(htmlBody)
	s = smtplib.SMTP(smtp_server)
	s.sendmail(sender, recipient, msg.as_string())
	s.quit()

#Alert for Hot Devices
def dev_hot_alert(tempThreshold):
	email_subject = "AntMonitor Network Alert - Hot Miners - "
	query = "SELECT DATE_FORMAT(B.writeDate, \"%M %d %Y %l:%i %p\") as 'Last Ping Date', B.ip as 'Miner IP', B.type as 'Device Type', B.temp1 as 'Temperature 1', B.temp2 as 'Temperature 2', B.temp3 as 'Temperature 3', B.temp4 as 'Temperature 4' FROM (SELECT ip, max(writeDate) writeDate FROM dc1 GROUP BY ip) A INNER JOIN dc1 B USING (ip,writeDate) WHERE B.writeDate >= DATE_SUB(NOW(), INTERVAL 1 HOUR) AND (B.temp1 >= " + tempThreshold + " OR B.temp2 >= " + tempThreshold + " OR B.temp3 >= " + tempThreshold + " OR B.temp4 >= " + tempThreshold + ")"
	msg = MIMEMultipart('alternative')
	msg['Subject'] = email_subject + now
	msg['From'] = sender
	msg['To'] = recipient
	html = sql_html(query)
	htmlBody= MIMEText(html, 'html')
	msg.attach(htmlBody)
	s = smtplib.SMTP(smtp_server)
	s.sendmail(sender, recipient, msg.as_string())
	s.quit()

def dev_not_hashing_alert():
	email_subject = "AntMonitor Network Alert - Miners Not Hashing - "
	query = "SELECT DATE_FORMAT(B.writeDate, \"%M %d %Y %r\") as Date, B.ip as 'Miner IP', B.type as 'Device Type', B.ghs_5s as 'Gigahash' FROM ( select ip, max(writeDate) writeDate from dc1 group by ip ) A INNER JOIN dc1 B USING (ip,writeDate) WHERE B.writeDate >= DATE_SUB(NOW(), INTERVAL 1 HOUR) AND B.ghs_5s = 0"
	msg = MIMEMultipart('alternative')
	msg['Subject'] = email_subject + now
	msg['From'] = sender
	msg['To'] = recipient
	html = sql_html(query)
	htmlBody= MIMEText(html, 'html')
	msg.attach(htmlBody)
	s = smtplib.SMTP(smtp_server)
	s.sendmail(sender, recipient, msg.as_string())
	s.quit()

	

dev_not_pinging_alert()
dev_hot_alert(tempThreshold)
dev_not_hashing_alert()