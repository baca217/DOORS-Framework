#!/usr/bin/env python3

import socket
import wave

def conn_stuff():
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 5555        # Port to listen on (non-privileged ports are > 1023)
    SIZE = int(65536/2)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        
        while True:
            try:
                print(f"listening for a connection IP: {HOST} PORT: {PORT}\n")
                s.listen()
                conn, addr = s.accept()
                print(f"got a connection from {addr}\n")
                with conn:
                    msg = conn.recv(SIZE)
                    if len(msg) > 5:
                        code = msg[:6]
                        msg = msg[6:]
                    else:
                        print(f"message is too short {msg}")
                        continue
                    print(code)
                    if (b"AOKAY\0") in code:
                        print("got an AOKAY, will send data")
                        send_stuff(conn)
                    elif (b"CNERR\0") in code:
                        print("got a CNERR, need to clear out buffer")
                    elif (b"GDATA\0") in code:
                        print("got a GDATA, the back-end got good data!")
                    elif (b"VOICE\0") in code:
                        print("got a VOICE, the back-end is sending us a voice file")
                    else:
                        print("code didn't match anything")

                    conn.close()

            except KeyboardInterrupt:
                print("keyboard stop. Closing connection and file")
                break
            except Exception as e:
                print("something went wrong")
                print(e)
                break
        s.close()

def send_stuff(conn):
    files = [
    "offLight.wav",
    "onLight.wav",
    "plugOff.wav",
    "plugOn.wav",
    "silence.wav",
    ]
    SIZE = int(65536/2)


    for i in range(len(files)):
        print("{}. {}".format(i, files[i]))
    name = int(input("enter file number to send : "))
    f = open("./voice_files/"+files[name], "rb")

    print("FILE: {}".format(files[name]))
    header = f.read(44)
    size = 1
    while size > 0:
        read = f.read(SIZE)
        size = len(read)
        print(size)
        try:
            conn.sendall(read)
        except BrokenPipeError:
            print("connection to front end died")
            break
    f.close()

def receive_stuff():
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 5555        # Port to listen on (non-privileged ports are > 1023)
    SIZE = int(65536/2)
    temp = wave.open("temp.wav", 'wb')
    temp.setnchannels(1) #mono
    temp.setsampwidth(2)
    temp.setframerate(16000)


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        print("listening")
        with conn:
            print('LISTEN Connected by', addr)
            size = 1
            while size > 0:
                try:
                    recv = conn.recv(SIZE)
                    size = len(recv)
                    opt = input("size is {} print content?".format(size))
                    if opt == "yes" or opt == "y":
                        print(recv)
                    else:
                        temp.writeframesraw(recv)
                except KeyboardInterrupt:
                    temp.close()
    temp.close()


def main():
    conn_stuff()

if __name__ == "__main__":
    main()
