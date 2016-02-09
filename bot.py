from collections import deque
import math


class Bot:
    '''Bot is the artificial intelligence itself'''

    def __init__(self):
        self.commands = deque()
        self.actions = {'accel': 'ACCELERATE', 'left': 'LEFT',
                        'right': 'RIGHT', 'missile': 'MISSILE',
                        'seeking': 'SEEKING', 'mine': 'MINE'}
        self.ticks = 0

    def get_command(self):
        try:
            command = self.commands.popleft()
            return command
        except IndexError:
            return ''

    def update_state(self, data):
        self.ticks += 1
        self.ship = data.myself
        self.opponents = data.opponents
        self.missiles = data.missiles

    def make_decisions(self):
        closest_opponent = self.get_closest_opponent()
        if closest_opponent is not None:
            if self.point_towards(closest_opponent.position) and self.ticks % 10 == 0:
                self.shoot()

    def accelerate(self):
        self.commands.append(self.actions['accel'])

    def shoot(self, seeking=False):
        self.commands.append(self.actions['seeking' if seeking else 'missile'])

    def turn(self, direction):
        if direction != 'r' and direction != 'l':
            print('Invalid rotation argument (must be either r or l)')
        else:
            self.commands.append(self.actions['right' if direction == 'r' else 'left'])

    def get_closest_opponent(self):
        shortest_dist = 999999
        shortest_dist_opponent = None
        for opponent in self.opponents:
            distance = (self.ship.position - opponent.position).length()
            if distance < shortest_dist:
                shortest_dist = distance
                shortest_dist_opponent = opponent
        return shortest_dist_opponent

    # Returns True when pointing towards point
    def point_towards(self, point):
        desired_angle = math.atan2(point.y - self.ship.position.y, point.x - self.ship.position.x)
        desired_angle *= (180.0 / math.pi)  # Convert to degrees
        ship_rotation = self.ship.rotation
        if 180 <= ship_rotation < 360:
            ship_rotation = ship_rotation - 360
        angle_diff = (desired_angle - ship_rotation + 180) % 360 - 180
        if angle_diff > 5:
            self.turn('r')
        elif angle_diff < -5:
            self.turn('l')
        return -5 < angle_diff < 5
