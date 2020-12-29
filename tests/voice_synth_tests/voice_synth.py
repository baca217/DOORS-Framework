#!/usr/bin/env python

from num2words import num2words
from subprocess import call

class VoiceSynth:

    def speak(self,sentence):
        command = 'espeak {} --stdout |aplay 2>/dev/null'.format(sentence)
        call([command], shell=True)
