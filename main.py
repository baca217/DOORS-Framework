#!/usr/bin/env python3 
import tools.vosk_rec as vosk_rec
import tools.sklearn_sims as sklearn_sims
#import modules.serial_comm as serial_comm
import tools.voice_synth as vs
import tools.front_info as fi
import modules.module_loader as ml
from tests.main_tests.main_test import run_tests
import os #for recording, temporary usage
import time #for testing
from pygame import mixer
from parse import *
import socket

def main():
    info = fi.get_fe_info()
    voice = vs.VoiceSynth(info)
    decoder = vosk_rec.Decoder(info)
    classes = ml.class_builder()
    filename = "./temp/downSamp.wav"
    os.system("clear") #clearing out text from vosk intialization
    menu = ("enter \"reuse\" to use previous recording\n"
            "enter \"r\" to record for 10 seconds\n"
            "enter \"wifi\" to test the wifi functionality\n"
            "enter \"test\" to enter the testing menu\n"
            "enter \"exit\" to exit the program: ")

    while True:
        print()
        record = input(menu)
        print()
        record = record.strip().lower()
        msg = ""
        func = None
        
        if(record == "exit"):
            exit()
        elif(record == "r" or record == "wifi" or record == "reuse"):
            if record == "r": #do a local recording
                local()
                sentence = decoder.decode_file(filename)
            elif record == "wifi": #test using wifi capability
                sentence = decoder.listen_stream()
            elif record == "reuse": #reuse previous recording
                sentence = decoder.decode_file(filename)
            else:
                print("that shouldn't have happened: "+record)
                exit()
            print("vosk sentence: "+sentence)
            if sentence == "":
                send_error(info)
                continue
            elif sentence == "stop":
                send_stop(info)
                continue
            else:
                msg, func, mod = sklearn_sims.compare_command(sentence, classes, info)
            run_results(msg, func, mod, classes, voice)
#code below is for serial communication
#        elif(record == "serial"):
#            serial_comm.rec_data()
        elif(record == "test"):
            run_tests(decoder, voice, classes)
        else:
            print(record,"is not an option \n")

def run_results(msg, func, mod, classes, voice):
    print(msg)
    #voice.sendToFront(msg)
    if func: #we got a func back
        if mod in classes.keys(): #classes funcs should manipulate themselves
            func(classes[mod])
        else:
            func()

def local(): #function for recording and testing locally
    rec_com = [ #commands for recording audio
        "echo \"recording for 10 seconds\"",
        "arecord -t wav -D \"hw:2,0\" -d 10 -f S16_LE -r 48000 ./temp/temp.wav",
        "ffmpeg -i ./temp/temp.wav -isr 48000 -ar 8000 ./temp/downSamp.wav",
        "rm ./temp/temp.wav",
        "clear",
        "echo \"done recording\"",
        ]

    try: #removing original recording file if it exists
        os.system("rm downSamp.wav")
    except:
        print(end = "")
    for i in rec_com:
        os.system(i)

def send_error(info): #send error for
    CHUNK = int(65536/2)
    IP, PORT = info["front"]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (IP, PORT)
    print ('connecting to {} port {}\n'.format(IP, PORT))
    sock.connect(server_address)
    sock.sendall(b"VRERR\0")
    sock.close()

def send_stop(info):
    CHUNK = int(65536/2)
    IP, PORT = info["front"]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (IP, PORT)
    print ('connecting to {} port {}\n'.format(IP, PORT))
    sock.connect(server_address)
    sock.sendall(b"CANCL\0")
    sock.close()
                
if __name__ == "__main__":
        main()
