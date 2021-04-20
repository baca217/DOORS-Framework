# DOORS-Framework

The DOORS-Framework is meant to be the backend software for the Homie smart home system. 
It does the voice recognition, silence detection, and also includes some other features. These features 
are playing music from the local library, playing music using YouTube, timer functionality, 
stopwatch functionality, getting the weather for any city, IoT integration for 2 devices (HS103 smart plug
and Flux LED Lightbulb). 

This version of the DOORS-Framework is heavily catered towards communicating with a microphone and speaker device designed by the JJ-GEEX student group at the University of Colorado Boulder. It requires that the IP of the microphone/speaker system be known, and that it gets the correct communication messages from that device. This system **requires** that device.
## Basic Instillation
Run the script install.sh by giving it execution permission and sudo privilege's.
command: chmod +x install.sh; sudo ./install.sh

## Potential Problems With Instillation
The install script should work for most Linux systems. There might be a warning where the
path '/home/pi/.local/bin' is not included within the main PATH environment variable. You
can simply add it within your .bashrc file which should be located within your home directory.
Just add this line to the top of the file or wherever you set your PATH environment variable.
Without doing this the program **will not work**
.bashrc addition: export PATH="$PATH:/home/pi/.local/bin"

Another problem that may occur is that Kaldi may not be installed on your system. This is highly
unlikely unless you have a very stripped down version of Linux. If this is the case please follow
the instructions on how to install kaldi on there official GitHub, and also how to get it working
with Vosk on their official GitHub. They do a much better job at explaining the process than I ever
could.
Kaldi github : https://github.com/kaldi-asr/kaldi
Kaldi website : https://kaldi-asr.org/
Vosk github : https://github.com/alphacep/vosk-api
Vosk website : https://alphacephei.com/vosk/

