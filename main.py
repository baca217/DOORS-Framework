import sklearn_sims
import server
import vosk_rec
import info_digest
import match_execute

def main():
    #ignoring for now, just gets in the way
    #server.listen_to_homie()
    filename = "downSamp.wav"
    rec_info = vosk_rec.decode_file(filename)
    sentence = info_digest.return_sentence(rec_info)
    results = sklearn_sims.compare_command(sentence)
    match_execute.execute_command(results)

if __name__ == "__main__":
    main()
