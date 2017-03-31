#!/usr/bin/python

import socket  # connection support

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 5050

# connection to hostname on the port.
s.connect((host, port))

# send hello
s.send(b'HELO {}'.format(host))

# Receive no more than 1024 bytes
data = s.recv(1024)

s.close()

print('Received', repr(data))