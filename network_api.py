#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import time
import threading
from flask import Flask, jsonify, request, make_response
from multiprocessing import Process
from werkzeug.serving import make_server

class NetworkAPI(threading.Thread):
	
	def __init__(self, health):
		super(NetworkAPI, self).__init__()
		self.setDaemon(False)
		self.app = Flask(__name__)
		self._health = health
		self._server = make_server(host='0.0.0.0', port=5005, app=self.app, threaded=True)
		self.ctx = self.app.app_context()
		self.ctx.push()

		# register some endpoints
		self.app.add_url_rule(rule="/v1.0/cpu_temp", endpoint="cpu_temp", view_func=self.cpu_temp, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/cpu_clock", endpoint="cpu_clock", view_func=self.cpu_clock, methods=['GET'])
		
		# register default error handler
		self.app.register_error_handler(code_or_exception=404, f=self.not_found)
	
	def run(self):
		self._server.serve_forever()
						
	def wrong_request(self, error="Internal Error"):
		return make_response(jsonify({'error': error}), 400)
		
	def not_found(self, error):
		return make_response(jsonify({'error': 'Not found'}), 404)
		
	def _jsonify(self, property, value):
		return jsonify({property: value})
		
	def cpu_temp(self):
		return self._jsonify("cpu_temp", self._health.cpu_temp())
	
	def cpu_clock(self):
		return self._jsonify("cpu_clock", self._health.cpu_clock())
	
	
# only for test
if __name__ == '__main__':
	nw_api = NetworkAPI(None)
	nw_api.start()
	
	import time
	starttime=time.time()
	while True:
		print "tick"
		time.sleep(60.0 - ((time.time() - starttime) % 60.0))
		
	