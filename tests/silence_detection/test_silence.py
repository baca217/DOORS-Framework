#!/usr/bin/env python3

import tools.vosk_rec as vr

def main():
    decode = vr.Decoder({"front" : ["127.0.0.1", 5555]})
    print(decode.detectSilence("silence.wav"))

if __name__ == "__main__":
    main()
