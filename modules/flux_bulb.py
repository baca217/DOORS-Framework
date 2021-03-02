#!/usr/bin/env python3

#pip install flux_led
#reference https://github.com/Danielhiversen/flux_led

from parse import *
import os
from flux_led import WifiLedBulb, BulbScanner

def commands(com):
    if com.lower().strip() is "turn on the flex bulb":
        turnOn() 

def turnOn():
    ip = "NONE"
    os.system("python -m flux_led "+ip+" --on")
