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
		self.app.add_url_rule(rule="/v1.0/query/<string:meth>", view_func=self.controller, methods=['GET'])
		
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
		
	def controller(self, meth):
		# illegal 
		if (meth.startswith("_")):
			logging.debug("attempt to call function with \"_\"")
			return self.wrong_request()

		function_name = "query_" + meth
		try:
			method = getattr(self._health, function_name)
		except AttributeError:
			logging.debug("attempt to call unknown function \"" + function_name + "\"")
			return self.wrong_request()
			
		logging.debug("calling function \"" + function_name + "\"")
		return self._jsonify( meth, method())

# only for test
if __name__ == '__main__':
	nw_api = NetworkAPI(None)
	nw_api.start()
	
	import time
	starttime=time.time()
	while True:
		print "tick"
		time.sleep(60.0 - ((time.time() - starttime) % 60.0))
		
	