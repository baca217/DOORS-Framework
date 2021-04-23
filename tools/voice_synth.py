#!/usr/bin/env python
import sys
sys.path.append("temp")

from subprocess import call
from os import system
import socket
import sys
import time

class VoiceSynth:
        
        def __init__(self):
                self.enabled = True

        def speak(self, sentence):
                if self.enabled:
                        comb = ""
                        for i in sentence:
                                comb += i
                        comb = comb.replace("\n", " ")
                        command = 'espeak \"{}\" --stdout |aplay 2>/dev/null'.format(comb)
                        system(command)
        def sendToFront(self, sentence): #still working on this
                fName = "./temp/voice.wav"
                temp = "./temp/vTemp.wav"
                comms = [
                        "rm "+fName,
                        "espeak -w "+temp+" -s 130 \""+sentence+"\"",  #converting msg to voice synth .wav file
                        "ffmpeg -i "+temp+" -ar 16000 "+fName, #downsampling .wav file for front-end
                        "rm "+temp, #removing the temp file
                        "clear"
                    ]

                if self.enabled == False:
                        print("voice synth not on. Will not send audio to front end")
                        return
                for i in comms:
                    try:
                        system(i)
                    except:
                        continue

        def enable(self):
                self.enabled = True
        
        def disable(self):
                self.enabled = False
