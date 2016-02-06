#!/usr/bin/env python3
import socket
import json
import sys
import time

class Connector:
    def __init__(self):
        self.TIMEOUT = 5.0
        self.PORT = 54321
        pass

    def connect(self, host = ''):
        self.sock = socket.socket()
        if host == '':
            host = socket.gethostname()

        t_start = time.time()
        error_msg = ''
        while time.time() - t_start <= self.TIMEOUT:
            try:
                self.sock.connect((host, self.PORT))
            except OSError as msg:
                error_msg = msg
        print('Could not open socket: ', error_msg)
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
