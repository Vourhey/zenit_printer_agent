import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('fca5:7846:cb2e:639c:ec9d:70c6:b597:2b84', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

choice = -1
while True:
    print('Choose a model:\n1. Cube\n2. Stans')
    choice = int(input(">"))
    if 0 < choice < 3:
        break

choice -= 1

print('Please visit http://[fced:97fd:da23:b15d:7897:4fa6:57b3:f2a3]/webcam/?action=stream for live stream')

try:

    # Send data
    message = choice.to_bytes(1, 'big')
    print('sending {!r}'.format(message))
    sock.sendall(message)

    while True:
        data = sock.recv(40)
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()
