from sockethandler import SocketHandler
from datahandler import DataHandler

class MotherRussia:
    '''Mother russia functions as the program object'''

    def __init__(self):
        pass

    def init(self):
        self.data_handler = DataHandler()

        self.connector = SocketHandler()
        self.connector.connect()
        self.connector.send_data('NAME Putin\n')

    def run(self):
        while True:
            raw_data = self.connector.poll_data()
            self.data_handler.parse_data(raw_data)
            self.data_handler.print_raw_json()
