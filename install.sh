MODEL="/modules/model"
CURDIR=`pwd`
if [ -d "$CURDIR$MODEL" ] 
then
	echo "$MODEL installed"
else
	echo "$MODEL not installed"
	echo "installing now"
	mkdir "$CURDIR$MODEL"
	wget https://alphacephei.com/vosk/models/vosk-model-en-us-daanzu-20200905.zip -P $CURDIR$MODEL #download model
	unzip $CURDIR$MODEL/vosk*
	mv vosk* vosk-model #easier rename for moving stuff
	mv vosk-model/* $CURDIR$MODEL #move stuff to correct directory
	rm -r vosk-model #rm temp directory
fi
pip3 install vosk
pip3 install sklearn
pip3 install scikit-learn
pip3 install fuzzywuzzy
pip3 install eyed3
pip3 install word2number
pip3 install python-Levenshtein
pip3 install spotipy
pip3 install youtube-search-python
pip3 install pygame
pip3 install parse
pip3 install youtube_dl
pip3 install pafy
pip3 install pydub
sudo apt-get update
sudo apt-get install libgfortran5
sudo apt-get install libgfortran3
sudo apt-get install libatlas-base-dev
