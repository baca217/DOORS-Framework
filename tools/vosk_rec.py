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
from pydub import AudioSegment, silence #for detecting silence in audio file

class Decoder:
        def __init__(self):
                model = Model(os.getcwd()+"/modules/model")
                self.rec = KaldiRecognizer(model, 8000)

        def decode_file(self, aud_file):
                SetLogLevel(0)
                sentence = ""
                results = ""
                confidence = 0
                tot = 0

                wf = wave.open(aud_file, "rb")
                if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE": #checking certain file characteristics
                        print ("Audio aud_file must be WAV format mono PCM.")
                        exit (1)

                
                while True: #loop for doing voice recognition
                        data = wf.readframes(4000)
                        if len(data) == 0: #done reading audio file
                                break
                        if self.rec.AcceptWaveform(data): #finished recognition on segment of audio file
                                items = self.rec.Result()
                                results = json.loads(items)
                                if len(results.items()) > 1: #false recognition, sometimes nothing is detected
                                        for i in results["result"]: 
                                            confidence += i["conf"]
                                            tot += 1
                                        sentence = sentence + " " + results["text"]
                                else:
                                        print(self.rec.PartialResult())
                f_res = json.loads(self.rec.FinalResult())
                if len(f_res.items()) > 1:
                    return f_res["text"]
                wf.close()                        
                if tot > 0 and confidence/tot > .8: #checking confidence of recognition
                        return sentence.lower().strip()
                elif tot > 0:
                        print("confidence too low: "+str(confidence/tot))
                return ""

        def listen_stream(self):
                HOST = '192.168.43.125'  # Standard loopback interface address (localhost)
                PORT = 5555        # Port to listen on (non-privileged ports are > 1023)
                CHUNK = int(65536/2)
                FTOT = "recv.wav"
                FTEMP = "temp.wav"

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        print("trying to connect "+HOST+ " " +str(PORT))
                        s.connect((HOST, PORT))
                        print("connected")
#                        s.send(b"MSTRM\0")
                        tot = wave.open(FTOT, 'wb')
                        tot.setnchannels(1) #mono
                        tot.setsampwidth(2)
                        tot.setframerate(8000)
                        tot.close()

                        temp = wave.open(FTEMP, 'wb')
                        temp.setnchannels(1) #mono
                        temp.setsampwidth(2)
                        temp.setframerate(8000)
                        try:
                                while True:                        
                                        data = s.recv(CHUNK)
                                        print("got data "+str(len(data)))
                                        temp.writeframesraw(data)
                                        temp.close()
                                        self.combine_files([FTOT, FTEMP])
                                        if(self.detectSilence(FTOT)): #3 seconds of silence detected
                                                s.send(b"MSTOP\0")
                                                s.close()
                                                break
                                        temp = wave.open(FTEMP, "wb")
                                        temp.setnchannels(1) #mono
                                        temp.setsampwidth(2)
                                        temp.setframerate(8000)
                        except KeyboardInterrupt:
                                input("send MSTOP")
                                s.send(b"MSTOP\0")
                                input("close socket")
                                s.close()

                results = self.decode_file(FTOT) #get results from file
                print("FINAL RESULT from stream: "+results)
                return results

        def combine_files(self, files):
                data = []

                for infile in files:
                        w = wave.open(infile, "rb")
                        data.append( [w.getparams(), w.readframes(w.getnframes())] )
                        w.close()

                output = wave.open(files[0], "wb")
                output.setnchannels(1) #mono
                output.setsampwidth(2)
                output.setframerate(8000)
                output.writeframes(data[0][1])
                output.writeframes(data[1][1])
                output.close()
                                                
        def detectSilence(self, fileName):
                myaudio = intro = AudioSegment.from_wav(fileName)
                dBFS = myaudio.dBFS
                pieces = silence.detect_silence(myaudio, min_silence_len=1000, silence_thresh=dBFS-8)
                pieces = [((start/1000),(stop/1000)) for start,stop in pieces] #convert to sec

                print(pieces)
                for i in pieces:
                        if i[1] - i[0] > 3:
                            print("big silence: "+str(i[0]) + " " + str(i[1]))
                            return True
                return False
