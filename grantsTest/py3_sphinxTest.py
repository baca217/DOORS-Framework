# Based on the code provided by CMUSphinx project maintainers
# on this page: https://github.com/cmusphinx/pocketsphinx-python
# Runs when called with python3.

from __future__ import print_function
import os
from os import environ, path, getcwd

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

# These commands seem to be obsolete now:
#model_path = get_model_path()
#data_path = get_data_path()
# So I had to define them explicitly here.
# Remember to change them to match your installation.
model_path= "/home/pi/Documents/Sphinx/install/pocketsphinx-python/pocketsphinx/model"
data_path= "/home/pi/Documents/Sphinx/install/pocketsphinx-python/pocketsphinx/test/data"
audio_path = os.getcwd() # Audio file must be in the current working directory

#ps = pocketsphinx(**config)
config = Decoder.default_config()
config.set_string('-hmm', path.join(model_path, 'en-us/en-us'))
config.set_string('-lm', path.join(model_path, 'en-us/en-us.lm.bin'))
config.set_string('-dict', path.join(model_path, 'en-us/cmudict-en-us.dict'))

decoder = Decoder(config)
decoder.start_utt()
stream = open(path.join(audio_path, 'downSamp.wav'), 'rb')


while True:
  buf = stream.read(1024)
  if buf:
    decoder.process_raw(buf, False, False)
  else:
    break
decoder.end_utt()

print(decoder.hyp().hypstr)

