#!/usr/bin/env python
"""
select: This module supports asynchronous I/O on multiple file descriptors
        (so, the server can handle with multiple clients at once)
        interface > select(input,output,exception[,timeout])
        the returns will be a tuple of three lists: input, output and exception events.
"""
import logging
import logging.config

import select
import socket
import sys
import threading

import signal

from logsettings import LOG_SETTINGS
logging.config.dictConfig(LOG_SETTINGS)

sys.path.append('../')
from authserver import db

class Server:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 6161
        self.size = 1024
        self.backlog = 5
        self.server = None
        self.threads = []
        # reboot.reboot(5151)

    def create_socket(self):
        try:
            print "Connecting server..."
            # create a socket object
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # bind the socket to the host name and port number
            self.server.bind((self.host, self.port))
            # keep a backlog of five connections.
            self.server.listen(5)
        except socket.error, (value, message):
            if self.server:
                self.server.close()
            print "Could not open the socket: " + message
            sys.exit(1)

    def run(self):
        self.create_socket()
        input = [self.server, sys.stdin]
        run = 1
        while run:
            input_ready, output_ready, except_ready = select.select(input, [], [])
            for i in input_ready:
                if i == self.server:
                    # handle the server socket
                    # accepts an incoming connection
                    c = Client(self.server.accept())
                    c.start()
                    self.threads.append(c)

                elif i == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    run = 0

        # close all threads created
        self.server.close()
        for c in self.threads:
            c.join()


class Client(threading.Thread):
    """
    Client is a subclasses of Thread class (thread module).
    As a subclass of Thread, we can use the instance as a thread.
    For this, we need call the Thread initialization method:
        threading.Thread.__init__(self)
    """

    def __init__(self, (client, address)):
        print "Creating a new client | client {0}, address {1}".format(client, address)
        threading.Thread.__init__(self)
        # new socket object to communicate with the client
        self.client = client
        # address of the client
        self.address = address
        self.size = 1024

    def run(self):
        """
        This method overrides the run method of the Thread class.
        It will be called automatically when the start() method is called.
        This loop will run until the client decides to close it.
        """
        while True:
            # receive data on the connection
            data = self.client.recv(self.size)
            if data:
                # get the first word in the request
                command = data
                logging.debug("command: %s " % command)
                response_content = ''
                if 'HELO' in command:
                    response_content = 'HELO {}'.format(self.address)
                elif 'VALIDATION TOKEN' in command:
                    token = command.split('TOKEN ')[1]

                    s01 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # connection to hostname on the port.
                    s01.connect(('127.0.0.1', 5151))
                    s01.sendall(b'VALIDATE_TOKEN {}'.format(token))
                    response = s01.recv(1024)

                    if 'NOT VALID' in response:
                        logging.debug('token invalid...')
                        response_content = 'NOT PERMIT'
                    else:
                        logging.debug('token valid...')
                        response_content = 'PERMIT'
                    s01.close()
                elif 'SELECT_PROJECTS' in command:
                    token = command.split('TOKEN ')[1]

                    s01 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # connection to hostname on the port.
                    s01.connect(('127.0.0.1', 5151))
                    s01.sendall(b'VALIDATE_TOKEN {}'.format(token))
                    response = s01.recv(1024)
                    s01.close()

                    if 'NOT VALID' in response:
                        logging.debug('token invalid...')
                        response_content = 'NOT PERMIT'
                    else:
                        logging.debug('token valid...')
                        projects = str(list(db.project_collection.find()))
                        response_content = projects

                elif 'BYE' in command:
                    break

                # sends data to the client
                status = self.client.send(response_content)
                # the return of send() are the byte sent
                # so, we can check if the data was sent successfully
                if not status:
                    print "data wasn't sent successfully"
            else:
                print "Closing client | client {0}, address {1}".format(self.client, self.address)
                self.client.close()
                break


def signal_handler(sig, frame):
    """
    Signal handler to stop the program if the
    user pressed ctrl + c in the terminal
    :param sig: signal number
    :param frame: current stack frame
    source: https://docs.python.org/2/library/signal.html
    """
    print('stopping the program...')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    s = Server()
    s.run()
