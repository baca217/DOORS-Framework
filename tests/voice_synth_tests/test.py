#!/usr/bin/env python

import voice_synth as vs

def main():
    synth = vs.VoiceSynth()
    synth.speak('hello')

if __name__ == "__main__":
    main()
