import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('fca5:7846:cb2e:639c:ec9d:70c6:b597:2b84', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:

    # Send data
    message = b'This'
    print('sending {!r}'.format(message))
    sock.sendall(message)

    while True:
        data = sock.recv(40)
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()