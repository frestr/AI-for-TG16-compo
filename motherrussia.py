from sockethandler import SocketHandler
from datahandler import DataHandler
from bot import Bot

class MotherRussia:
    '''Mother russia functions as the program object'''

    def __init__(self):
        pass

    def init(self):
        self.bot = Bot()
        self.data_handler = DataHandler()

        self.connector = SocketHandler()
        self.connector.connect()
        self.connector.send_data('NAME Putin')

    def run(self):
        while True:
            raw_data = self.connector.poll_data()
            self.data_handler.parse_data(raw_data)
            # self.data_handler.print_raw_json()

            self.bot.update_state(self.data_handler)
            self.bot.make_decisions()

            while len(self.bot.commands) > 0:
                command = self.bot.get_command()
                self.connector.send_data(command)

        self.connector.close()            

