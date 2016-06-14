from http.server import BaseHTTPRequestHandler, HTTPServer

class HTTPRequestHandler(BaseHTTPRequestHandler):

	 # def do_POST(self):
		#  if None != re.search('/api/v1/addrecord/*',self.path):
		#  ctype,pdict = cgi.parse_headerself.headers.getheader('content-type'))
		#  if ctype == 'application/json':
		#  length = intself.headers.getheader('content-length'))
		#  data = cgi.parse_qsself.rfile.read(length), keep_blank_values=1)
		#  recordID =self.path.split('/')[-1]
		#  LocalData.records[recordID] = data
		#  print "record %s is added successfully" % recordID
		#  else:
		#  data = {}
		 
		# self.send_response(200)
		# self.end_headers()
		#  else:
		# self.send_response(403)
		# self.send_header('Content-Type', 'application/json')
		# self.end_headers()
		 
		# return
		 
	# get from ioT server
	def do_GET(self):
		url =self.path
		result, message =self.process_request(url)

		 # SEND response status code
		if result:
			self.send_response(200)
		else:
			self.send_response(400)

		 # Send headers
		self.send_header('Content-type', 'text/html')
		self.end_headers()

		 # Write content as utf-8 data
		self.car_node.get_graph_services().log_trace(debug,
				 "CarNode:ServerRequestHandler: Returning following response to client: {0}".format(message))
		self.wfile.write(bytes(message, "utf8"))
		return

	def process_request(self, url):
		parsed_url      = urlparse(url)
		parsed_params   = parse_qs(parsed_url.query)
		split_path      = parsed_url.path.split('/')

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
				#					 																															#
				#																																				#
				#########################################################################
					# get response from above code
					if response['result'] == 'success':
						success= True
						json_response['query_status'] = 'success'
						json_response['status'] = {
												'action':'change',
												'frequency': frequency
												}
					elif response['result'] == 'error':
						success = False
						json_response['query_status'] = 'failed'
					else:
						success = False
						json_response['query_status'] = 'failed'
						json_response['description'] = 'Request timed out'
				else:
					return False, self.error_invalid_parameter # no tv frequency precise

class HttpServer:
	def connect_server(self):
			HandlerClass = BlogofileRequestHandler
			ServerClass = http.server.HTTPServer
			self.httpd = ServerClass(('10.3.31.255', 8080), HandlerClass)

	def start_server(self):
		self.server.serve_forever()

	def stop_server(self):
		self.server.shutdown()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='HTTP Server')
	parser.add_argument('port', type=int, help='Listening port for HTTP Server')
	parser.add_argument('ip', help='HTTP Server IP')
	args = parser.parse_args()

	server = SimpleHttpServer(args.ip, args.port)
	print 'HTTP Server Running...........'
	server.start()
	server.waitForThread()
	



