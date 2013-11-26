#!/usr/bin/python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.net

"""
execute commands on remote hosts

"""
import os
import time
import socket
import paramiko
from report_log import ReportLog

class ExecCMD(object):
	@classmethod
	def exec_cmd(self,exec_cmd):
		try :
#			print exec_cmd['ip'],exec_cmd['passwd']
#			print "\n"
			print "Connecting %s..."%exec_cmd['ip']
			log_time = time.strftime("%Y-%m-%d %H:%M:%S")
			socket.setdefaulttimeout(2)
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(exec_cmd['ip'],exec_cmd['port'],exec_cmd['username'],exec_cmd['passwd'])
			stdin, stdout, stderr = ssh.exec_command(exec_cmd['cmd2exec'])
			err_message = stderr.read()
			if err_message:
				ReportLog.send_results(False,"[ERROR %s]: execute [%s] on %s"%(log_time,exec_cmd['cmd2exec'],exec_cmd['ip']),des_str=err_message)
				return False
			ok_message = stdout.read()
			ReportLog.send_results(True,"[INFO %s]: execute [%s] on %s"%(log_time,exec_cmd['cmd2exec'],exec_cmd['ip']),des_str=str(ok_message))
			ssh.close()
		except socket.timeout:
			ReportLog.send_results(False,"[ERROR %s]: execute [%s] on %s"%(log_time,exec_cmd['cmd2exec'],exec_cmd['ip']),des_str="%s Connection timed out"%(exec_cmd['ip']))
			return False
		except socket.error:
			ReportLog.send_results(False,"[ERROR %s]: execute [%s] on %s"%(log_time,exec_cmd['cmd2exec'],exec_cmd['ip']),des_str="%s Connection timed out"%(exec_cmd['ip']))
			return False
		except paramiko.AuthenticationException:
			ReportLog.send_results(False,"[ERROR %s]: execute [%s] on %s"%(log_time,exec_cmd['cmd2exec'],exec_cmd['ip']),des_str="[IP=%s Password=%s] Authentication failured"%(exec_cmd['ip'],exec_cmd['passwd']))
			return False		
		return True

exec_cmd = {}
exec_cmd['ip'] = "42.21.117.13"
exec_cmd['username'] = "root"
exec_cmd['passwd'] = "zooboa.com"
exec_cmd['port'] = 22
exec_cmd['cmd2exec'] = "ls ...."

if __name__ == '__main__':
	result = ExecCMD.exec_cmd(exec_cmd)
#	ReportLog.send_results(True,"YES: execute [%s]"%(exec_cmd['cmd2exec']))
