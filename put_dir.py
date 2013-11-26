#!/usr/bin/python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.net

"""
put directory to remote hosts

"""
import os
import socket
import time
from report_log import ReportLog

class PutDIR(object):
	@classmethod
	def dir_exists(self,dirput):
		if not os.path.isdir(dirput['dir2put']):
			ReportLog.send_results(False,"NO: locate [%s]"%(dirput['dir2put']),des_str="%s doesn't exist."%(dirput['dir2put']))
			return False
		return True

	@classmethod
	def put_dir(self,dirput):

		if not self.dir_exists(dirput):
			return False
		socket.setdefaulttimeout(2)
		print "Connecting %s..."%dirput['ip']
		log_name = "/tmp/" + dirput['ip'].split('/')[-1] + "_put_dir.log"
		put_dir_cmd = "./put_dir.sh %s %s %s %s > %s 2>&1"%(dirput['ip'],dirput['passwd'],dirput['dir2put'],dirput['dir2save'],log_name)
#		print put_dir_cmd
		log_time = time.strftime("%Y-%m-%d %H:%M:%S")
		os.popen(put_dir_cmd)
		fd = open(log_name,'r')
		log = fd.read(1024)
		if 'No such file or directory' in log:
			ReportLog.send_results(False,"[ERROR %s]: upload %s to %s"%(log_time,dirput['dir2put'],dirput['ip']),des_str="%s doesn't exist on %s ."%(dirput['dir2save'],dirput['ip']))
			return False
		elif 'timed out' in log or 'Connection refused' in log:
			ReportLog.send_results(False,"[ERROR %s]: upload %s to %s"%(log_time,dirput['dir2put'],dirput['ip']),des_str="%s: Connection timed out."%(dirput['ip']))
			return False
#		print log
		ReportLog.send_results(True,"[INFO %s]: upload %s to %s"%(log_time,dirput['dir2put'],dirput['ip']))
		fd.close()
		return True

dirput = {}
dirput['ip'] = "42.121.117.13"
dirput['username'] = "root"
dirput['passwd'] = "zooboa.com"
dirput['port'] = 22
dirput['dir2put'] = "./log/"
dirput['dir2save'] = "/home/debugd/"

if __name__ == '__main__':
	
	PutDIR.put_dir(dirput)
