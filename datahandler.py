import sockethandler
import json

class DataHandler:
    def __init__(self):
        self.is_dead = False
        self.is_end_of_round = False

    def parse_data(self, raw_data):
        self.data = json.loads(raw_data)

        message_type = self.data['messagetype']
        if message_type == 'dead':
            self.is_dead = True

        elif message_type == 'endofround':
            self.is_end_of_round = True

        elif message_type == 'stateupdate':
            self.update_state_data(self.data)

    def update_state_data(self, data):
        pass

    def print_raw_json(self):
        print(self.data)

