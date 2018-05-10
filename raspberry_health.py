#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import platform
from subprocess import PIPE, Popen
from network_api import NetworkAPI

class RaspberryHealth(object):
	
	def __init__(self):
		super(RaspberryHealth, self).__init__()
		self._api = NetworkAPI(self)
		self._api.start()
		
class RaspberryHealthWindows(RaspberryHealth):
	def __init__(self):
		super(RaspberryHealthWindows, self).__init__()

	def cpu_temp(self):
		return "18"
		
	def cpu_clock(self):
		return "500"

class RaspberryHealthLinux(RaspberryHealth):
	subprocess = __import__('subprocess')
	
	def __init__(self):
		super(RaspberryHealthLinux, self).__init__()

	def cpu_temp(self):
		"""get cpu temperature using vcgencmd"""
		process = subprocess.Popen(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
		output, _error = process.communicate()
		return float(output[output.index('=') + 1:output.rindex("'")])
		
	def cpu_clock(self):
		return "500"
		
if __name__ == '__main__':
	pf = platform.system()
	if "Windows" == pf:
		RaspberryHealthWindows()
	else:
		RaspberryHealthLinux()
