#!/usr/bin/python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.net

import json
import time
import sys

class ReportLog(object):
	@classmethod
	def sys_info(self,error_str):
		now_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		print "[ERROR %s] : %s"%(now_time,error_str)
		sys.exit(1)
		
	@classmethod
	def send_results(self,res,info_str,des_str=""):
		results = {}
		if res :
			results['result'] = True
		else:
			results['result'] = False
		results['description'] = des_str
		results['data'] = info_str
		print json.dumps(results)