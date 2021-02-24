#!/usr/bin/env python3

#pip3 install youtube-search-python
#pip3 install pafy
#pip3 install python-vlc

#need to worry about converting the quality down to 8000 sample rate and then playing it

from __future__ import unicode_literals
from youtubesearchpython import VideosSearch
import youtube_dl
import json
import pafy
from pygame import mixer

videosSearch = VideosSearch('joji', limit = 2)
result = (videosSearch.result())

#mixer.init()
#mixer.music.load('test.mp3')
#mixer.music.play()
#input("press enter to continue")

video = pafy.new(result["result"][0]["link"])
url = result["result"][0]["link"]
audiostreams = video.audiostreams

ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "4",
            }],
        }

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

for i in audiostreams:
    print(i.bitrate, i.extension, i.get_filesize())
#audiostreams[0].download()

'''
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
