#!/usr/bin/env python3
from os import system
from os import listdir
from os.path import isfile, join

mypath = "/home/pi/Documents/DOORS/modules/recordings/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print("files to downsamp:")
for i in range(len(onlyfiles)):
    print(i,":",onlyfiles[i])
num = int(input("enter file number:"))
fname = mypath+onlyfiles[num]
system("ffmpeg -i "+fname+" -isr 9000 -ar 8000 downSamp.wav")
