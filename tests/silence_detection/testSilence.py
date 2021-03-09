#!/usr/bin/env python3

import modules.vosk_rec as vr

def main():
    decoder = vr.Decoder()
    #decoder.detectSilence("downSamp.wav")
    decoder.listen_stream()

if __name__ == "__main__":
    main()
