import os
from os import listdir
from os.path import isfile, join
import importlib

def run():
    mypath = os.getcwd()+"/modules"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for i in onlyfiles:
#        if ".py" in i:
#            print(i)
        if "local_music_player" in i:
            print(i)
            module = __import__("modules/local_music_player")

            my_class = getattr(module, "module")
            print(my_class.strFunctions())
