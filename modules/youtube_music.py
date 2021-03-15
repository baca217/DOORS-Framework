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
def download_song(songName):
    videosSearch = VideosSearch(songName, limit = 2) #searching information about song
    result = (videosSearch.result())
    video = pafy.new(result["result"][0]["link"])
    url = result["result"][0]["link"]
    audiostreams = video.audiostreams #pulling audio from video
    
    for i in audiostreams:
        print(i.bitrate, i.extension, i.get_filesize()) #showing download qualities  of songs


    ydl_opts = { #downloads options for youtube dl
            "outmpl": "temp.wav",
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
                }],
            }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url]) #downloading video using youtube-dl
    return play_song()
    
def play_song():
    convert = "ffmpeg -i \"{}\" -isr 48000 -ar 16000 -ac 1 Song.wav" #downsampling command
    files = glob.glob("./*.wav") #getting the latest wave file
    latest = max(files, key=os.path.getctime)

    os.system(convert.format(latest))
    os.system("rm \'"+latest+"\'")
    if not mixer.get_init():
        mixer.init(16000, -16, 1)
    mixer.music.load("./Song.wav")
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
                "using youtube look for the song {}",
                "using you tube play the song {}",
                "using you tube look for the song {}",

            ]
            ]
    classify = [
            "parse"
            ]
    return coms, classify

def test(sentence):

    for i in command_format(): #trying to pull arguments from string passed in
        ret = parse(i, sentence)
        if ret is not None:
            vals = ret
            break
    if vals is not None:
        print(vals[0])
        download_song(vals[0])

def command_handler(sentence):
    msg = "song name couldn't be derived"
    function = None
    comms, classify = commands()
    for i in comms: #iterating through command arrays
        for j in i: #iterating through individual commands
            result = parse(j, sentence)
            if result: #was able to parse sentence using a command format
                function = download_song(result[0])
                msg = "going to play the song "+result[0]
                break
        if function: #function was set, break and return
            break
    return msg, function




'''
FUNCTION:sendToFront
ARGUMENTS: NONE
FUNCTIONALITY: takes the downsampled audio file for music named "Song.wav" and sends it to some
ip address on port 10000 in chunks of 32768 bytes. The message is preappended with "APCKT\n"
for formatting which is how the front-end team wants it. After the whole file is sent the socket is
closed.
'''
def sendToFront():
    SIZE = int(65536/2)
    #open file for sending
    f = open("Song.wav", "rb")
    binaryHeader = f.read(44) #remove .wav header info for raw format
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('127.0.0.1', 10000)
    print (sys.stderr, 'connecting to %s port %s' % server_address)
    sock.connect(server_address)
    sock.send(b"APCKT\n")
    size = 1
    while size > 0:
            read = f.read(SIZE)
            size = len(read)
            print(size)
            sock.send(read)
    sock.close()


def main(): 
    download_song("dance in the darkness joji")
    sendToFront()

if __name__ == "__main__":
    main()
