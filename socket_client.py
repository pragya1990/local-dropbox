import socket
import os
import time
import socket
import os
import string
import socket
import fcntl
import struct
CLIENT_FILE_PORT = 7050
CLIENT_ID_PATH = "/home/pragya/Documents/drop/client_id"
CLIENT_FOLDER_PATH = "/home/pragya/Documents/drop/client_files/"

class socket_client():

	def __init__(self):
		self.get_server_ip()
		self.get_client_ip()

	def socket_program(self):
		self.client_sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		port = raw_input("Enter port at which server is listening for control information:")
		connect_flag = 0
		while(1):
			try:		
				self.client_sockfd.connect((self.server_ip, int(port)))
				print ('Connected to server :)')
				break			
			except socket.error:
				if(connect_flag == 0):
					print('could not connect to port..sleeping for sometime')				
					connect_flag = 1				
				time.sleep(2)
		return self.client_sockfd

	def get_client_id(self):
		fp = open(CLIENT_ID_PATH,'r')
		client_id = fp.read()
		return client_id

	def get_client_ip(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('www.google.com',0))
		self.client_ip = s.getsockname()[0]

	# ****************************************** CHANGE THIS
	def get_server_ip(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('www.google.com',0))
		self.server_ip = s.getsockname()[0]
	# ****************************************** END

	def send_trigger_to_server(self, message):
		print ('sending message to server')		
		self.client_sockfd.send(message)
		message = self.client_sockfd.recv(1024)
		print ("message received: " + message)
	
	def start_client_at_both_ports(self):
		#pid = os.fork()
		#if(pid == 0):
		#	os.chdir(CLIENT_FOLDER_PATH)
			#self.open_client_port_for_file_transfer()
		#else:
		self.socket_program()
		message = "id:" + " " + self.get_client_id()
		print ('client_id: ' + message)				
		self.send_trigger_to_server(message)

		message = "ip:" + " " + self.client_ip
		self.send_trigger_to_server(message)

		message = "port:" + " " + str(CLIENT_FILE_PORT)
		self.send_trigger_to_server(message)

		#self.server_inst = client_processing_using_server_log()
		#self.server_inst.start_reading_from_server(self.server_ip, self.server_file_port)
		#os.wait()



	
			

	

