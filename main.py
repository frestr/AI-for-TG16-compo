#!/usr/bin/env python3
import socket
import json
import sys

class Connector:
    def __init__(self):
        pass

    def connect(self, host = ''):
        self.sock = socket.socket()
        if host == '':
            host = socket.gethostname()

        port = 54321
        try:
            self.sock.connect((host, port))
        except OSError as msg:
            print('Could not open socket: ', msg)
            sys.exit(1)
        
    def poll_data(self, timeout = None):
        try:
            self.sock.settimeout(timeout)
            data_block = self.sock.recv(2**14)
            return data_block.decode()

        except socket.timeout:
            print('Timed out polling data.')

    def send_data(self, string):
        self.sock.send(string.encode('ascii'))

def main():
    connector = Connector()
    connector.connect()
    connector.send_data('NAME bob\n')

    while True:
        data = json.loads(connector.poll_data())
        print(data)

if __name__ == "__main__": 
    main()
