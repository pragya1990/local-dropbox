import http.server
import socket
import fcntl
import struct
#WIRELESS_INTERFACE = 'eth1'
port = 8000

def start_server(wireless_logical_address):
	Handler = http.server.SimpleHTTPRequestHandler	
	httpd = http.server.HTTPServer((wireless_logical_address, port), Handler)

	print ("serving at port", port)
	httpd.serve_forever()

def get_ip_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('www.google.com',0))
	ip = s.getsockname()[0]
	print(ip)
	return ip	
	
wireless_logical_address = get_ip_address()
start_server(wireless_logical_address)	
