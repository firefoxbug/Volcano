#!/usr/bin/python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.net
import os
import sys
import signal
from put_file import PutFile
from exec_cmd import ExecCMD
from put_dir import PutDIR
from report_log import ReportLog
import rlcompleter, readline

class GetConf(object):
	@classmethod
	def read_local_conf(self):
		conf_file = "./conf/volcano.conf"
		tmp_conf_file = "./conf/volcano.conf.tmp"
		
		if not os.path.exists(conf_file):
			ReportLog.sys_info("%s does not exists !"%(conf_file))
		cmd = "sed \'/^$/D\' %s | grep -v \"^[[:blank:]]*#\" > %s"%(conf_file,tmp_conf_file)
		os.system(cmd)	
		fd = open(tmp_conf_file)
		self.hosts_list = []
		while True:
			hosts = {}
			line = fd.readline()
			if not line :
				break
			hosts['ip'] = line.split()[0]
			hosts['passwd'] = line.split()[1]
			hosts['port'] = 22
			hosts['username'] = "root"
#			put_dir_test(hosts)
			exec_cmd_test(hosts)
			self.hosts_list.append(hosts)
		fd.close()
		os.system("rm -f %s"%tmp_conf_file)
		return self.hosts_list
	
	def read_mysql_conf(self):
		pass;


class Volcano(object):
	"""docstring for Volcano"""
	def __init__(self):
		self.fun_map = {1:ExecCMD.exec_cmd,2:PutFile.put_file,3:PutDIR.put_dir}
#		self.print_choose()
		
#		self.job_call = {}
		self.hosts_list = []

	def submit_job(self):
		self.read_local_conf()
		self.get_choose()

	def get_choose(self):
		
		while True:
#			'''execute commands'''
			resultes = dict(OK=[],NO=[])
			self.print_choose()
			opt = raw_input("Please input choice : ").strip()
			if opt == "1":
				cmd2exec = self.get_execute2cmds()
				if not cmd2exec:
#					print "Error..."
					continue
				for hosts in self.hosts_list:
					hosts['cmd2exec'] = cmd2exec
					if ExecCMD.exec_cmd(hosts):
						resultes["OK"].append(hosts['ip'])
					else:
						resultes["NO"].append(hosts['ip'])
#			'''transfer file'''
			elif opt == "2":
				(local_file_path,remote_file_path) = self.get_file2transfer()
				for hosts in self.hosts_list:
					hosts['file2put'] = local_file_path
					hosts['file2save'] = remote_file_path
					if PutFile.put_file(hosts):
						resultes["OK"].append(hosts['ip'])
					else:
						resultes["NO"].append(hosts['ip'])
#			'''transfer dictory'''
			elif opt == "3":
				(local_dir_path,remote_dir_path) = self.get_dir2transfer()
				for hosts in self.hosts_list:
					hosts['dir2put'] = local_dir_path
					hosts['dir2save'] = remote_dir_path
					if PutDIR.put_dir(hosts):
						resultes["OK"].append(hosts['ip'])
					else:
						resultes["NO"].append(hosts['ip'])
			elif opt == "4":
				pass
			else :
				continue
			self.print_results(resultes)
#			self.job_call = dict(func=self.fun_map[opt])

	def print_results(self,resultes):
		print "Final resulte :"
		print "======Successfully======"
		for ip in resultes['OK']:
			print ip
		print "========Failed=========="
		for ip in resultes['NO']:
			print ip
		print 

	def print_choose(self):
		print '''\
[1]. Excetue commands on remote nodes
[2]. Transmission file form localhost to remote nodes
[3]. Transmission dictory form localhost to remote nodes
[4]. Download file from remote node to localhost
'''
	def get_execute2cmds(self):
		while True:
			cmd2exec = raw_input("Please input commands : ")
			if cmd2exec :
				break
		return cmd2exec

	def get_file2transfer(self):
		remote_file_path=''
		local_file_path=''
		local_file_path = raw_input("Please input local path : ")
		if not os.path.isfile(local_file_path):
			ReportLog.sys_info("%s does not exists !"%(local_file_path))
			sys.exit(1)
		remote_file_path = raw_input("Please input remote path : ")
		return (local_file_path,remote_file_path)

	def get_dir2transfer(self):
		remote_dir_path=''
		local_dir_path=''
		local_dir_path = raw_input("Please input local path : ")
		if not os.path.isdir(local_dir_path):
			ReportLog.sys_info("%s does not exists !"%(local_dir_path))
			sys.exit(1)
		remote_dir_path = raw_input("Please input remote path : ")
		return (local_dir_path,remote_dir_path)

	def read_local_conf(self):
		conf_file = "./conf/volcano.conf"
		tmp_conf_file = "./conf/volcano.conf.tmp"
		
		if not os.path.exists(conf_file):
			ReportLog.sys_info("%s does not exists !"%(conf_file))
		cmd = "sed \'/^$/D\' %s | grep -v \"^[[:blank:]]*#\" > %s"%(conf_file,tmp_conf_file)
		os.system(cmd)	
		fd = open(tmp_conf_file)
		while True:
			hosts = {}
			line = fd.readline()
			if not line :
				break
			hosts['ip'] = line.split()[0]
			hosts['passwd'] = line.split()[1]
			hosts['port'] = 22
			hosts['username'] = "root"
			self.hosts_list.append(hosts)
		fd.close()
		os.system("rm -f %s"%tmp_conf_file)
#		print self.hosts_list
#		return self.hosts_list

class Watcher:
	def __init__(self):
		""" Creates a child thread, which returns.  The parent
			thread waits for a KeyboardInterrupt and then kills
			the child thread.
		"""
		self.child = os.fork()
		if self.child == 0:
			return
		else:
			self.watch()
 
	def watch(self):
		try:
			os.wait()
		except KeyboardInterrupt:
			print ' exit...'
			self.kill()
		sys.exit()
 
	def kill(self):
		try:
			os.kill(self.child, signal.SIGKILL)
		except OSError:
			pass

def put_dir_test(hosts):
	hosts['dir2put'] = "/home/firefoxbug/server/OpenCDN2/node/Tengine/conf"
	hosts['dir2save'] = "/usr/local/nginx"
	PutDIR.put_dir(hosts)

def exec_cmd_test(hosts):
	hosts['cmd2exec'] = "cp -raf /usr/local/nginx /usr/local/nginx2"	
	ExecCMD.exec_cmd(hosts)

def main():
	readline.parse_and_bind('tab: complete')
	vol = Volcano()
	vol.submit_job()
	pass;

if __name__ == '__main__':
	w = Watcher()
	main()