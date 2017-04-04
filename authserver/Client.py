#!/usr/bin/env python

"""
Client to test the ServerThread.py
Ctr+c will close the client.
"""

import socket
import sys

HOST = '127.0.0.1'
PORT = 5151
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
sys.stdout.write('connecting... \n')

while 1:
    try:
        sys.stdout.write("send > ")
        line = sys.stdin.readline()
        s.send(line)
        data = s.recv(BUFFER_SIZE)
        sys.stdout.write("receiving > {0}\n".format(data))
    except (KeyboardInterrupt, SystemExit):
        print "\nclosing client...\n"
        sys.exit(1)
    except ValueError:
        print "Could not send message: {0}".format(ValueError.message)
s.close()