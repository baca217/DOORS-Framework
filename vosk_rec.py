#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import json

def decode_file(f_rec):
    SetLogLevel(0)

    wf = wave.open(f_rec, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)

    model = Model("model")
    rec = KaldiRecognizer(model, wf.getframerate())
    results = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            results.append(rec.Result())

    print("Final Result: ", rec.FinalResult())

    for i in results:
        y = json.loads(i)
        print(y["result"])
        print(y["text"])
    return results
