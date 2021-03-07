# File: pify.py
# Auth: Grant
# Desc: Prototype Python script for interfacing with the AirLift via WiFi.

import os
import sys
import socket


HOST ='192.168.43.151'
PORT = 5555
afAddr = (HOST, PORT)

oF = open("rawDat.raw", 'wb')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #sock.connect({HOST,PORT})
    sock.connect(afAddr)
    sock.sendall(b'MSTOP\0')
    doneYet = False
    while not doneYet:
        data = sock.recv(1024)
        if (len(data) == 0):
            doneYet = True
        else:
            oF.write(data)
oF.close()
