import serial

def rec_data():
    #port = serial.Serial("/dev/ttyACM0", baudrate=230400, timeout=3.0)
    port = open("test.txt", "r")
    f = ("downSamp.wav", "w")
    start = "are ya ready kids?"
    stop = "done!!!"

    while True:
        rcv = port.read(1024)
        start = rcv.find(msg)
        if(start != -1): #start message was detected
            rcv = rcv[start+len(start):] #remove message
            start = rcv.find(stop) #checking for stop message
            while(start == -1):
                f.write(rcv) #write data to file
                rcv = port.read(1024) #rcv data
                start = rcv.find(stop) #try and find stop word
            rcv = rcv[:start+len(stop)] #remove stop word
            f.write(rcv) #write remaining data
            f.close()
            break
