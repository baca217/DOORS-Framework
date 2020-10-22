import vosk_rec as vr

def main():
    rec = vr.Decoder()
    rec.decode_file("downSamp.wav")

if __name__ == "__main__":
    main()
