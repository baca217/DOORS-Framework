#!/usr/bin/env python3

from __future__ import unicode_literals
from youtubesearchpython import VideosSearch
from pygame import mixer
from parse import *
import youtube_dl
import json
import pafy
import glob
import os
import socket
import sys
import time

'''
FUNCTION: download_song
INPUTS: songName (string)
FUNCTIONALITY: essentially takes in a song name or really string and plugs it into the youtube
search algorithm. There are 2 search results that are returned. For now we just take the first
one and pull the audio from that video using youtube-dl and ffmpeg. The audio is downloaded 
any format usually .webm or .mp4 but it's converted to a .wav file. That file is then downsampled
to 8000 samples, converted to mono if necessary and saved to "Song.wav". The old .wav file is removed
and the new sampled file is what's left.
'''
def download_song(songName, info):
    try:
        videosSearch = VideosSearch(songName, limit = 2) #searching information about song
    except:
        return None
    result = (videosSearch.result())
    try:
        video = pafy.new(result["result"][0]["link"])
    except KeyError: #for some reason like counts breaks the program
        pass
    try: #remove the youtube holder song when possible
        os.system("rm {}/temp/yt_song.wav".format(info["path"]))
    except:
        pass
    url = result["result"][0]["link"]
    convert = "ffmpeg -i \"{}\" -ar 16000 -ac 1 "+"{}/temp/yt_song.wav".format(info["path"]) #downsampling command 

    ydl_opts = { #downloads options for youtube dl
            "outmpl": "temp/yt_temp.wav",
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
                }],
            }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url]) #downloading video using youtube-dl
    
    files = glob.glob("{}/*.wav".format(info["path"])) #getting the latest wave file
    latest = max(files, key=os.path.getctime)

    os.system(convert.format(latest))
    os.system("rm \'"+latest+"\'")
    def call_play():
        play_song()
    return call_play
    
def play_song(info):
    if not mixer.get_init():
        mixer.init(16000, -16, 1)
    mixer.music.load("{}/temp/yt_song.wav".format(info["path"]))
    mixer.music.play()

    input("wait")

    mixer.music.stop()


'''
FUNCTION: command_format
ARGUMENTS: NONE
FUNCTIONALITY: returns formats of strings that will be used for parsing the derived text from an
audio text
'''
def commands():
    coms = [
            [
                "using youtube play the song {}",
                "using you to play the song {}",
                "using youtube look for the song {}",
                "using you to look for the song {}",
                "using youtube look for and play the song {}",
                "using youtube play {}",
                "using you tube look for and play the song {}",
                "using you tube play the song {}",
                "using you tube look for the song {}",
                "using you tube play {}",
                "using you to play {}",
                "using you tube and play the song {}",
                "using youtube and play the song {}",
                "using you to and play the song {}",
            ]
            ]
    classify = [
            "parse"
            ]
    return coms, classify

def command_handler(sentence, info):
    msg = "song name couldn't be derived"
    function = None
    comms, classify = commands()
    for i in comms: #iterating through command arrays
        for j in i: #iterating through individual commands
            result = parse(j, sentence)
            if result: #was able to parse sentence using a command format
                function = download_song(result[0], info)
                if function == None:
                    msg = "error looking up song " + result[0]
                else:
                    msg = "going to play the song "+result[0]
                break
        if function: #function was set, break and return
            break
    return msg, function
