#!/usr/bin/env python3 
import sys
sys.path.append('tools')
sys.path.append('modules')

import vosk_rec as vosk_rec
import sklearn_sims as sklearn_sims
#import modules.serial_comm as serial_comm
import voice_synth as vs
import module_loader as ml
from tests.main_tests.main_test import run_tests
import os #for recording, temporary usage
import time #for testing
from pygame import mixer
from parse import *
import socket
import time
import pathlib

def main():
    voice = vs.VoiceSynth()
    decoder = vosk_rec.Decoder()
    classes = ml.class_builder()
    os.system("clear") #clearing out text from vosk intialization
    menu = ("enter \"reuse\" to use previous recording\n"
            "enter \"r\" to record for 10 seconds\n"
            "enter \"test\" to enter the testing menu\n"
            "enter \"exit\" to exit the program: ")

    while True:
        record = input(menu)
        print()
        record = record.strip().lower()
        msg = ""
        func = None
        
        if(record == "exit"):
            exit()
        elif(record == "r" or record == "reuse"):
            if record == "r": #do a local recording
                local()
                sentence = decoder.decode_file(filename)
            elif record == "reuse": #reuse previous recording
                sentence = decoder.decode_file(filename)
            else:
                print("that shouldn't have happened: "+record)
                exit()
            print("vosk sentence: "+sentence)
            run_results(msg, func, mod, classes, voice)
        elif(record == "test"):
            run_tests(decoder, voice, classes)
        else:
            print(record,"is not an option \n")

def run_results(msg, func, mod, classes, voice):
    print(msg)
    voice.sendToFront(msg)
    if func: #we got a func back
        if mod in classes.keys(): #classes funcs should manipulate themselves
            func(classes[mod])
        else:
            time.sleep(2)
            func()

def local(): #function for recording and testing locally
    rec_com = [ #commands for recording audio
        "echo \"recording for 10 seconds\"",
        "arecord -t wav -D \"hw:2,0\" -d 10 -f S16_LE -r 48000 {}/temp/temp.wav".format(info["path"]),
        "ffmpeg -i {}/temp/temp.wav -isr 48000 -ar 8000 {}/temp/downSamp.wav".format(info["path"],info["path"]),
        "rm {}/temp/temp.wav".format(info["path"]),
        "clear",
        "echo \"done recording\"",
        ]

    try: #removing original recording file if it exists
        os.system("rm downSamp.wav")
    except:
        print(end = "")
    for i in rec_com:
        os.system(i)
                
if __name__ == "__main__":
        main()
