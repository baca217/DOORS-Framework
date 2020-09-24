arecord -f S16_LE -d 10 -r 48000 --device="hw:2" /tmp/test-mic.wav
echo 'stopped playing, will play recording'
aplay /tmp/test-mic.wav

echo 'eval recording'
python live.py
