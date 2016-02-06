from collections import deque

class Bot:
    '''Bot is the artificial intelligence itself'''

    def __init__(self):
        self.commands = deque()
        self.actions = {'accel': 'ACCELERATE', 'left': 'LEFT',
                        'right': 'RIGHT', 'missile': 'MISSILE',
                        'seeking': 'SEEKING', 'mine': 'MINE'}

    def get_command(self):
        try:
            command = self.commands.popleft()
            return command
        except IndexError as e:
            return ''

    def update(self, data):
        if data.myself['speed'] < 0.02:
            self.accelerate()    
            self.shoot()

    def accelerate(self):
        self.commands.append(self.actions['accel'])

    def shoot(self, seeking = False):
        self.commands.append(self.actions['seeking' if seeking else 'missile'])

    
