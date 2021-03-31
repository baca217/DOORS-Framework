#!/usr/bin/env python3

#pip install flux_led
#reference https://github.com/Danielhiversen/flux_led

from parse import *
import os
from flux_led import WifiLedBulb, BulbScanner
from word2number import w2n

#still working on the brightness function. Need to worry about querying the color of the lightbulb first,
#then setting the brightness back

def command_handler(sentence, info):
    scanner = BulbScanner()
    coms, classify = commands()
    msg = sentence+" is not a know flux lightbulb command"
    function = None

    print("scanner scan: ", end="")
    print(scanner.scan(timeout = 4))

    try:
        #specific ID/MAC of bulb
        my_light = scanner.getBulbInfoByID("D8F15BA2EE72")
    except:
        msg = "flux lightbulb not detected!"
        return msg, function

    print("success!")
    bulb = WifiLedBulb(my_light["ipaddr"])
            
    for i in coms[0]: #lightbulb color changer
        res = parse(i, sentence)
        if res:
            msg, function = colorChanger(bulb, res[0])
            return msg, function
    if sentence in coms[1]: #turn lightbulb off
        msg = "turning the flux lightbulb off"
        function = bulb.turnOff()
        return msg, function
    if sentence in coms[2]: #turn the lightbulb on
        msg = "turning the flux lightbulb on"
        function = bulb.turnOn()
        return msg, function
    for i in coms[3]: #change brightness of lightbulb
        res = parse(i, sentence)
        if res:
            msg, function = brightnessChanger(bulb, res[0])
            return msg, function
    return msg, function

def commands():
    coms = [
            [
                "turn the flux lightbulb color to {}",
                "set the flux bulb color to {}",
            ],
            [
                "turn the flux lightbulb off",
                "turn the flux light bulb off",
                "turn off the flux lightbulb",
                "turn off the flux light bulb",
            ],
            [
                "turn the flux lightbulb on",
                "turn the flux light bulb on",
                "turn on the flux lightbulb",
                "turn on the flux light bulb",
            ],
            [
                "set the flux lightbulb brightness to {} percent",
                "set the flux light bulb brightness to {} percent",
                "set the brightness of the flux lightbulb to {} percent",
                "set the brightness of the flux light bulb to {} percent",
            ],
        ]
    
    classify = [
            "parse",
            "cosine",
            "cosine",
            "parse",
        ]
    return coms, classify

def colorChanger(bulb, color):
    msg = ""
    function = None
    colors = {
            "red" : (255,0,0),
            "orange" : (255,125,0),
            "yellow" : (255, 255, 0),
            "springgreen" : (125,255,0),
            "green" : (0,255,0),
            "turquoise" : (0,255,125),
            "cyan" : (0, 255, 255),
            "ocean" : (0,125,255),
            "blue" : (0,0,255),
            "violet" : (125, 0, 255),
            "magenta" : (255, 0, 255),
            "raspberry" : (255, 0, 125)
            }
    try:
        rgb = colors[color]
    except:
        msg = color+" is not a supported color for flux lightbulb"
        return msg, function
    bulb.refreshState()

    # set to color and wait
    # (use non-persistent mode to help preserve flash)
    bulb.setRgb(*rgb, persist=False)
    msg = "going to change flux bulb color to "+color
    function = None

    return msg, function

def brightnessChanger(bulb, percent):
    num = w2n.word_to_num(percent) / 100
    msg = "okay"
    def funct():
        print(str(num) + " percent")
        bulb.setRgb(255, 0, 0, persist=False, brightness = int(255 * num))
    return msg, funct

def main():
    print("flux main does nothing")
        
if __name__ == "__main__":
    main()
