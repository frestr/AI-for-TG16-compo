import sockethandler
import json
from math import sqrt

class DataHandler:
    def __init__(self):
        self.is_dead = False
        self.is_end_of_round = False

    def parse_data(self, raw_data):
        try:
            self.data = json.loads(raw_data)
        except ValueError as e:
            print('Error parsing json data:', e)

        message_type = self.data['messagetype']
        if message_type == 'dead':
            self.is_dead = True

        elif message_type == 'endofround':
            self.is_end_of_round = True

        elif message_type == 'stateupdate':
            self.update_state_data(self.data['gamestate'])
        
    def update_state_data(self, data):
        self.missiles = data['missiles'] if 'missiles' in data else []
        self.opponents = data['others'] if 'others' in data else []

        self.myself = data['you']

    def print_raw_json(self):
        print(self.data)

