import socket
import time


class SocketHandler:
    def __init__(self, timeout=10.0):
        if timeout is None:
            timeout = 10.0
        self.TIMEOUT = timeout
        self.PORT = 54321
        self.sock = socket.socket()

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
            while True:
                data_block = self.sock.recv(2**16).decode()
                # A newline at the end means the whole data block was received
                if '\n' in data_block:
                    break
                # If no data was received, check if the connection was closed
                if len(data_block) == 0:
                    self.sock.settimeout(2)
                    # Sending data may throw an exception if the pipe is broken
                    bytes_received = self.send_data('test')
                    if bytes_received == 0:
                        raise BrokenPipeError
                    self.sock.settimeout(timeout)

            return data_block

        except BrokenPipeError:
            print('Network socket closed (presumably by server). Quitting')

        except Exception as msg:
            if msg == socket.timeout():
                print('Timed out polling data.')
            else:
                print('Could not poll for data: ', msg)

        return ''

    def send_data(self, string):
        if string[-1:] != '\n':
            string += '\n'
        # Returns the number of bytes sent
        return self.sock.send(string.encode('ascii'))
