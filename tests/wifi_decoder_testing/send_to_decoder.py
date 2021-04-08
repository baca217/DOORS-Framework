#!/usr/bin/env python3

import socket
import wave

def send_stuff():
    files = [
            "offLight.wav",
            "onLight.wav",
            "plugOff.wav",
            "plugOn.wav",
            ]
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 5555        # Port to listen on (non-privileged ports are > 1023)
    SIZE = int(65536/2)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        for i in files:
            temp = wave.open("temp.wav", 'wb')
            temp.setnchannels(1) #mono
            temp.setsampwidth(2)
            temp.setframerate(16000)
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('SEND Connected by', addr)

                # Receive the data in small chunks and retransmit it
                print("FILE: "+i)
                f = open("./voice_files/"+i, "rb")
                header = f.read(44)
                size = 1
                while size > 0:
                    read = f.read(SIZE)
                    size = len(read)
                    print(size)
                    conn.sendall(read)
            '''
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
                        temp.writeframesraw(recv)
                    except KeyboardInterrupt:
                        temp.close()
            '''
        s.close()
        temp.close()

def main():
    send_stuff()

if __name__ == "__main__":
    main()
