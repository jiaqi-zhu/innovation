# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from urlparse import *
import urllib, json
import db

PORT = 8000
# ADDRESS = 'localhost'
ADDRESS = '10.3.28.189'

class HTTPRequestHandler(BaseHTTPRequestHandler):
	error_invalid_url = json.dumps({
	 'query_status' : 'error',
	 'error_code' : '3',
	 'description' : 'Syntax error: The URL requested is invalid'})

	# get from hu
	def do_GET(self):
		url = self.path
		if url != '/favicon.ico':
			res, data = self.process_request(url)
			if res:
				self.send_response(200)
			else:
				self.send_response(400)

			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(bytes(data))
		return 

	def process_request(self, url):
		parsed_url      = urlparse(url)
		parsed_params   = parse_qs(parsed_url.query)
		split_path      = parsed_url.path.split('/')
		json_response = {}
	 # validate url
		try:
		 # get rid of empty path part
			split_path.pop(0)
			api     = split_path.pop(0)
			service = split_path.pop(0)
			action  = split_path.pop(0)
		except IndexError:
		 	return False, self.error_invalid_url

		if service == 'radio':
			if action == 'change':
				if 'frequency' in parsed_params:
					frequency = parsed_params['frequency'][0]

				################# connect to hu and change frequency ####################
				#					 													                                    #
				#																		                                    #
				#########################################################################
					# get response from above code
					# if response['result'] == 'success':
					success= True
					json_response['query_status'] = 'success'
					json_response['status'] = {
											'action':'change',
											'frequency': frequency
											}
					# elif response['result'] == 'error':
					# 	success = False
					# 	json_response['query_status'] = 'failed'
					# else:
					# 	success = False
					# 	json_response['query_status'] = 'failed'
					# 	json_response['description'] = 'Request timed out'
					return success, json.dumps(json_response)
				else:
					return False, self.error_invalid_parameter # no tv frequency precise

class HttpServer:
	def __init__(self, address, port):
		HandlerClass = HTTPRequestHandler
		ServerClass = BaseHTTPServer.HTTPServer
		self.httpd = ServerClass((address, port), HTTPRequestHandler)

	def start_server(self):
		self.httpd.serve_forever()

	def stop_server(self):
		self.httpd.server_close()

if __name__ == '__main__':

	server = HttpServer(ADDRESS, PORT)
	print 'HTTP Server Running...........'
	try:
		server.start_server()
	except KeyboardInterrupt:
		server.stop_server()
		print "HTTP Server stopped"

	



