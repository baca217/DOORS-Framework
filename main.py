import voice_rec
import sklearn_sims

def main():
    filename = "downSamp.wav"
    sentence = voice_rec.decode_file(filename)
    sklearn_sims.compare_command(sentence)

if __name__ == "__main__":
    main()
