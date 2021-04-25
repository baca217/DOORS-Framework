#!/usr/bin/env python3

import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import json

class Decoder:

    def __init__(self):
        self.q = queue.Queue()
        self.device = None
        try:
            model = "tools/model" #setting model location
            if not os.path.exists(model):
                print ("Please download a model for your language from https://alphacephei.com/vosk/models")
                print ("and unpack as 'model' in the tools folder.")
                exit(0)
            device_info = sd.query_devices(self.device, 'input')
            # soundfile expects an int, sound device provides a float:
            self.samplerate = int(device_info['default_samplerate'])
            model = vosk.Model(model)
            self.rec = vosk.KaldiRecognizer(model, self.samplerate) 
        except Exception as e:
            print("EXCEPTION : {}".format(e))
            exit(0)

    def callback(self, indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status, file=sys.stderr)
            self.q.put(bytes(indata))

    def run(self):
        with sd.RawInputStream(samplerate=self.samplerate, blocksize = 16000, device=self.device,
                        dtype='int16',channels=1, callback=self.callback):
            while True:
                data = self.q.get()
                if self.rec.AcceptWaveform(data):
                    res = self.rec.Result()
                    results = json.loads(res)
                    size = len(results["text"])
                    print("TEXT: {}\nLEN: {}".format(results["text"], size))
                    if size > 0:
                        return results["text"]

        


def main():
    test = Decoder()
    test.run()

if __name__ == "__main__":
    main()
