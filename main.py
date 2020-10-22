import modules.vosk_rec as vosk_rec
import modules.info_digest as info_digest
import modules.sklearn_sims as sklearn_sims
import modules.local_commands as local_commands
import os #for recording, temporary usage
from pygame import mixer

def main():
    decoder = vosk_rec.Decoder()
    filename = "downSamp.wav"
    stopwatch = local_commands.Stopwatch()
    mixer.init()
    #ignoring for now, just gets in the way
    #server.listen_to_homie()
    while True:
        print("enter \"reuse\" to use previous recording")
        record = input("enter \"r\" to record for 10 seconds\nenter \"exit\" to exit the program: ")
        record = record.strip().lower()
        if(record == "exit"):
            exit()
        elif(record == "r"):
            os.system("./rec_resamp.sh")
        elif(record != "reuse"):
            print(record,"is not an option")
            continue
        rec_info = decoder.decode_file(filename)
        sentence = info_digest.return_sentence(rec_info)
        sentence, results = sklearn_sims.compare_command(sentence)
        local_commands.check_command(results, sentence, stopwatch)


if __name__ == "__main__":
    main()
