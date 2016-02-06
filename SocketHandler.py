import socket
import json
import sys
import time

class SocketHandler:
    def __init__(self):
        self.TIMEOUT = 10.0
        self.PORT = 54321
        pass

    def connect(self, host = ''):
        self.sock = socket.socket()
        if host == '':
            host = socket.gethostname()
        self.sock.settimeout(self.TIMEOUT)
        t_start = time.time()
        error_msg = ''
        while time.time() - t_start <= self.TIMEOUT:
            try:
                self.sock.connect((host, self.PORT))
                return 1
            except OSError as msg:
                error_msg = msg
        print('Could not create socket: ', error_msg)
        sys.exit(1)
                
    def poll_data(self, timeout = None):
        try:
            self.sock.settimeout(timeout)
            data_block = self.sock.recv(2**14)
            return data_block.decode()

        except Exception as e:
            if e == socket.timeout():
                print('Timed out polling data.')
            else:
                print('Could not poll for data: ', e)

    def send_data(self, string):
        self.sock.send(string.encode('ascii'))
