#!/usr/bin/env python3 
import modules.vosk_rec as vosk_rec
import modules.sklearn_sims as sklearn_sims
import modules.local_commands as local_commands
import modules.serial_comm as serial_comm
import modules.voice_synth as vs
import os #for recording, temporary usage

def main():
        decoder = vosk_rec.Decoder()
        voice = vs.VoiceSynth()
        filename = "downSamp.wav"
        stopwatch = local_commands.Stopwatch()
        #ignoring for now, just gets in the way
        #just the wifi socket communication we'll do later
        #server.listen_to_homie)
        os.system("clear") #clearing out text from vosk intialization
        menu = ("enter \"reuse\" to use previous recording\n"
                "enter \"r\" to record for 10 seconds\n"
                "enter \"test\" to enter the testing menu\n"
                "enter \"exit\" to exit the program: ")
        while True:
                record = input(menu)
                print()
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

                elif(record == "serial"):
                        serial_comm.rec_data()
                elif(record == "reuse"):
                        sentence = decoder.decode_file(filename)
                        print("vosk sentence: "+sentence)
                        sentence, result = sklearn_sims.compare_command(sentence)
                        if(sentence == -1):
                                print()
                                continue
                        elif(result == ""):
                                print("\nNo command match was found\n")
                                continue
                        local_commands.check_command(result, sentence, stopwatch, voice)
                elif(record == "test"):
                        testing()
                else:
                        print(record,"is not an option \n")
                print()
        return 0
 
def testing():
        message = ("TEST 1: set a timer for 3 seconds\n"
                "TEST 2: play the song country roads\n"
                "TEST 3: playing music\n"
                "TEST 4: what's the weather in denver\n"
                "TEST 5: start a stopwatch\n"
                "TEST 6: stop the stopwatch"
                "Enter test number: ")
        input(message)
    

if __name__ == "__main__":
                main()
