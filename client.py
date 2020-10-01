import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 10000))
s.send(bytes("Hi server!!!","utf-8"))
msg = s.recv(1024)
print(msg)
