import time #for stopwatch
import requests, json #for weather
from fuzzywuzzy import fuzz #for music
from fuzzywuzzy import process #for music
import os #for muci
import pwd #for music
import eyed3


def setReminder(dateStr): #only going to focus on time for now
    yourdate = dateutil.parser.parse(dateStr)
    return 0

def playSong(songName):
    songs = []
    highDis = 0
    highTitle = ""
    path = "/home/"+pwd.getpwuid(os.getuid()).pw_name+"/Music/" #dir for music for current user
    onlyfiles = [f for f in os.listdir(path) if f.endswith(".mp3")] #only mp3 files pulled
    for i in onlyfiles:
        audFile = eyed3.load(path+i)
        print("artist: ",audFile.tag.artist," album: ",audFile.tag.album," title: ",audFile.tag.title) #check metadata of mp3 file
        dis = fuzz.ratio(songName.lower(), audFile.tag.title.lower())
        if dis > 80:
            songs.append([dis, audFile.tag.title])
            if dis > highDis:
                highDis = dis
                highTitle = audFile.tag.title
        print("ratio", dis)
    print("songs")
    for j in songs:
        print("comparison: ", j[0], " title:", j[1])
    print("highest", highDis, highTitle)
    return 0

def getWeather():
    #reference https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/
    api_key = "5985bc671ecc377555ecb761fbc53914"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = "Denver"
    print("using city,",city_name,"\n")

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
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
      
        # print following values 
        print(" Temperature (in kelvin unit) = " +
                        str(current_temperature) + 
              "\n atmospheric pressure (in hPa unit) = " +
                        str(current_pressure) +
              "\n humidity (in percentage) = " +
                        str(current_humidiy) +
              "\n description = " +
                        str(weather_description)) 

    else:
        print(" City Not Found ")
    return 0

def startStopwatch(): #not the cleanest way, maybe store time in main
    startTime = time.time() 
    f = open("time.txt", mode = "w")
    f.write(str(startTime))
    f.close()
    return 0

def stopStopwatch(): #using time from main, check if clock is even running
    stopTime = time.time()
    f = open("time.txt", mode = "r")
    startTime = float(f.read())
    print("tot time: ", stopTime - startTime) 
    return 0
