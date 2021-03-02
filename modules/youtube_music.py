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

def download_song(songName):
    videosSearch = VideosSearch(songName, limit = 2) #searching information about song
    result = (videosSearch.result())
    video = pafy.new(result["result"][0]["link"])
    url = result["result"][0]["link"]
    audiostreams = video.audiostreams
    convert = "ffmpeg -i \"{}\" -isr 48000 -ar 8000 -ac 1 Song.wav"

    for i in audiostreams:
        print(i.bitrate, i.extension, i.get_filesize()) #showing quality and version of song we can download
    #audiostreams[0].download() #old way of downloading one of the above formats


    ydl_opts = { #downloads options for youtube dl
            "outmpl": "temp.wav",
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "8",
                }],
            }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url]) #downloading video using youtube-dl

    files = glob.glob("./*.wav") #getting the latest wave file
    latest = max(files, key=os.path.getctime)
    print(latest)
    if not mixer.get_init():
        mixer.init()
    mixer.music.load(latest)
    mixer.music.play()
    input("press enter to continue")
    print(convert.format(latest))
    input("is this okay?")
    os.system(convert.format(latest))
    os.remove(latest)
    mixer.music.stop()

def command_format():
    formats = [
            "play the song {} by {}",
            "play the song {}",
            "look for the song {} by {}",
            "look for the song {}",
            "play {} by {}",
            "play {}"
            ]
    return formats

def test(decoder, rec_com):
    f_name = "downSamp.wav"
    try:
        os.system("rm downSamp.wav")
    except:
        print("nothing to do")
    for i in rec_com:
        os.system(i)
#    os.system("clear")

    sentence = decoder.decode_file(f_name)
    print(sentence)
    vals = None
    for i in command_format():
        ret = parse(i, sentence)
        print(ret)
        if ret is not None:            
            vals = ret
            break
    if vals is not None:
        print(vals[0])
        download_song(vals[0])

def sendToFront():
    SIZE = int(65536/2)
    #open file for sending
    f = open("Song.wav", "rb")
    binaryHeader = f.read(44)
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
    #sendToFront()

if __name__ == "__main__":
    main()
