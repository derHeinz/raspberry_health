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

class RaspberryHealthLinux(RaspberryHealth):
	
	def __init__(self):
		super(RaspberryHealthLinux, self).__init__()
		self.subprocess = __import__('subprocess')
		self.dht = __import__('Adafruit_DHT')
		
	def _query_process(self, args):
		process = self.subprocess.Popen(args, stdout=self.subprocess.PIPE)
		output, _error = process.communicate()
		return output

	def query_cpu_temp(self):
		output = self._query_process(['vcgencmd', 'measure_temp'])
		return float(output[output.index('=') + 1:output.rindex("'")])
		
	def query_cpu_clock(self):
		output = self._query_process(['vcgencmd', 'measure_clock', 'arm'])
		return long(output[output.index('=') + 1:])
		
	def query_sys_temp(self):
		output = self._query_process(['cat', '/sys/class/thermal/thermal_zone0/temp'])
		return float(output) / 1000
		
	def _query_dht(self):
		return self.dht.read_retry(self.dht.DHT22, 26)
		
	def query_external_temp(self):
		humidity, temperature = self._query_dht()
		return temperature
		
	def query_external_hum(self):
		humidity, temperature = self._query_dht()
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
