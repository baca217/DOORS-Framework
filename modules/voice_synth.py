#!/usr/bin/env python

from subprocess import call
from os import system

class VoiceSynth:
	enabled = True
	
#	def __init__(self):
#		enabled = True

	def speak(self, sentence):
		if self.enabled:
			comb = ""
			for i in sentence:
				comb += i
			comb = comb.replace("\n", " ")	
			command = 'espeak \"{}\" --stdout |aplay 2>/dev/null'.format(comb)
			system(command)

	def enable(self):
		self.enabled = True
	
	def disable(self):
		self.enabled = False
