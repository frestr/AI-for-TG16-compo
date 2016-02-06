import socket
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
                s = '\r{:<5.2f}'.format(self.TIMEOUT
                                        - time.time() + t_start)
                sys.stdout.write(s)
                error_msg = msg
        print('\nCould not create socket: ', error_msg)
        sys.exit(1)

    def poll_data(self, timeout = None):
        try:
            self.sock.settimeout(timeout)
            data_block = self.sock.recv(2**14)
            return data_block.decode()

        except Exception as msg:
            if msg == socket.timeout():
                print('Timed out polling data.')
            else:
                print('Could not poll for data: ', msg)
                
    def send_data(self, string):
        if string[-1:] != '\n':
            string += '\n'
        self.sock.send(string.encode('ascii'))
