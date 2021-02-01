#!/usr/bin/env python3

import modules.vosk_rec as vr

dec = vr.Decoder()

dec.decode_file("tot.wav")
