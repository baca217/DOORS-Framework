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
                self.rec = KaldiRecognizer(model, 16000)

        def decode_file(self, aud_file):
                SetLogLevel(0)
                sentence = ""

                wf = wave.open(aud_file, "rb")
                if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                        print ("Audio aud_file must be WAV format mono PCM.")
                        exit (1)

                results = ""
                confidence = 0
                tot = 0

                while True:
                        data = wf.readframes(4000)
                        if len(data) == 0:
                                break
                        if self.rec.AcceptWaveform(data):
                                print(self.rec.Result())
                                results = json.loads(self.rec.Result())
                                print(results.items())
                                for i in results["result"]: #for some reason results sometimes isn't added to the dictionary. Need to figure out a work around
                                    confidence += i["conf"]
                                    tot += 1
                                sentence = sentence + results["text"]
                wf.close()        
                print("SENTENCE: "+sentence)
                print("conf: "+str(confidence))
                print("tot: "+str(tot))
                print("conf/tot: "+str(confidence/tot))
                #---------------------------------------------------------------
                #need to do some confidence checking here. 
                #temp2 = json.loads(temp["result"])
                #for i in temp["result"]:
                #       print(i["conf"])
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
                                        data = conn.recv(int(CHUNK/2))
                                        if not data: #didn't receive any data
                                                f.writeframesraw(holder)
                                                f.close()
                                                results = self.decode_file(fTot) #get results from file
                                                print("-----------------------------FINAL RESULT-----------------------------"+str(cur)+":"+results)
                                                break
                                        if data:
                                                holder += data #aggregating total voice data
                                                if len(holder) >= CHUNK:
                                                        fname = 'temp.wav'
                                                        temp = wave.open(fname, 'wb')
                                                        temp.setnchannels(1) #mono
                                                        temp.setsampwidth(2)
                                                        temp.setframerate(8000)
                                                        temp.writeframesraw(holder)
                                                        print("SIZE OF HOLDER AFTER WRITE"+str(len(holder)))
                                                        f.writeframesraw(holder)
                                                        temp.close
                                                        holder = b""

                                                        results = self.decode_file(fname)
                                                        print("results "+str(cur)+":"+results)
                                                        temp.close()
                                                        cur += 1
                                                else:
                                                        continue
