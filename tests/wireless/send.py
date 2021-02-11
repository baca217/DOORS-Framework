#!/usr/bin/env python3
import socket
import sys
import time

def connect():
	SIZE = int(65536/2)
	#open file for sending
	f = open("downSamp.wav", "rb")
	binaryHeader = f.read(44)
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect the socket to the port where the server is listening
	server_address = ('127.0.0.1', 10000)
	print (sys.stderr, 'connecting to %s port %s' % server_address)
	sock.connect(server_address)
	
	size = 1
	while size > 0:
		read = f.read(SIZE)
		size = len(read)
		print(size)
		sock.send(read)
		time.sleep(1)
	sock.close()

def main():
	connect()

if __name__ == "__main__":
	main()
