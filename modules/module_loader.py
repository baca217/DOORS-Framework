#!/usr/bin/env python3
import os
import importlib
import local_music_player as lmp
import stopwatch as sw
import timer as timer
import weather_api as weather
from os import listdir
from os.path import isfile, join

def run():
    mypath = os.getcwd()+"/modules"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for i in onlyfiles:
#        if ".py" in i:
#            print(i)
        if "local_music_player" in i:
            print(i)
            module = __import__("modules.local_music_player")
            print(module)
            my_class = getattr(module, "module")
            print(my_class.strFunctions())

def modules():
    mods = [
            lmp,
            sw,
            timer,
            weather
            ]
    return mods

def print_coms(mods):
    for i in mods:
        print(i.commands())
        print()

def all_coms(mods):
    coms = []
    for i in mods:
        coms.append(i.commands())
    return coms

def main():
    mods = modules()
    print_coms(mods)

if __name__ == "__main__":
    main()
