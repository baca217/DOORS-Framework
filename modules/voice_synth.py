#!/usr/bin/env python

from subprocess import call

class VoiceSynth:
	enabled = True
	
	def __init__(self):
		enabled = True

	def speak(self, sentence):
		if enabled:
			sentence = sentence.replace(" ","_") #spaces must be replaced with _ for aplay to work
			command = 'espeak {} --stdout |aplay 2>/dev/null'.format(sentence)
			call([command], shell=True)

	def enable(self):
		enabled = True
	
	def disable(self):
		enabled = False
