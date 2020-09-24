arecord -f S16_LE -d 10 -r 48000 --device="hw:2" /tmp/test-mic.wav
ffmpeg -i /tmp/test-mic.wav -vn -ar 16000 -ac 1 /tmp/test1-mic.wav

