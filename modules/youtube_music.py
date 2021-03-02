#!/usr/bin/env python3

#pip3 install youtube-search-python
#pip3 install pafy
#pip3 install python-vlc

#need to worry about converting the quality down to 8000 sample rate and then playing it
#the way we're downloading it now is slowing the audio down a little :(

from __future__ import unicode_literals
from youtubesearchpython import VideosSearch
from pygame import mixer
from parse import *
import youtube_dl
import json
import pafy
import glob
import os

def download_song(songName):
    videosSearch = VideosSearch(songName, limit = 2) #searching information about song
    result = (videosSearch.result())
    print(result)
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

    ''' information in the result class
    for i in result["result"]:
        print(i["title"])
        print(i["link"])
        type
        id
        title
        publishedTime
        duration
        viewCount
        thumbnails
        descriptionSnippet
        channel
        accessibility
        link
        shelfTitle
        print()
    '''

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

def main():
    input("please press enter when you're ready to record for 10 seconds")

    download_song("dance in the darkness joji")

if __name__ == "__main__":
    main()
