#!/usr/bin/env python3
import socket
import sys
import modules.vosk_rec as vr

#192.168.0.5

def main():
	decoder = vr.Decoder()
	decoder.listen_stream()
	#connect()
	#listen()

def connect():
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect the socket to the port where the server is listening
	server_address = ('192.168.0.5', 10000)
	print (sys.stderr, 'connecting to %s port %s' % server_address)
	sock.connect(server_address)
	sock.send(b"Hello world!")	

def listen():	
	HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
	PORT = 10000        # Port to listen on (non-privileged ports are > 1023)
	f = open("recv.wav", "wb")
	decoder = vr.Decoder()

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		conn, addr = s.accept()
		with conn:
			print('Connected by', addr)
			data = conn.recv(1024)
			if not data:
				print("no data received, exiting")
				f.close()
			if data:	
				decoder.decode_stream(sock, data)

			"""
			while True:
				data = conn.recv(1024)
				if not data:
					f.close()
					break
				if data:
					print(data)
					f.write(data)
			"""
				


if __name__ == "__main__":
	main()
