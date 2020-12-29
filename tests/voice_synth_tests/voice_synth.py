#!/usr/bin/env python

from num2words import num2words
from subprocess import call

class VoiceSynth:

    def speak(self, sentence):
	sentence = sentence.replace(" ","_")
        command = 'espeak {} --stdout |aplay 2>/dev/null'.format(sentence)
        call([command], shell=True)
