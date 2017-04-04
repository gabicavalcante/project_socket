#!/usr/bin/python

import socket  # connection support

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 5151
token = ''

email = 'raivitor@gmail.com'
password = '12345'

print 'port: {} host: {}'.format(port, host)

# connection to hostname on the port.
s.connect((host, port))

print 'connect authentication...'

response = raw_input('SAY HELLO (y/n)')
if response:
    #### send hello
    s.sendall(b'HELO')
    print 'saying hello...'
    data = s.recv(1024)  # receive the client data

    print 'receiving...'
    print 'Received >> \n-------\n' + data + '\n-------\n'

response = raw_input('AUTHENTICATION (y/n)')
if response:
    #### authentication
    s.sendall(b'AUTH EMAIL:{} PASSWORD:{}'.format(email, password))
    print 'asking for authentication...'
    data = s.recv(1024)  # receive the client data

    print 'receiving...'
    print 'Received >> \n-------\n' + data + '\n-------'
    token = data.split('TOKEN ')[1]

response = raw_input('BYE (y/n)')
if response:
    #### bye
    s.sendall(b'BYE')
    print 'saying bye...'
    data = s.recv(1024)  # receive the client data

    print 'receiving...'
    print 'Received >> \n-------\n' + data + '\n-------'

s.close()

######-----------------

host = '127.0.0.1'
port = 6060

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

print 'connect proxy...'

response = raw_input('SAY HELLO (y/n)')
if response:
    #### send hello
    s.sendall(b'HELO')
    print 'saying hello...'
    data = s.recv(1024)  # receive the client data

    print 'receiving...'
    print 'Received >> \n-------\n' + data + '\n-------\n'

response = raw_input('VALIDATION TOKEN (y/n)')
if response:
    #### ask for validation token_manage
    s.sendall(b'TOKEN {}'.format(token))
    print 'sending token_manage...'
    data = s.recv(1024)  # receive the client data

    print 'receiving...'
    print 'Received >> \n-------\n' + data + '\n-------\n'
