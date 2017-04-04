#!/usr/bin/env python
"""
select: This module supports asynchronous I/O on multiple file descriptors
        (so, the server can handle with multiple clients at once)
        interface > select(input,output,exception[,timeout])
        the returns will be a tuple of three lists: input, output and exception events.
"""
import logging
import logging.config

from token_manage.token import generate_token, save_token, validate_token
from logsettings import LOG_SETTINGS
logging.config.dictConfig(LOG_SETTINGS)

import select
import signal
import socket
import sys
import threading

import reboot
from db import users_collection


class Server:
    def __init__(self):
        """
        server's constructor
        """
        self.host = '127.0.0.1'
        self.port = 5151
        self.size = 1024
        self.backlog = 5
        self.server = None
        self.threads = []
        reboot.reboot(5151)

    def create_socket(self):
        try:
            logging.info("Connecting server...")
            # create a socket object
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # flag tells the kernel to reuse a local socket in TIME_WAIT state,
            # without waiting for its natural timeout to expire.
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # bind the socket to the host name and port number
            self.server.bind((self.host, self.port))
            # keep a backlog of five connections.
            self.server.listen(5)
        except socket.error, (value, message):
            if self.server:
                self.server.close()
            logging.error("Could not open the socket: " + message)
            sys.exit(1)

    def run(self):
        self.create_socket()
        logging.debug("Server successfully connected port %s | host %s " % (self.port, self.host))
        logging.info("Press Ctrl + C to stop")

        input = [self.server, sys.stdin]
        run = 1
        while run:
            input_ready, output_ready, except_ready = select.select(input, [], [])
            for i in input_ready:
                if i == self.server:
                    # handle the server socket
                    # accepts an incoming connection
                    c = ClientThread(self.server.accept())
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


class ClientThread(threading.Thread):
    """
    Client is a subclasses of Thread class (thread module).
    As a subclass of Thread, we can use the instance as a thread.
    For this, we need call the Thread initialization method:
        threading.Thread.__init__(self)
    """
    def __init__(self, (client, address)):
        logging.debug("Creating a new client | client {0}, address {1}".format(client, address))
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
            # data = bytes.decode(data)

            if data:
                # get the first word in the request
                command = data
                logging.debug("command: %s " % command)
                # logging.debug("content: %s " % data)

                if 'HELO' in command:
                    response_content = 'HELO {}'.format(self.address)
                elif 'AUTH' in command:
                    email = command.split('EMAIL:')[1].split(' PASSWORD:')[0]
                    password = command.split('PASSWORD:')[1]

                    user = users_collection.find_one({"email": email, "password": password})

                    token = generate_token(str(user['_id']))
                    save_token(token)

                    response_content = 'TOKEN {}'.format('123')
                elif 'VALIDATE_TOKEN' in command:
                    token = command.split('TOKEN ')[1]
                    valid = validate_token(token)
                    if valid:
                        response_content = 'VALID'
                    else:
                        response_content = 'NOT VALID'
                else:
                    response_content = 'TCHAU'

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