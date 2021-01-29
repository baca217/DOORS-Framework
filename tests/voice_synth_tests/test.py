#!/usr/bin/env python3
import modules.sklearn_sims as sklearn_sims
import modules.local_commands as lc
import modules.voice_synth as vs
import os #for recording, temporary usage

def main():
	voice = vs.VoiceSynth()
	stopwatch = lc.Stopwatch()

	#testSetTimer(voice)
	testPlaySong(voice)
	#testWeather(voice)
	#testStartWatch(stopwatch, voice)
	#testStopWatch(stopwatch, voice)
	#testStopMusic(voice)
		
def testSetTimer(voice):
	sent1 = "set a timer for 3 seconds" #works correctly
	sent2 = "set a timer for 0 seconds" #works correctly
	sent3 = "set a timer for seconds" #test defaults to 0 second error. Might change to no time detected error
	sent4 = "set a timer for 5" #works correctly
	sent5 = "set a timer for 33 seconds" #works correctly
	sent6 = "set a timer for"
	arr = [sent1, sent2, sent3, sent4, sent5]
	match = "set a timer for"
	title = "TESTING SET TIMER FUNCTIONALITY"
	testNum	= 1

	print(title)
	for i in range(0, len(arr)):
		testInfo(arr[i], i)
		lc.check_command(match, arr[i], None, voice)
		input("press enter for the next test\n\n")
	print("END*******************************************")	
def testPlaySong(voice):
	sent1 = "play the song country roads"
	sent2 = "play the song"
	sent3 = "play the song random"
	match = "play the song"
	arr = [sent1, sent2, sent3]
	
	for i in range(0, len(arr)):
		testInfo(arr[i], i)
		lc.check_command(match, arr[i], None, voice)
		input("press enter for the next test")

def testWeather(voice):
	sent1 = "what's the weather in denver"
	sent2 = "what's the weather in america"
	sent3 = "what's the weather in random"
	sent4 = "what's the weather in"
	match = "what's the weather in"
	lc.check_command(match, sent1, None, voice)
	lc.check_command(match, sent2, None, voice)
	lc.check_command(match, sent3, None, voice)
	lc.check_command(match, sent4, None, voice)

def testStartWatch(watch, voice):
	sent1 = "start a stopwatch"
	match = "start a stopwatch"
	lc.check_command(match, sent1, watch, voice)

def testStopWatch(watch, voice):
	sent1 = "stop the stopwatch"
	match = "stop the stopwatch"
	lc.check_command(match, sent1, watch, voice)

def testStopMusic(voice):
	sent1 = "stop playing music"
	match = "stop playing music"
	lc.check_command(match, sent1, None, voice)

def testInfo(command, testNum):
	print("TEST",testNum)
	print("command to be tested:",command)

if __name__ == "__main__":
    main()
