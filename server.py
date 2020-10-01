import socket
import sys

def listen_to_homie():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    print ('listening for homie on {} port {}'.format(server_address[0], server_address[1]))
    sock.bind(server_address)

    sock.listen(1)
    while True:
        print('waiting for a connection')
        connection, client_address = sock.accept();
        try:
            print ('connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(16)
                print ('received "{}"'.format(data))
                if data:
                    print ('sending data back to the client')
                    connection.sendall(data)
                else:
                    print ('no more data from {}'.format(client_address))
                    break

        finally:
            # Clean up the connection
            connection.close()
