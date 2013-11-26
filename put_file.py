#!/usr/bin/python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.net

"""
put file to remote hosts

"""
import os
import socket
import paramiko
import time
from report_log import ReportLog

'''
fileput
{
	'ip':			192.168.1.1
	'port':			22
	'username':		root
	'password':		volcano
	'file2put':		file_name
	'file2save':	remote_dir
}

'''
class PutFile(object):
	@classmethod 
	def file_exist(self,fileput):
		if not os.path.isfile(fileput['file2put']):
			ReportLog.send_results(False,"NO: locate [%s]"%(fileput['file2put']),des_str="%s doesn't exist."%(fileput['file2put']))
			return False
		return True

	@classmethod
	def put_file(self,fileput):

		if not self.file_exist(fileput):
			return False

		try:
			log_time = time.strftime("%Y-%m-%d %H:%M:%S")
			print "Connecting %s..."%fileput['ip']
			socket.setdefaulttimeout(5)
			t = paramiko.Transport((fileput['ip'],fileput['port']))
			t.connect(username = fileput['username'], password = fileput['passwd'])
			sftp = paramiko.SFTPClient.from_transport(t)
			sftp.put(fileput['file2put'],fileput['file2save'])
			t.close()
		except IOError:
			error_msg = fileput['file2save'] + " is wrong."
			ReportLog.send_results(False,"[ERROR %s]: upload %s to %s"%(log_time,fileput['file2put'],fileput['ip']),des_str=error_msg)
			return False
		except Exception,e:
			ReportLog.send_results(False,"[ERROR %s]: upload %s to %s"%(log_time,fileput['file2put'],fileput['ip']),des_str=str(e))
			return False
		ReportLog.send_results(True,"[INFO %s]: upload %s to %s"%(log_time,fileput['file2put'],fileput['ip']))
		return True

if __name__ == '__main__':
	fileput = {}
	fileput['ip'] = "42.121.117.13"
	fileput['username'] = "root"
	fileput['passwd'] = "zooboa.com"
	fileput['port'] = 22
	fileput['file2put'] = "./install.sh"
	fileput['file2save'] = "//shome/debug/1aaa.txt"

	PutFile.put_file(fileput)