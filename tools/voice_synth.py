#!/usr/bin/env python

from subprocess import call
from os import system

class VoiceSynth:
	enabled = True
	
#	def __init__(self):
#		enabled = True

	def speak(self, sentence):
		if self.enabled:
			comb = ""
			for i in sentence:
				comb += i
			comb = comb.replace("\n", " ")
			command = 'espeak \"{}\" --stdout |aplay 2>/dev/null'.format(comb)
			system(command)
        def sentToFront(self, sentence): #still working on this
                SIZE = int(65536/2)
                #open file for sending
                f = open("Song.wav", "rb")
                binaryHeader = f.read(44) #remove .wav header info for raw format
                # Create a TCP/IP socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Connect the socket to the port where the server is listening
                server_address = ('192.168.43.151', 5555)
                print (sys.stderr, 'connecting to %s port %s' % server_address)
                sock.connect(server_address)
                sock.send(b"APCKT\0")
                size = 1
                while size > 0:
                        read = f.read(SIZE)
                        size = len(read)
                        print(size)
                        sock.send(read)
                sock.close()

	def enable(self):
		self.enabled = True
	
	def disable(self):
		self.enabled = False
