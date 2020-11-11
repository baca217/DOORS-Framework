#!/usr/bin/env python3
import vosk_rec

decoder = vosk_rec.Decoder()
decoder.decode_file("audio.wav")
print("done")
