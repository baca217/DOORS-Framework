#!/usr/bin/env python3

import socket
import wave

def send_stuff():
    files = [
            "offLight.wav",
            "onLight.wav",
            "plugOff.wav",
            "plugOn.wav",
            "silence.wav",
            ]
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 5555        # Port to listen on (non-privileged ports are > 1023)
    SIZE = int(65536/2)


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        for i in range(len(files)):
            print("{}. {}".format(i, files[i]))
        name = int(input("enter file number to send :"))
        f = open("./voice_files/"+files[name], "rb")

        s.listen()
        conn, addr = s.accept()
        with conn:
            print('SEND Connected by', addr)
            # Receive the data in small chunks and retransmit it
            print("FILE: {}".format(files[name]))
            header = f.read(44)
            size = 1
            while size > 0:
                read = f.read(SIZE)
                size = len(read)
                print(size)
                conn.sendall(read)
        while True:
            s.listen()
            conn, addr = s.accept()
            print("RECEIVE by {}".format(addr))
            cont = conn.recv(1024)
            print(cont)
            listen = input("continue listening?")
            if listen == "no" or listen == "n":
                break
        f.close()
        s.close()

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
    while True:
        todo = input("s for send\nr for receive\n")
        if todo == "s":
            send_stuff()
        elif todo == "r":
            receive_stuff()
        else:
            print(todo + " is not an option\n")

if __name__ == "__main__":
    main()
