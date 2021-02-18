import time #for stopwatch
import requests, json #for weather
from fuzzywuzzy import fuzz #for music
from fuzzywuzzy import process #for music
import os #for music
import pwd #for music
import eyed3 #for mp3 metadata pulling
from word2number import w2n #for settting timer
import signal #for setting a timer
from pygame import mixer #for playing music
from copy import deepcopy

class Stopwatch:
    
        def __init__(self):
                self.start = 0.0

        def handler(self, task):
                msg = ""
                if task == "start": #start a stopwatch
                        def startWatch():
                                self.start = time.time()
                        msg = "\nStarted a stopwatch"
                        return msg, startWatch()
                elif task == "stop": #stop the stopwatch
                        if(self.start != 0):
                                stop = "{0:.2f}".format(time.time() - self.start)
                                self.start = 0
                                msg = "\nstopwatch ran for "+stop+" seconds"
                                return msg, None
                        else:
                                msg = "\nstopwatch was never started"
                                return msg, None
                else:
                        msg = task,"is not a known task"
                        return msg, None

def handler(signal, frame): #handler for timer
        print("\n\nTime is up for timer!\n")

def setTimer(timeStr): #only going to focus on time for now
        temp = ""
        arr = timeStr.split()
        num = 0
        strNum = ""
        msg = ""
        timeSwitch = { #dictionary for scaling the time
            "second": 1,
            "minute": 60,
            "hour": 3600,
            }

        try:
                timeFormat = arr[-1].strip() #get time format
                arr = arr[:-1] #remove time format
        except: #failed to pull timeformat from string
                msg = "no time format was detected for setting a timer"
                return msg, None

        if(timeFormat[-1] is "s"): #removing trailing s. EX: seconds, minutes
                timeFormat = timeFormat[:-1]

        for f in range(len(arr),0,-1): #pulling time amount out of string
                try:
                        strtemp = " ".join(arr[f-1:]) #pull substring and see if it's a number          
                        numtemp = w2n.word_to_num(strtemp)
                        num = int(numtemp)
                except valueerror:
                        break

        if(timeFormat not in timeSwitch.keys()): #error 1: no time format
                msg = timeFormat+" is not a valid time format"
                return msg, None
        elif(num == 0): #error 2: time requested is 0 for timer
                msg = "can't set a timer for 0 "+timeFormat
                return msg, None

        msg = "\nsetting timer for "+str(num)+" "+timeFormat
        if num > 1:
                msg += "s"
        def setSignal():
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(num * timeSwitch[timeFormat])
        return msg, setSignal

def playSong(songName):
        songName = songName.strip()
        songs = []
        highDis = 0
        highDitle = ""
        highPath = ""
        path = "/home/"+pwd.getpwuid(os.getuid()).pw_name+"/Music/" #dir for music for current user
        onlyfiles = [f for f in os.listdir(path) if f.endswith(".mp3")] #only mp3 files pulled

        if(len(songName) == 0):
                msg = "No song name was given"
                return msg, None

        for i in onlyfiles:
                fpath = path+i
                try:
                        audFile = eyed3.load(fpath)
                except:
                        print("files in Music directory must have no spaces in the file name")
                        continue
                if audFile.tag.title is None:
                        print("file "+i+" doesn't have a song title in its metadata")
                        continue
                dis = fuzz.ratio(songName.lower(), audFile.tag.title.lower())
                if dis > 79: # 80% similarity or more is saved
                        songs.append([dis, audFile.tag.title])
                        if dis > highDis: #getting the most similar
                                highDis = dis
                                highTitle = audFile.tag.title
                                highPath = i
        if(highPath):
                msg = "Song "+highTitle+" will be played"
                def playSong():
                        mixer.init()
                        mixer.music.load(path+highPath)
                        mixer.music.play()
                return msg, playSong
        else:
                msg = "No songs in the local library matched "+songName
                return msg, None
        return 0

def stopSong():
        def stopMusicFunc():
#               mixer.init()
                mixer.music.pause()
        msg = "music is stopped"
        return msg, stopMusicFunc()

def getWeather(city_name):
        #reference https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/
        api_key = "5985bc671ecc377555ecb761fbc53914"
        base_url = "http://api.openweathermap.org/data/2.5/weather?q="
        msg = "\nusing city: "+city_name

        complete_url = base_url + city_name + "&appid=" + api_key 
        response = requests.get(complete_url)
        x = response.json()

        if x["cod"] != "404" and city_name.strip() != "": #404 = city not found
                # store the value of "main" 
                # key in variable y 
                y = x["main"] 

                # store the value corresponding 
                # to the "temp" key of y 
                current_temperature = y["temp"] 

                # store the value corresponding 
                # to the "pressure" key of y 
                current_pressure = y["pressure"] 

                # store the value corresponding 
                # to the "humidity" key of y 
                current_humidiy = y["humidity"] 

                # store the value of "weather" 
                # key in variable z 
                z = x["weather"] 

                # store the value corresponding  
                # to the "description" key at  
                # the 0th index of z 
                weather_description = z[0]["description"]

                temperature = "{0:.2f}".format(current_temperature * 9 / 5 - 459.65)
                # print following values 
                msg = (msg + " Temperature in degrees Fahrenheit = " +
                                temperature + 
                        "\n atmospheric pressure in hPa unit = " +
                                str(current_pressure) +
                        "\n humidity in percentage = " +
                                str(current_humidiy) +
                        "\n description = " +
                                weather_description +
                                "\n") 
                return msg, None
        else:
                msg += " City Not Found \n"
                return msg, None
        return 0

def check_command(match, original, stopwatch, voice):
        sentence = ""
        command = None
        if(match == "set a timer for"):
                data = original.replace(match, "") #removing matched string for easier comparison
                sentence, command = setTimer(data)
        elif(match == "play the song"):
                data = original.replace(match, "")
                sentence, command = playSong(data)
        elif(match == "what's the weather"):
                if "what's the weather in" in original:
                        city = original.replace(match+" in", "")
                        sentence, command = getWeather(city)
                else:
                        sentence, command = getWeather("Denver")
        elif(match == "start a stopwatch"):
                sentence, command = stopwatch.handler("start")
        elif(match == "stop the stopwatch"):
                sentence, command = stopwatch.handler("stop")
        elif(match == "stop playing music"):
                sentence, command = stopSong()
        else:
                sentence = match, "is not a known command"
        #print(sentence) out for testing
        #voice.speak(sentence)   
        if command != None:
                command()
        return sentence #just for assertion testing
