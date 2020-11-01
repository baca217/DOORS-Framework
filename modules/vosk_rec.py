#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import json

class Decoder:
    def __init__(self):
        model = Model("modules/model")
        self.rec = KaldiRecognizer(model, 8000)

    def decode_file(self, aud_file):
        SetLogLevel(0)

        wf = wave.open(aud_file, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print ("Audio aud_file must be WAV format mono PCM.")
            exit (1)

        results = []
        
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if self.rec.AcceptWaveform(data):
                results.append(self.rec.Result())
 
        for i in results:
            y = json.loads(i)
            print(y["text"])
        return results
