#!/usr/bin/env python2.7

def reboot(miner):
	import paramiko, sys

	sshUsername = 'root'
	sshPassword = 'admin'
	cmd = '/sbin/shutdown -r now -n -f'

	ssh = paramiko.SSHClient()
	#Set paramiko to auto add uknown hosts
	try:
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		#Connect to miner and get hostname
		ssh.connect(miner, username=sshUsername, password=sshPassword)
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

		print(ssh_stdout.read())

		ssh.close()
	except Exception as e:
		print(' An error has occured \nError: ' + str(e))