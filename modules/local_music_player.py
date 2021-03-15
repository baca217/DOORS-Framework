from pygame import mixer #for audio control
from fuzzywuzzy import fuzz #for music searching
from fuzzywuzzy import fuzz #for music searching
import os #for parsing files in directory
import pwd #for finding current directory
import eyed3 #for mp3 metadata pulling
from parse import *

def command_handler(sentence):
    msg = ""
    function = None
    if "play the song" in sentence:
        print(sentence)
        p1 = parse("play the song {} by {}", sentence)
        p2 = parse("play the song {}", sentence)
        if p1:
            msg, function = playSong(p1[0])
        elif p2:
            msg, function = playSong(p2[0])
        else:
            msg = "couldn't pull song from sentence"
            function = None
    elif "stop playing music" in sentence:
        msg, function = stopSong()
    elif "continue playing music" in sentence:
        msg, function = continueSong()
    else:
        msg = sentence+" is not a known command"
        function = None
    return msg, function

def commands():
    coms = [
                ["play the song {}"],
                [
                    "stop playing music", "you must stop playing music",
                    "stop whatever music is playing", "stop the music",
                    "the music must stop"
                ],
                [
                    "continue playing music", "unpause the music",
                    "continue playing the song", "unpause the song"
                ]
            ]
    comp_types = [
        "parse",
        "cosine",
        "cosine"
        ]
    return coms, comp_types

def playSong(songName):
        songName = songName.strip()
        songs = []
        highDis = 0
        highDitle = ""
        highPath = ""
        path = "/home/"+pwd.getpwuid(os.getuid()).pw_name+"/Music/" #dir for music for current user
        onlyfiles = [f for f in os.listdir(path) if f.endswith(".mp3")] #only mp3 files pulled

        if(len(songName) == 0):
                msg = "No song name was given"
                return msg, None

        for i in onlyfiles:
                fpath = path+i
                try:
                        audFile = eyed3.load(fpath)
                except:
                        print("files in Music directory must have no spaces in the file name")
                        continue
                if audFile.tag.title is None:
                        print("file "+i+" doesn't have a song title in its metadata")
                        continue
                dis = fuzz.ratio(songName.lower(), audFile.tag.title.lower())
                if dis > 79: # 80% similarity or more is saved
                        songs.append([dis, audFile.tag.title])
                        if dis > highDis: #getting the most similar
                                highDis = dis
                                highTitle = audFile.tag.title
                                highPath = i
        if(highPath):
                msg = "Song "+highTitle+" will be played"
                def playSong():
                        mixer.init()
                        mixer.music.load(path+highPath)
                        mixer.music.play()
                return msg, playSong
        else:
                msg = "No songs in the local library matched "+songName
                return msg, None
        return 0

def stopSong():
        if mixer.get_init():
            def stopMusicFunc():
                mixer.music.pause()
            msg = "music is stopped"
            return msg, stopMusicFunc()
        else:
            return "no music playing", None
        
def continueSong():
    if mixer.get_init():
        def contMusicFunc():
                mixer.music.unpause()
        msg = "music will be unpaused"
        return msg, contMusicFunc()
    else:
        return "no music playing", None
