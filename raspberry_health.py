#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import platform
import signal
import time
import sys
import os
from network_api import NetworkAPI

class RaspberryHealth(object):
	
	def __init__(self):
		super(RaspberryHealth, self).__init__()
		self._api = NetworkAPI(self)
	
	def start(self):
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
		process = self.subprocess.Popen(['vcgencmd', 'measure_temp'], stdout=self.subprocess.PIPE)
		output, _error = process.communicate()
		return float(output[output.index('=') + 1:output.rindex("'")])
		
	def cpu_clock(self):
		return "500"
		
def signal_handler(signal, frame):
	print('Exiting!')
	os._exit(0)

if __name__ == '__main__':
	pf = platform.system()
	print("Starting \nPress CTRL-C to exit")
	ph = None
	if "Windows" == pf:
		ph = RaspberryHealthWindows()
	else:
		ph = RaspberryHealthLinux()
	ph.start()
	signal.signal(signal.SIGINT, signal_handler)
	while True:
		time.sleep(1000)
