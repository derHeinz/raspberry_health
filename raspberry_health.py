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

	def query_cpu_temp(self):
		return "18"
		
	def query_cpu_clock(self):
		return "500"
		
	def query_sys_temp(self):
		return "82"
		
	def query_sys_hum(self):
		return "42"

class RaspberryHealthLinux(RaspberryHealth):
	
	def __init__(self):
		super(RaspberryHealthLinux, self).__init__()
		self.subprocess = __import__('subprocess')
		self.dht = __import__('Adafruit_DHT')

	def query_cpu_temp(self):
		"""get cpu temperature using vcgencmd"""
		process = self.subprocess.Popen(['vcgencmd', 'measure_temp'], stdout=self.subprocess.PIPE)
		output, _error = process.communicate()
		return float(output[output.index('=') + 1:output.rindex("'")])
		
	def query_cpu_clock(self):
		process = self.subprocess.Popen(['vcgencmd', 'measure_clock', 'arm'], stdout=self.subprocess.PIPE)
		output, _error = process.communicate()
		return float(output[output.index('=') + 1:])
		
	def _query_dht(self):
		return self.dht.read_retry(self.dht.DHT22, 26)
		
	def query_sys_temp(self):
		humidity, temperature = _query_dht()
		return temperature
		
	def query_sys_hum(self):
		humidity, temperature = _query_dht()
		return humidity
	
		
def signal_handler(signal, frame):
	print('Exiting!')
	os._exit(0)

if __name__ == '__main__':
	pf = platform.system()
	print("Starting on " + pf + "\nPress CTRL-C to exit")
	ph = None
	if "Windows" == pf:
		ph = RaspberryHealthWindows()
	else:
		ph = RaspberryHealthLinux()
	ph.start()
	signal.signal(signal.SIGINT, signal_handler)
	while True:
		time.sleep(1000)
