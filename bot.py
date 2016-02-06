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

    # We need to figure out exactly how the Bot class should get access to data
    def update(self):
        self.accelerate()    
        self.shoot()

    def accelerate(self):
        self.commands.append(self.actions['accel'])

    def shoot(self, seeking = False):
        self.commands.append(self.actions['seeking' if seeking else 'missile'])

    
