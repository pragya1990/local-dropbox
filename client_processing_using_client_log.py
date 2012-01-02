import os, time
import re
import socket
import fcntl
import struct
import string
from socket_client import *
names = {}
from client_processing_using_server_log import *
WIRELESS_INTERFACE = 'eth1'
CLIENT_LOG_FILE_PATH_NAME = "/home/pragya/Documents/drop/client_files/client_log.txt"
CLIENT_FILE_PATH = "/home/pragya/Documents/drop/client_files/"

class files_values():
	def __init__(self,time, client_approved = None, server_approved = None):
		print('inside file_values')
		print(client_approved)
		self.time = time		
		self.client_approved = client_approved
		self.server_approved = server_approved

class client_processing_using_client_log(socket_client, client_processing_using_server_log):
	def __init__(self):
		instance = socket_client()
		self.start_client_side_processing(instance)
		self.server_file_port = 8000
	
	def start_client_side_processing(self, instance):
		self.make_hash_using_log()
		self.open1(instance)

	def make_hash_using_log(self):
		print('inside make_hash_using_log')
		try:
			client_log_fp = open(CLIENT_LOG_FILE_PATH_NAME,'r')
		except:
			print('log file does not exist')
			return
	
		print('log file exists')
		for line in client_log_fp:
			try:		
				string_list = line.split(' ')
				abs_path = string_list[0]
				current_time = string_list[1] + ' ' + string_list[2] + ' ' + string_list[3] + ' ' + string_list[4] + ' ' + string_list[5]
				client_approved = int(string_list[6])	
				server_approved = int(string_list[7][0])
				names[abs_path] = files_values(current_time, client_approved, server_approved)
			except IndexError:
				print('index error occured')

		for val in names:
			print ('values in hash:\n' + str(val) + ' ' + str(names[val].time) + ' ' + str(names[val].client_approved) + ' ' + str(names[val].server_approved))
			

	def delete_entry_in_log_file(self,regex_old_line):

		print('inside delete entry in log file')
		log_list = []
		client_log_fp = open(CLIENT_LOG_FILE_PATH_NAME,'r')
		for line in client_log_fp:	
			log_list.append(line)
		for line in log_list:
			if(re.compile(regex_old_line+'.*').match(line)):
				log_list.remove(line)
				break
		client_log_fp.close()

		client_log_fp = open(CLIENT_LOG_FILE_PATH_NAME,'w')
		for line in log_list:
			client_log_fp.write(line)
		client_log_fp.close()

	def add_entry_in_log_file(self,abs_path):
	
		client_log_fp = open(CLIENT_LOG_FILE_PATH_NAME,'a+')

		new_line = str(abs_path) + ' ' + str(names[abs_path].time) + ' ' + str(names[abs_path].client_approved) + ' ' + str(names[abs_path].server_approved) + '\n'
		client_log_fp.write(new_line)
		client_log_fp.close()

	def check_files_to_deleted(self, instance):	
		
		files_to_be_deleted = []			
		for val in names:
			if(names[val].client_approved == 0):
				print ('\ndelete entry:\n' + str(val) + ' ' + str(names[val].time) + ' ' + str(names[val].client_approved) + ' ' + str(names[val].server_approved))
				files_to_be_deleted.append(val)
				
		for abs_path in files_to_be_deleted:
			regex_old_line = abs_path + ' ' + names[abs_path].time + ' '

			self.delete_entry_in_log_file(regex_old_line)
			print ('tell the server to delete this file, its entry in log and its hash from its database')
			del names[abs_path] # deleting entry in hash table

	def make_client_approved_invalid(self):
		for val in names.keys():
			names[val].client_approved = 0

	def check_values_for_correctness(self, file_path, current_file, instance, abs_path):
		
		print ('current file: ' + current_file)
		
		client_path = (string.split(abs_path,'/',6))[6]
		client_approved = 1
		server_approved = 0
		current_time = time.ctime(os.stat(abs_path).st_mtime)	
		try:
			if (names[client_path].time != current_time):
				regex_old_line = client_path + ' ' + names[client_path].time + ' '							
				print("time changed" + ' ' + abs_path + ' ' + current_time)
				names[client_path] = files_values(current_time, client_approved, server_approved)
								
				self.delete_entry_in_log_file(regex_old_line)
				self.add_entry_in_log_file(client_path)
					
			else: 				
				names[client_path].client_approved = 1				
		except KeyError:
			print("adding new name: ")						
			names[client_path] = files_values(current_time, client_approved, server_approved)
			print(str(client_path) + ' ' + str(names[client_path].time) + ' ' + str(names[client_path].client_approved) + ' ' + str(names[client_path].server_approved))
			self.add_entry_in_log_file(client_path)

		if( self.one_iteration_completed != 0 and names[client_path].server_approved == 0):
			message = "add: " + client_path
			print ('sending message: ' + message)
			instance.send_trigger_to_server(message)	
			print(message)
		else:
			print ('it did not enter this loop')
			print ("values: " + str(client_path) + ' ' + str(names[client_path].client_approved) + ' ' + str(names[client_path].server_approved))
			print ("iteration: " + str(self.one_iteration_completed))

	def open1(self, instance):
		self.one_iteration_completed = 0
		while(True):
			if(self.one_iteration_completed == 1):
				self.one_iteration_completed = 2
				instance.start_client_at_both_ports()

			self.make_client_approved_invalid()
			for file_path in os.walk(CLIENT_FILE_PATH):		
				for current_file in file_path[2]:
					abs_path = os.path.join(file_path[0], current_file)
					if(abs_path == CLIENT_LOG_FILE_PATH_NAME):		
						continue					

					self.check_values_for_correctness(file_path, current_file, instance, abs_path)

			self.check_files_to_deleted(instance) #these are the files that no longer exist in the client database and should be deleted
			if(self.one_iteration_completed == 0):
				self.one_iteration_completed = 1
			time.sleep(1)

	

