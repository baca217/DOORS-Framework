import serial
import numpy as np
import wavio
import time
import vosk_rec as vr

# ser = serial.Serial(
#     port='COM5',\
#     baudrate=9600,\
#     parity=serial.PARITY_NONE,\
#     stopbits=serial.STOPBITS_ONE,\
#     bytesize=serial.EIGHTBITS,\
#         timeout=0)

# Protocol is  Homie Front End: "\n\rAre Ya Ready Kids?\n\r"
#  Response "Aye Aye Captain!" -> if Failed it will say "I cant hear you"

SAMPLE_RATE = 8000
RECEIVE_FILE = "audio.wav"
COMPLETE_FILE = "complete.wav"

port = serial.Serial("/dev/ttyACM0", baudrate = 921600, timeout = 10.0)
decoder = vosk_rec.Decoder()
allData = ""


print("Press Push Button When Ready")
while port.inWaiting() < 17:
    pass

message = port.read(17).decode(errors='ignore')
print(message)
if message == "are ya ready kids": #front-end ready
    my_message = "aye aye captain".encode('ascii', errors='ignore')
    port.write(my_message) #back-end ready
    print(my_message)
    while True: #voice recognition
        rcv = port.read(80000)
        my_audio = np.frombuffer(rcv, np.int16)
        wavio.write(RECEIVE_FILE, my_audio, SAMPLE_RATE) #temporary file
        result = decoder.decode_file(RECEIVE_FILE)
        if(len(result) == 0): #nothing was detected, stopping
            my_audio = np.frombuffer(allData, np.int16)
            wavio.write(COMPLETE_FILE, my_audio, SAMPLE_RATE)
            decoder.decode_file(COMPLETE_FILE)
        else: #something was detected, adding it to a buffer
            allData += rcv

        
    #***************NOTE**************************
    #what is this for?---------------------------
    #my_message = "i cant hear you".encode('ascii', errors='ignore')
    #port.write(my_message)
    #print(my_message)

    #reason for sleep?--------------------------
    #time.sleep(1)

    #reason for this message?--------------------
    #my_message = "ooohhh".encode('ascii', errors='ignore')
    #port.write(my_message)
    #print("ooohhh")
    #*********************************************
