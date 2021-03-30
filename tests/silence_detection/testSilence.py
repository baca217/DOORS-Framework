#!/usr/bin/env python3

import tools.vosk_rec as vr

def main():
    decoder = vr.Decoder()
    input("press enter to connect to front-end")
    #decoder.detectSilence("recv.wav")
    decoder.listen_stream()

if __name__ == "__main__":
    main()
