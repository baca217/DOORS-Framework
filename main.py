#!/usr/bin/env python3 
import modules.vosk_rec as vosk_rec
import modules.sklearn_sims as sklearn_sims
import modules.local_commands as local_commands
import modules.serial_comm as serial_comm
import modules.voice_synth as vs
import os #for recording, temporary usage
import time #for testing
from pygame import mixer
from parse import *

def main():
    decoder = vosk_rec.Decoder()
    voice = vs.VoiceSynth()
    voice.disable()
    filename = "downSamp.wav"
    stopwatch = local_commands.Stopwatch()
    os.system("clear") #clearing out text from vosk intialization
    menu = ("enter \"reuse\" to use previous recording\n"
            "enter \"r\" to record for 10 seconds\n:"
            "enter \"test\" to enter the testing menu\n"
            "enter \"exit\" to exit the program: ")
    while True:
        record = input(menu)
        record = record.strip().lower()
        if(record == "exit"):
            exit()
        elif(record == "r"):
            os.system("rm downSamp.wav")
            os.system("./modules/rec_resamp.sh")
            os.system("clear")

            sentence = decoder.decode_file(filename)
            print("vosk sentence: "+sentence)
            sentence, result = sklearn_sims.compare_command(sentence)
            if(sentence == -1):
                print("\n error occurred\n")
                continue
            elif(result == ""):
                print("\nNo command match was found\n")
                continue
            local_commands.check_command(result, sentence, stopwatch, voice)

#        elif(record == "serial"):
#            serial_comm.rec_data()

        elif(record == "reuse"):
            sentence = decoder.decode_file(filename)
            print("vosk sentence: "+sentence)
            sentence, result = sklearn_sims.compare_command(sentence)
            if(sentence == -1):
                continue
            elif(result == ""):
                print("\nNo command match was found\n")
                continue
            local_commands.check_command(result, sentence, stopwatch, voice)
        
        elif(record == "test"):
            run_tests(decoder, voice, stopwatch)

        else:
            print(record,"is not an option \n")
        print()

def run_tests(decoder, voice, stopwatch):
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
                    sentence, result = sklearn_sims.compare_command(sentence)
                    if(sentence == -1):
                        continue
                    elif(result == ""):
                        print("\nNo command match was found\n")
                        continue
                    ret = local_commands.check_command(result, sentence, stopwatch, voice)
                    check_test(num, ret)
            elif num != "7":
                print(str(num)+" isn't a valid option!")
            else:
                break
            
def check_test(num, sentence):
        sentence = sentence.strip()

        print("\nExpected == Returned")
        if num == "1":
            print("\"setting timer for 3 seconds\" == "+sentence+": ", end='')
            print("setting timer for 3 seconds" == sentence)
        if num == "2":
            print("\"Song Country Roads will be played\" == "+sentence+": ", end='')
            print("Song Country Roads will be played" == sentence)
        if num == "3":
            print("\"music is stopped\" == "+sentence+": ", end ='')
            print("music is stopped" == sentence)
        if num == "4":
            msg = ("\"using city:   denver Temperature in degrees Fahrenheit = x\n"
                        " atmospheric pressure in hPa unit = y\n"
                        " humidity in percentage = z\n"
                        " description = a\"\n == \n"+sentence+": ")
            print(msg, end='')
            check = ("using city:   denver Temperature in degrees Fahrenheit = {}"
                        " atmospheric pressure in hPa unit = {}"
                        " humidity in percentage = {}"
                        " description = {}")
            ret = parse(check, sentence)
            print(ret is not None)

        if num == "5":
            print("\"Started a stopwatch\" == "+sentence+": ", end='')
            print("Started a stopwatch" == sentence)
        if num == "6":
            print("\"stopwatch ran for x seconds\" == "+sentence+": ", end='')
            ret = parse("stopwatch ran for {} seconds", sentence)
            print(ret is not None)
        print()


                
if __name__ == "__main__":
        main()
