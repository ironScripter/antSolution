#!/usr/bin/env python2.7
def antIdent(miner):
    import socket
    import json
    import sys
    import re
    from datetime import date, datetime, timedelta
    import mysql.connector
    import paramiko
    import hashlib
    import base64
    from termcolor import colored
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

    api_command2 = 'stats'
    api_command3 = 'pools'
    api_ip = miner
    api_port = 4028
#Get Data from API
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((api_ip,int(api_port)))
    except Exception as e:
        raise e
#Get SSH Fingerprint as minerID
    try:
        try:
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mySocket.connect((miner, int(22)))
        except socket.error:
            print "Error opening socket"
            quit()
         
        try:
            myTransport = paramiko.Transport(mySocket)
            myTransport.start_client()
            sshKey = myTransport.get_remote_server_key()
        except paramiko.SSHException:
            print "SSH error"
            quit()
        myTransport.close()
        mySocket.close()

        sshFingerprint = hashlib.md5(sshKey.__str__()).hexdigest()
        minerID = ':'.join(a+b for a,b in zip(sshFingerprint[::2], sshFingerprint[1::2]))
        minerID = str(minerID)
    except Exception as e:
        raise e
#Stats Command
    try:
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
    except Exception as e:
        raise e

#Pools Command
    try:
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
    except Exception as e:
        raise e

    #Extract Data from API Return
    writeDate = datetime.now()
    minerIP = miner
    minerType = mType['Type']
    pool1 = poolDict['pool1']
    pool2 = poolDict['pool2']
    pool3 = poolDict['pool3']
    worker1 = poolDict['worker1']
    worker2 = poolDict['worker2']
    worker3 = poolDict['worker3']

    #Open SQL Connection
    try:
        cnx = mysql.connector.connect(user='antMan', password=secrets.antManPass , database='antStore')
        cursor = cnx.cursor()

        add_antdata = ("REPLACE INTO antIdent VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")
        data_antdata = (writeDate, minerIP, minerID, minerType, pool1, pool2, pool3, worker1, worker2, worker3)

        cursor.execute(add_antdata, data_antdata)

        cnx.commit()

        cursor.close()
        cnx.close()
    except Exception as e:
        raise e
    print colored("WriteDate: %s \nMinerIP: %s \nMinerID: %s \nMinerType: %s \nPool1: %s \nPool2: %s \nPool3: %s \nWorker1: %s \nWorker2: %s \nWorker3: %s" % (writeDate, minerIP, minerID, minerType, pool1, pool2, pool3, worker1, worker2, worker3), 'Green')
#antIdent('192.168.2.54')