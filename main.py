#!/usr/bin/env python3 
import modules.vosk_rec as vosk_rec
import modules.info_digest as info_digest
import modules.sklearn_sims as sklearn_sims
import modules.local_commands as local_commands
import modules.serial_comm as serial_comm
import os #for recording, temporary usage

def main():
    decoder = vosk_rec.Decoder()
    filename = "downSamp.wav"
    stopwatch = local_commands.Stopwatch()
    #ignoring for now, just gets in the way
    #just the wifi socket communication we'll do later
    #server.listen_to_homie)
    os.system("clear")
    while True:
        print("enter \"reuse\" to use previous recording")
        record = input("enter \"r\" to record for 10 seconds\nenter \"exit\" to exit the program: ")
        record = record.strip().lower()
        if(record == "exit"):
            exit()
        elif(record == "r"):
            os.system("rm downSamp.wav")
            os.system("./rec_resamp.sh")
            os.system("clear")
        elif(record == "serial"):
            serial_comm.rec_data()
        elif(record != "reuse"):
            print(record,"is not an option \n")
            continue
        rec_info = decoder.decode_file(filename)
        sentence = info_digest.return_sentence(rec_info)
        print("vosk sentence: "+sentence)
        sentence, result = sklearn_sims.compare_command(sentence)
        if(sentence == -1):
            print()
            continue
        elif(result == ""):
            print("\nNo command match was found\n")
            continue
        local_commands.check_command(result, sentence, stopwatch)
        print()


if __name__ == "__main__":
    main()
