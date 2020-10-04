import sklearn_sims
import server
import vosk_rec
import info_digest

def main():
    #ignoring for now, just gets in the way
    #server.listen_to_homie()
    filename = "recv.wav"
    rec_info = vosk_rec.decode_file(filename)
    sentences = info_digest.return_sentences(rec_info)
    sklearn_sims.compare_command(sentences)

if __name__ == "__main__":
    main()
