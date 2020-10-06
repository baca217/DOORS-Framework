import time #for stopwatch
import requests, json #for weather

def setReminder(dateStr):
    yourdate = dateutil.parser.parse(dateStr)
    return 0
def playSong(songName):
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
