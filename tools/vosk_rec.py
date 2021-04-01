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
import time
from pydub import AudioSegment, silence #for detecting silence in audio file

class Decoder:
        def __init__(self, info):
                model = Model(os.getcwd()+"/modules/model")
                self.rec = KaldiRecognizer(model, 8000)
                self.ip, self.port = info["front"]

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
                HOST = self.ip
                PORT = self.port
                CHUNK = 32768
                FTOT = "./temp/recv.wav"
                FTEMP = "./temp/temp.wav"

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        print("trying to connect "+HOST+ " " +str(PORT))
                        s.connect((HOST, PORT))
                        print("connected")
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
                                        print("got data: "+len(data))
                                        temp.writeframesraw(data)
                                        temp.close()
                                        self.combine_files([FTOT, FTEMP])
                                        if(self.detectSilence(FTOT)): #2 seconds of silence detected
                                                s.send(b"MSTOP\0")
                                                time.sleep(1)
                                                s.close()
                                                break
                                        temp = wave.open(FTEMP, "wb")
                                        temp.setnchannels(1) #mono
                                        temp.setsampwidth(2)
                                        temp.setframerate(8000)
                                
                        except KeyboardInterrupt:
                                s.send(b"MSTOP\0")
                                time.sleep(1)
                                s.close()

                results = self.decode_file(FTOT) #get results from file
                print("FINAL RESULT from stream: "+results)
                return results

        def combine_files(self, files):
                data = []

                for infile in files:
                        w = wave.open(infile, "rb")
                        data.append( [w.readframes(w.getnframes())] )
                        w.close()

                output = wave.open(files[0], "wb")
                output.setnchannels(1) #mono
                output.setsampwidth(2)
                output.setframerate(8000)
                output.writeframes(data[0][0])
                output.writeframes(data[1][0])
                output.close()
                                                
        def detectSilence(self, fileName):
                myaudio = intro = AudioSegment.from_wav(fileName)
                dBFS = myaudio.dBFS
                pieces = silence.detect_silence(myaudio, min_silence_len=1000, silence_thresh=dBFS-4)
                pieces = [((start/1000),(stop/1000)) for start,stop in pieces] #convert to sec

                for i in pieces:
                        if i[1] - i[0] > 2:
                            print("big silence: "+str(i[0]) + " " + str(i[1]))
                            return True
                return False
