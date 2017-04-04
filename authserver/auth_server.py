#!/usr/bin/python

import logging
import logging.config
import os
import signal  # catch the ctrl + c
import socket  # connection support
import sys
import time  # access the current time

from db import users_collection
from logsettings import LOG_SETTINGS

sys.path.append('../')
from utils.status import Status
from token_manage.token import generate_token, save_token, validate_token

logging.config.dictConfig(LOG_SETTINGS)


class Server:
    def __init__(self):
        """
        server's constructor
        :param port: port to connection
        """
        self.host = '127.0.0.1'  # host
        self.port = 5050  # port
        self.socket = None
        self.size = 1024
        self.backlog = 5
        # method the reboot port if it's used
        # for now, it's not necessary
        # reboot(self.port)

    def create_socket(self):
        # factory socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a new socket object
        # flag tells the kernel to reuse a local socket in TIME_WAIT state,
        # without waiting for its natural timeout to expire.
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start_server(self):
        """
        Method to start the server
        """
        try:
            self.create_socket()
            logging.debug("Serving HTTP on port %s | host %s " % (self.port, self.host))
            self.socket.bind((self.host, self.port))  # bind the socket to a local address
            self.socket.listen(self.backlog)  # maximum number of connections
        except Exception as exc:
            logging.error("Exception %s " % exc)
            self.shutdown()
            sys.exit(1)

        logging.debug("Server successfully connected port %s | host %s " % (self.port, self.host))
        logging.info("Press Ctrl + C to stop")
        self._doing_connections()

    def shutdown(self):
        """
        Method to shutdown the server
        """
        try:
            logging.info("Shutting down the server")
            self.socket.shutdown(socket.SHUT_RDWR)
        except Exception as exc:
            logging.error("Problems to shutdown the server, I'm sorry. Check if it was already closed. %s " % exc)

    def _doing_connections(self):
        """
        Method to make the connection
        """

        logging.info("Waiting Request...")

        # socket to client and clients address .accept - accept connection
        client_connection, client_address = self.socket.accept()

        while True:
            # accept(): Return a new socket representing the connection, and the address of the client

            logging.debug("connection from: {}' ".format(client_address))

            data = client_connection.recv(self.size)  # receive the client data
            request_string = bytes.decode(data)  # decode the request to string

            # get the first word in the request
            os.environ["REQUEST_METHOD"] = request_string.split(' ')[0]
            logging.debug("method: %s " % os.environ["REQUEST_METHOD"])
            logging.debug("content: %s " % request_string)

            response_content = ''

            if os.environ["REQUEST_METHOD"] == 'HELO':
                response_content = 'HELO {}'.format(client_address)
            elif os.environ["REQUEST_METHOD"] == 'AUTH':
                email = request_string.split('EMAIL:')[1].split(' PASSWORD:')[0]
                password = request_string.split('PASSWORD:')[1]

                user = users_collection.find_one({"email": email, "password": password})

                token = generate_token(str(user['_id']))
                save_token(token)

                response_content = 'TOKEN {}'.format(token)
            elif os.environ["REQUEST_METHOD"] == 'VALIDATE_TOKEN':
                token = request_string.split('TOKEN ')[1]
                valid = validate_token(token)
                if valid:
                    response_content = 'VALID'
                else:
                    response_content = 'NOT VALID'
            elif os.environ["REQUEST_METHOD"] == 'BYE':
                break

            response_headers = self._build_header(Status.CODE200)
            server_response = response_headers.encode() + response_content
            client_connection.sendall(server_response)
            logging.info("closing connection with client...")

        client_connection.close()

    @staticmethod
    def _build_header(param):
        """
        Method to build a response header
        :param status: 200 if the page was found or 400 if not
        :return: a response header
        """
        header = ""
        if param == Status.CODE200:
            header = 'HTTP/1.0 200 OK\n'
        elif param == Status.CODE404:
            header = 'HTTP/1.1 404 Not Found\n'

        current_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: ' + current_time + '\n'
        header += 'Server: Unice\n'
        header += 'MIME-version: 1.0\n'
        header += 'Content-type: text/html\n'

        return header

    @staticmethod
    def _args_handler(args):
        """
        Method to split the argument and get the parameters
        to build the file name that will be send as server's answer
        :param args: url arguments
        :return: file name
        """
        list_args = args.split('&')
        file_name = ""
        for param in list_args:
            file_name += param.split('=')[1]
        return file_name + ".html"


def signal_handler(sig, frame):
    """
    Signal handler to stop the program if the
    user pressed ctrl + c in the terminal
    :param sig: signal number
    :param frame: current stack frame
    source: https://docs.python.org/2/library/signal.html
    """
    logging.info('stopping the server...')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# method main
if __name__ == '__main__':
    logging.info('starting web server...')
    server = Server()
    server.start_server()
