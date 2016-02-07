from sockethandler import SocketHandler
from datahandler import DataHandler
from bot import Bot

class MotherRussia:
    '''Mother russia functions as the program object'''

    def __init__(self):
        self.data_handler = DataHandler()
        self.connector = SocketHandler()

    def __enter__(self):
        return self

    def __exit__(self, exec_type, value, traceback):
        if isinstance(value, KeyboardInterrupt):
            print('Recieved keyboard interrupt')
        elif isinstance(value, SystemExit):
            print('Recieved system exit signal')
        else:
            print('Exception: ', value)
        print('Attempting to clean up')
        self.clean()
        return True  # Prevents further error messages

    def init(self):
        self.bot = Bot()
        self.connector.connect()
        self.connector.send_data('NAME Putin')

    def run(self):
        while True:
            raw_data = self.connector.poll_data()
            json_error = self.data_handler.parse_data(raw_data)
            if isinstance(json_error, ValueError):
                # The exception will contain the string 'Extra data' if the raw data
                # it received was incomplete. Therefore, try to receive new raw data
                if 'Extra data' in str(json_error):
                    continue
                else:
                    # In most cases, this error will be 'Expecting value', because
                    # the block of raw data it received was empty
                    raise json_error
            # self.data_handler.print_raw_json()

            self.bot.update_state(self.data_handler)
            self.bot.make_decisions()

            while len(self.bot.commands) > 0:
                command = self.bot.get_command()
                self.connector.send_data(command)

        self.clean()

    def clean(self):
        if self.connector.sock is not None:
            self.connector.close()

