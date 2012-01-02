import socket
import os
import string
import socket
import fcntl
import struct
import webbrowser
import sys
import urllib


#from urllib import *
from urllib import urlopen
import os, time

CLIENT_LIST_PATH = "/home/pragya/Documents/drop/apache_server/client_list"
SERVER_PATH = "/home/pragya/Documents/drop/"
SERVER_NAME = "apache_server"
SERVER_LOG_FILE_NAME = "server_log.txt"
SERVER_FILE_PORT = 8000

class processing_server_data():

	def __init__(self):	
		c=0

	def process_data(self,message):
		message_list = string.split(message)  # will change in python3
		if(message_list[0] == "id:"):
			self.check_if_client_exists(message_list[1])
			self.client_id = message_list[1]
			message = 'connected to client: ' + message_list[1]
			return message
		if(message_list[0] == "ip:"):
			self.client_ip = message_list[1]
			message = 'connected to client ip: ' + message_list[1]
			return message
		if(message_list[0] == "port:"):
			self.client_file_port = message_list[1]
			message = 'connected to client file port: ' + message_list[1]
			return message
		if(message_list[0] == "add:"):
			client_file_url = "http://" + self.client_ip + ":" + self.client_file_port + "/" + message_list[1]
			print("copying file: " + message_list[1])			
			download = urlopen(client_file_url).read()
			file_path = SERVER_PATH + SERVER_NAME + '/' + self.client_id + '/' + message_list[1]
			f = open(file_path,'wb')
			f.write(download)
			f.close()
			print ("send message to client that file has been successfully copied.. update its log")			
			exit()
	
	def check_if_client_exists(self,client_id):	
	
		fp = open(CLIENT_LIST_PATH,'r+')
		for line in fp:
			if(line == client_id):
				fp.close()			
				print ('client exists')			
				return 	
		# making a new client: (a) adding client_entry in client_list file (b) making a new folder for this client_id (c)make an empty server_log file inside this folder
		print('client does not exist..making the new client')
		fp.write(client_id) 
		fp.close()

		folder_name = SERVER_PATH + SERVER_NAME + '/' + client_id
		os.mkdir(folder_name)

		fp = open( folder_name + '/' + SERVER_LOG_FILE_NAME, 'a+')
		fp.close()
