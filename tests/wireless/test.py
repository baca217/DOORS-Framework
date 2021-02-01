#!/usr/bin/env python3

import modules.vosk_rec as vr

dec = vr.Decoder()

print(dec.decode_file("tot.wav"))
print(dec.decode_file("downSamp.wav"))
