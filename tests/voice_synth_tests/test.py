#!/usr/bin/env python
import modules.sklearn_sims as sklearn_sims
import modules.local_commands as lc
import modules.serial_comm as serial_comm
import modules.voice_synth as vs
import os #for recording, temporary usage

def main():
	sentence = ""
        command = None
        if(match == "set a timer for"):
                data = original.replace(match, "") #removing matched string for easier comparison
                sentence, command = setTimer(data)
        elif(match == "play the song"):
                data = original.replace(match, "")
                sentence, command = playSong(data, voice)
        elif(match == "what's the weather"):
                if "what's the weather in" in original:
                        city = original.replace(match+" in", "")
                        sentence, command = getWeather(city, voice)
                else:
                        sentence, command = getWeather("Denver", voice)
        elif(match == "start a stopwatch"):
                sentence, command = stopwatch.handler("start", voice)
        elif(match == "stop the stopwatch"):
                sentence, command = stopwatch.handler("stop", voice)
        elif(match == "stop playing music"):
                sentence, command = stopSong(voice)
        else:
                sentence = match, "is not a known command"
        print(sentence)
        voice.speak(sentence)
        if command != None:
                command()	

def checkTimer():
	sent1 = "set a timer for 3 seconds"
	sent2 = "set a timer for 0 seconds"
	sent3 = "set a timer for 3" 
	match = "set a timer for"
	lc.check_command(match, sent1, None, )

if __name__ == "__main__":
    main()
