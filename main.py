#!/usr/bin/env python3 
import tools.vosk_rec as vosk_rec
import tools.sklearn_sims as sklearn_sims
#import modules.serial_comm as serial_comm
import modules.youtube_music as yt #remove this later , need for sending to front end
import tools.voice_synth as vs
import modules.module_loader as ml
import os #for recording, temporary usage
import time #for testing
from pygame import mixer
from parse import *

def main():
    decoder = vosk_rec.Decoder()
    voice = vs.VoiceSynth()
    classes = ml.class_builder()
    filename = "downSamp.wav"
    os.system("clear") #clearing out text from vosk intialization
    menu = ("enter \"reuse\" to use previous recording\n"
            "enter \"r\" to record for 10 seconds\n"
            "enter \"wifi\" to test the wifi functionality\n"
            "enter \"test\" to enter the testing menu\n"
            "enter \"exit\" to exit the program: ")

    while True:
        record = input(menu)
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
            msg, func, mod = sklearn_sims.compare_command(sentence, classes)
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
    voice.sendToFront(msg)
    if func: #we got a func back
        if mod in classes.keys(): #classes funcs should manipulate themselves
            func(classes[mod])
        else:
            func()

def local():
    rec_com = [ #commands for recording audio
        "echo \"recording for 10 seconds\"",
        "arecord -t wav -D \"hw:0,0\" -d 10 -f S16_LE -r 48000 temp.wav",
        "ffmpeg -i temp.wav -isr 48000 -ar 8000 downSamp.wav",
        "rm temp.wav",
        "clear",
        "echo \"done recording\"",
        ]

    try: #removing original recording file if it exists
        os.system("rm downSamp.wav")
    except:
        print(end = "")
    for i in rec_com:
        os.system(i)

def run_tests(decoder, voice, classes):
        t_range = ["1", "2", "3", "4", "5", "6"]
        t_menu = (            
                "TEST 1: \"set a timer for 3 seconds\"\n"
                "TEST 2: \"play the song country roads\"\n"
                "TEST 3: \"stop playing music\"\n"
                "TEST 4: \"what's the weather in denver\"\n"
                "TEST 5: \"start a stopwatch\"\n"
                "TEST 6: \"stop the stopwatch\"\n"
                "enter \"7\" to exit this menu\n"
                "Enter a test number for the test you would like to run: "
                )
        num = None

        os.system("clear")

        while True:
            num = input(t_menu).strip()
            if num in t_range:
                    f_name = os.getcwd()+"/tests/voice_files/file_"+num+".wav"
                    if num == "3":
                        mixer.init()
                        mixer.music.pause()
                    os.system("aplay "+f_name)
                    if num == "3":
                        mixer.music.unpause()
                    os.system("clear")
                    sentence = decoder.decode_file(f_name)
                    if sentence == "":
                        print("nothing detected within vosk")
                        continue
                    msg, func = sklearn_sims.compare_command(sentence, classes)
                    check_test(num, msg)
            elif num != "7":
                print(str(num)+" isn't a valid option!")
            else:
                break
            
def check_test(num, sentence):
        sentence = sentence.strip()

        if num == "1":
            print("EXPECTED: setting timer for 3 seconds")
            print("RETURNED: "+sentence)
            temp = "setting timer for 3 seconds" == sentence
            print("EQUAL: "+str(temp))
        if num == "2":
            print("EXPECTED: Song Country Roads will be played")
            print("RETURNED: "+sentence)
            temp = "Song Country Roads will be played" == sentence
            print("EQUAL: "+str(temp))
        if num == "3":
            print("EXPECTED: music is stopped")
            print("RETURNED: "+sentence)
            temp = "music is stopped" == sentence
            print("EQUAL: "+str(temp))
        if num == "4":
            print("EXPECTED: using city: denver Temperature in degrees Fahrenheit = x\n"
                        " atmospheric pressure in hPa unit = y\n"
                        " humidity in percentage = z\n"
                        " description = a")
            print("RETURNED: "+sentence)
            check = ("using city: denver Temperature in degrees Fahrenheit = {}"
                        " atmospheric pressure in hPa unit = {}"
                        " humidity in percentage = {}"
                        " description = {}")
            ret = parse(check, sentence)
            temp = ret is not None
            print("EQUAL: "+str(temp))
        if num == "5":
            print("EXPECTED: started a stopwatch")
            print("RETURNED: "+sentence)
            temp = "Started a stopwatch" == sentence
            print("EQUAL: "+str(temp))
        if num == "6":
            print("EXPECTED: stopwatch ran for x seconds")
            print("RETURNED: "+sentence)
            ret = parse("stopwatch ran for {} seconds", sentence)
            temp = ret is not None
            print("EQUAL: "+str(temp))
        print()

                
if __name__ == "__main__":
        main()
