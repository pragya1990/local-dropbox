import socket
import os
import string
import socket
import fcntl
import struct
from processing_server_data import *
NO_OF_CLIENTS = 5
#SERVER_CONTROL_PORT = 8008


def get_ip_address():
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('www.google.com',0))
		ip = s.getsockname()[0]
		print (ip)
		return ip

def socket_program(ip):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
	port = input("Enter the port for control information in server:")

	rc = s.bind((ip, int(port)))
	if(rc == -1):
		print('server not able to bind')	
		exit()
	s.listen(NO_OF_CLIENTS)
	for i in range(5):
		pid = os.fork()	
	
	if(pid == 0):
		conn, addr = s.accept()
		print('Connected by', addr)	
		while (1):
			message = conn.recv(1024)
			print ('message received: ' + message)
			message = process_data_instance.process_data(message)
			conn.send(message)		
		conn.close()
	else:
		os.wait()

def check_if_server_exists():
	try:
		path = os.listdir(SERVER_PATH + SERVER_NAME + '/')
		print ('file exists')
	except OSError:
		print ('inside OSError ...making server directory')
		os.mkdir(SERVER_PATH + SERVER_NAME + '/')
		# making an empty client_list file
		fp = open(CLIENT_LIST_PATH,'a+')
		fp.close()

#def start_server_at_file_port(ip):
#	Handler = http.server.SimpleHTTPRequestHandler	
#	httpd = http.server.HTTPServer((ip, SERVER_FILE_PORT), Handler)
#	print ("\nserving at port for file transfer", SERVER_FILE_PORT)
#	httpd.serve_forever()	
		
def start_server_at_both_ports():
	ip = get_ip_address()
	#pid = os.fork()
	#if(pid == 0):
	#	os.chdir(SERVER_PATH + SERVER_NAME + '/')
	#	start_server_at_file_port(ip)
	#else:
	socket_program(ip)
	#os.wait()

process_data_instance = processing_server_data()
check_if_server_exists()
start_server_at_both_ports() # one port for control information, another for file transfer 
