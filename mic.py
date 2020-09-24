from pocketsphinx import LiveSpeech
for phrase in LiveSpeech(audio_device="hw:2.0"): print(phrase)
