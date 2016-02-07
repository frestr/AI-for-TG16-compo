from sockethandler import SocketHandler
from datahandler import DataHandler
from bot import Bot


class MotherRussia:
    '''Mother russia functions as the program object'''

    def __init__(self, debug_mode=False, timeout=10.0):
        self.data_handler = DataHandler()
        self.connector = SocketHandler(timeout)
        self.debug = debug_mode

    def __enter__(self):
        return self

    def __exit__(self, exec_type, value, traceback):
        if isinstance(value, KeyboardInterrupt):
            print('\r\rRecieved keyboard interrupt')
        elif isinstance(value, SystemExit):
            print('Recieved system exit signal')
        elif isinstance(value, Exception):
            print('Exception: ', value)

        print('Attempting to clean up...')
        clean_error = self.clean()
        if isinstance(clean_error, Exception):
            print('Could not clean up: ', clean_error)
        else:
            print('Done')

        if not self.debug:
            return True

    def init(self):
        self.bot = Bot()
        socket_error = self.connector.connect()
        if isinstance(socket_error, Exception):
            raise socket_error
        self.connector.send_data('NAME Putin')

    def run(self):
        while True:
            raw_data = self.connector.poll_data()
            json_error = self.data_handler.parse_data(raw_data)
            if isinstance(json_error, ValueError):
                raise json_error
            # self.data_handler.print_raw_json()

            self.bot.update_state(self.data_handler)
            self.bot.make_decisions()

            while len(self.bot.commands) > 0:
                command = self.bot.get_command()
                self.connector.send_data(command)

        self.clean()

    def clean(self):
        try:
            if self.connector.sock is not None:
                self.connector.close()
        except Exception as e:
            return e
