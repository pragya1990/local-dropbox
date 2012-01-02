import os, time
import re
import socket
import fcntl
import struct
import string
import webbrowser
import sys
import urllib
from urllib import *
from socket_client import *

SERVER_LOG_FILE_NAME = "server_log.txt"

class client_processing_using_server_log():
	def __init__(self):
		c = 0

	def start_reading_from_server(self, server_ip, server_file_port):
		
		server_log_path = 'http://' + server_ip + ':' + server_file_port + '/' + 'sample.txt'
		server_log_fp = urlopen(server_log_path)
		for line in server_log_fp:
			print(line)
