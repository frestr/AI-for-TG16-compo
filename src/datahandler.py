import json
from entities import Ship
from entities import Missile


class DataHandler:
    def __init__(self):
        self.is_dead = False
        self.is_end_of_round = False

    def parse_data(self, raw_data):
        try:
            self.data = json.loads(raw_data)
        except ValueError as e:
            return e

        message_type = self.data['messagetype']

        self.is_dead         = message_type == 'dead'
        self.is_end_of_round = message_type == 'endofround'

        if message_type == 'stateupdate':
            self.update_state_data(self.data['gamestate'])

    def update_state_data(self, data):
        self.missiles = []
        for _m in data['missiles']:
            self.missiles.append(Missile(_m))

        self.opponents = []
        for opponent in data['others']:
            self.opponents.append(Ship(opponent))

        self.myself = Ship(data['you'])

    def print_raw_json(self):
        print(self.data)
