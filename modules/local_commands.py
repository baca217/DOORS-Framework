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
import modules.voice_synth as vs

class Stopwatch:
    
    def __init__(self):
        self.start = 0.0

    def handler(self, task):
        if task == "start":
            self.start = time.time()
            #t = time.localtime()
            #cur_time = time.strftime("%H:%M:%S", t)
            #print("started stopwatch at:",cur_time)
            print("\nStarted a stopwatch")
        elif task == "stop":
            if(self.start != 0):
                #t = time.localtime()
                #cur_time = time.strftime("%H:%M:%S", t)
                #print("stopped stopwatch at:",cur_time)
                stop = "{0:.2f}".format(time.time() - self.start)
                print("\nstopwatch ran for",stop,"seconds")
                self.start = 0
            else:
                print("\nstopwatch was never started")
        else:
            print(task,"is not a known task")

def handler(signal, frame): #handler for timer
    print("\n\nTime is up for timer!\n")

def setTimer(timeStr, voice): #only going to focus on time for now
    temp = ""
    arr = timeStr.split()
    num = 0
    strNum = ""
    msg = ""
    timeFormat = arr[-1] #get time format
    arr = arr[:-1] #remove time format
    timeSwitch = { #dictionary for scaling the time
            "second": 1,
            "minute": 60,
            "hour": 3600,
            }

    if(timeFormat[-1] is "s"): #removing trailing s. EX: seconds, minutes
        timeFormat = timeFormat[:-1]
    for f in range(len(arr),0,-1):
        try:
            strTemp = " ".join(arr[f-1:])
            numTemp = w2n.word_to_num(strTemp)
            num = int(numTemp)
        except ValueError:
            break

    if(timeFormat == ""): #error 1: no time format
	msg = "no time format was detected for setting a timer"
        print(msg)
	voice.speak(msg)
        return 1
    elif(num == 0): #error 2: time requested is 0 for timer
	msg = "can't set a timer for 0",timeFormat
        print(msg)
	voice.speak(msg)
        return 1
    if timeFormat in timeSwitch:
	msg = "\nsetting timer for",num,timeFormat
        print(msg)
	voice.speak(msg)
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(num * timeSwitch[timeFormat])
        #time.sleep(num * timeSwitch[timeFormat])
    else:
	msg = timeFormat,"is not a known time format"
	voice.speak(msg)
        print(msg)
    return 0

def playSong(songName):
    songName = songName.strip()
    songs = []
    highDis = 0
    highTitle = ""
    highPath = ""
    path = "/home/"+pwd.getpwuid(os.getuid()).pw_name+"/Music/" #dir for music for current user
    onlyfiles = [f for f in os.listdir(path) if f.endswith(".mp3")] #only mp3 files pulled
    for i in onlyfiles:
        audFile = eyed3.load(path+i)
        #print("artist: ",audFile.tag.artist," album: ",audFile.tag.album," title: ",audFile.tag.title) #check metadata of mp3 file
        dis = fuzz.ratio(songName.lower(), audFile.tag.title.lower())
        if dis > 79: # 80% similarity or more is saved
            songs.append([dis, audFile.tag.title])
            if dis > highDis: #getting the most similar
                highDis = dis
                highTitle = audFile.tag.title
                highPath = i
        #print("ratio", dis)
    #print("songs")
    #for j in songs:
    #    print("comparison: ", j[0], " title:", j[1])
    #print("highest", highDis)
    if(highPath):
        print("Song",highTitle,"will be played")
        mixer.init()
        mixer.music.load(path+highPath)
        mixer.music.play()
    else:
        print("No songs matched in the local library matched",songName)
    return 0

def stopSong():
    mixer.init()
    mixer.music.pause()
    print("music is stopped")

def getWeather(city_name):
    #reference https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/
    api_key = "5985bc671ecc377555ecb761fbc53914"
    base_url = "http://api.openweathermap.org/data/2.5/weather?q="
    print("\nusing city:",city_name)

    complete_url = base_url + city_name + "&appid=" + api_key 
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404": #404 = city not found
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
        print(" Temperature (in degrees Fahrenheit) = " +
                        temperature + 
              "\n atmospheric pressure (in hPa unit) = " +
                        str(current_pressure) +
              "\n humidity (in percentage) = " +
                        str(current_humidiy) +
              "\n description = " +
                        str(weather_description) +
                        "\n") 

    else:
        print(" City Not Found \n")
    return 0

def check_command(match, original, stopwatch, voice):
    if(match == "set a timer for"):
        data = original.replace(match, "")
        setTimer(data, voice)
    elif(match == "play the song"):
        data = original.replace(match, "")
        playSong(data, voice)
    elif(match == "what's the weather"):
            if "what's the weather in" in original:
                city = original.replace(match+" in", "")
                getWeather(city, voice)
            else:
                getWeather("Denver", voice)
    elif(match == "start a stopwatch"):
        stopwatch.handler("start", voice)
    elif(match == "stop the stopwatch"):
        stopwatch.handler("stop", voice)
    elif(match == "stop playing music"):
        stopSong(voice)
    else:
        print(match, "is not a known command")
