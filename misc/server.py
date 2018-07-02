import socket
import time
import sys
import os
import subprocess

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('fca5:7846:cb2e:639c:ec9d:70c6:b597:2b84', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
cmd = ["rosservice", "call", "/make_ask"]
objectives = ['QmaFhGQjwHkhkxwyGsLfGkyF2hjB3xQxN1AWNFrH71ADqB', 'QmWuCcQvNpKwMecASgsGZCDT8ht5V2XEBWhSZ2adpgLLPQ']

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        while True:
            data = connection.recv(1)
            print('received {!r}'.format(data))
            if data:
                data = data.from_bytes(1, 'big')
                cmd.append(objectives[data])
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                logfile = open("/home/zenit/zenit_output.log","r")
                loglines = follow(logfile)
                for line in loglines:
                    connection.sendall(bytes(line, 'utf-8'))
            else:
                print('no data from', client_address)
                break
    finally:
        connection.close()

