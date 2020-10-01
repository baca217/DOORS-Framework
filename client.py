import socket
import os

CHUNK = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 10000))

f_size = os.path.getsize("downSamp.wav")
fd = open("downSamp.wav", "rb")
#opening the .wav file binary
if(not fd):
    print("file failed to open")
    exit()
#reading the file
r_bytes = fd.read(CHUNK)
while (r_bytes):
    s.send(r_bytes)
    r_bytes = fd.read(CHUNK)
s.close()
#msg = s.recv(1024)
#print(msg)
