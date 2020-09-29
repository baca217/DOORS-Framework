#!/bin/sh

### Grant's PocketSphinx-Python Test
### 09/28/2020
###
### Remember to change the arecord and ffmpeg commands to match
### your microphone.  The result should be 16kHz mono audio.
###
### Included are the commands known to be good for my (Grant's)
### and Elmer's microphones.
### Uncomment the appropriate lines for you, or append your own.

###========================================================###
### Elmer's microphone:
#arecord -t wav -D "hw:2" -c 2 -d 10 -f S16_LE -r 48000 test.wav
#ffmpeg -i test.wav -isr 48000 -ar 16000 downSamp.wav
### Grant's microphone:
arecord -t wav -D "hw:2" -c 2 -d 10 -f S16_LE -r 48000 test.wav
ffmpeg -i test.wav -isr 48000 -ac 1 -ar 16000 downSamp.wav
###========================================================###

### Uncomment this line to preview the line (requires mpv (obviously))
#mpv downSamp.wav
python3 py3_sphinxTest.py
rm test.wav downSamp.wav
