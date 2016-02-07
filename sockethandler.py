import socket
import time


class SocketHandler:
    def __init__(self, timeout=10.0):
        if timeout is None:
            timeout = 10.0
        self.TIMEOUT = timeout
        self.PORT = 54321
        self.sock = socket.socket()
        pass

    def connect(self, host=''):
        if host == '':
            host = socket.gethostname()
        self.sock.settimeout(self.TIMEOUT)
        t_start = time.time()
        error_msg = ''
        while time.time() - t_start <= self.TIMEOUT:
            try:
                self.sock.connect((host, self.PORT))
                return True
            except OSError as msg:
                error_msg = msg

        return error_msg

    def close(self):
        self.sock.close()

    def poll_data(self, timeout=None):
        try:
            self.sock.settimeout(timeout)
            data_block = self.sock.recv(2**16)
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
