from collections import deque
from vector import vec

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

    def update_state(self, data):
        self.velocity = vec(data.myself['velocityX'], data.myself['velocityY'])

    def make_decisions(self):
        if self.velocity.length() < 0.02:
            self.accelerate()    
            self.shoot()

    def accelerate(self):
        self.commands.append(self.actions['accel'])

    def shoot(self, seeking = False):
        self.commands.append(self.actions['seeking' if seeking else 'missile'])

    
