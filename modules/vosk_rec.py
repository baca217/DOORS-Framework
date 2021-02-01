#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import socket
import os
import wave
import json
import struct
import math
import random
import wave

class Decoder:
	def __init__(self):
		model = Model(os.getcwd()+"/modules/model")
		self.rec = KaldiRecognizer(model, 8000)

	def decode_file(self, aud_file):
		SetLogLevel(0)
		sentence = ""

		wf = wave.open(aud_file, "rb")
		if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
			print ("Audio aud_file must be WAV format mono PCM.")
			exit (1)

		results = ""

		while True:
			data = wf.readframes(4000)
			if len(data) == 0:
				break
			if self.rec.AcceptWaveform(data):
				results += self.rec.Result()
		print("RESULTS:",results,"\n")
		temp = json.loads(results)
		print(temp["text"])
		#---------------------------------------------------------------
		#need to do some confidence checking here. 
		#temp2 = json.loads(temp["result"])
		#for i in temp["result"]:
		#	print(i["conf"])
		sentence = temp["text"]
		return sentence

	def listen_stream(self):
		HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
		PORT = 10000        # Port to listen on (non-privileged ports are > 1023)
		CHUNK = 65536
		f = open("recv.wav", "wb")

		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((HOST, PORT))
			print("Listening on port: "+str(PORT))
			s.listen()
			conn, addr = s.accept()
			with conn:
				fTot = 'tot.wav' #file that will hold all audio received
				f = wave.open(fTot, 'wb')
				f.setnchannels(1) #mono
				f.setsampwidth(2)
				f.setframerate(8000)
				f.close
				holder = b"" #temporary holder for chunk of audio recognition
				while True:
					cur = 1
					data = conn.recv(1024)
					print("received "+str(len(data))+" bytes")
					if not data:
						f.close()
						results = self.decode_file(fTot)
						print("results"+cur+":"+results)
						break
					if data:
						holder += data
						if len(holder) >= CHUNK:
							fname = 'temp.wav'
							temp = wave.open(fname, 'wb')
							temp.setnchannels(1) #mono
							temp.setsampwidth(2)
							temp.setframerate(8000)
							temp.writeframesraw(holder)
							f.writeframesraw(holder)
							temp.close
							holder = b""

							results = self.decode_file(fname)
							print("results "+cur+":"+results)
							temp.close()
						else:
							continue


		
		"""
		while true:
		    obj = wave.open(fname, 'wb')
		    obj.setchannels(1) #mono
		    obj.setsampwidth(2)
		    obj.setframerate(8000)
		    obj.writeframesraw(socket.read(1024))
		    obj.close
		    results = self.decode_file(fname)
		    print("results "+cur+":"+results)
		    cur += 1
		"""
