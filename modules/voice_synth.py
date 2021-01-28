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
			comb = comb.replace(" ","_") #spaces must be replaced with _ for aplay to work		
			comb = comb.replace("\n", "_")	
			command = 'espeak {} --stdout |aplay 2>/dev/null'.format(comb)
			print(command)
#			call([command], shell=True)
			system(command)

	def enable(self):
		self.enabled = True
	
	def disable(self):
		self.enabled = False
