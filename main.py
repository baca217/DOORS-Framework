import sklearn_sims
import server
import vosk_rec
import info_digest
import local_commands as lc

def main():
    #ignoring for now, just gets in the way
    #server.listen_to_homie()
    filename = "downSamp.wav"
    rec_info = vosk_rec.decode_file(filename)
    sentence = info_digest.return_sentence(rec_info)
    sentence, results = sklearn_sims.compare_command(sentence)
    lc.check_command(results, sentence)

if __name__ == "__main__":
    main()
