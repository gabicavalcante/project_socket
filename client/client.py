#!/usr/bin/python

"""
Client to test the auth_server_thread.py
Ctr+c will close the client.
"""

import socket  # connection support

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1'
PORT = 5151
BUFFER_SIZE = 1024

token = ''
email = 'gabicavalcantesilva@gmail.com'
password = '12345'

# connection to hostname on the port.
s.connect((HOST, PORT))

print 'connect authentication...'

response = raw_input('SAY HELLO (y/n): ')
if response:
    s.sendall(b'HELO')
    print 'saying hello...'

    data = s.recv(BUFFER_SIZE)  # receive the client data
    print 'receiving...'
    print 'Received >> \n' + data + '\n'

response = raw_input('AUTHENTICATION (y/n): ')
if response:
    s.sendall(b'AUTH EMAIL:{} PASSWORD:{}'.format(email, password))
    print 'asking for authentication...'

    data = s.recv(BUFFER_SIZE)  # receive the client data
    print 'receiving...'
    print 'Received >> \n' + data + '\n'
    if not 'Unauthorized' in data:
        token = data.split('TOKEN ')[1]

response = raw_input('BYE (y/n): ')
if response:
    s.sendall(b'BYE')
    print 'saying bye...'

    data = s.recv(BUFFER_SIZE)  # receive the client data
    print 'receiving...'
    print 'Received >> \n' + data + '\n'

s.close()

#################################################################


PORT = 6161

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print 'connect proxy...'

response = raw_input('SAY HELLO (y/n): ')
if response:
    s.sendall(b'HELO')
    print 'saying hello...'

    data = s.recv(BUFFER_SIZE)  # receive the client data
    print 'receiving...'
    print 'Received >> \n' + data + '\n'

response = raw_input('SELECT PROJECTS (y/n): ')
if response:
    s.sendall(b'SELECT_PROJECTS TOKEN {}'.format(token))
    data = s.recv(BUFFER_SIZE)  # receive the client data
    print 'receiving...'
    print 'Received >> \n' + data + '\n'

"""
response = raw_input('VALIDATION TOKEN (y/n): ')
if response:
    s.sendall(b'TOKEN {}'.format(token))
    print 'sending token_manage...'

    data = s.recv(BUFFER_SIZE)  # receive the client data
    print 'receiving...'
    print 'Received >> \n' + data + '\n'
"""