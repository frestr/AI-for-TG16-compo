from collections import deque
import math
import copy
import entities


class Bot:
    '''Bot is the artificial intelligence itself'''

    def __init__(self):
        self.commands = deque()
        self.actions = {'accel': 'ACCELERATE', 'left': 'LEFT',
                        'right': 'RIGHT', 'missile': 'MISSILE',
                        'seeking': 'SEEKING', 'mine': 'MINE'}
        self.ticks = 0
        self.shoot_rate = 0

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
        for angle in range(0, 360, 10):
            radians = (self.ship.rotation + angle) * math.pi / 180
            if self.simulate(radians):  # NB! Radians
                if angle == 0:
                    if (self.shoot_rate != 0 and
                            self.ticks % self.shoot_rate == 0):
                        self.shoot()
                elif angle < 180:
                    self.turn('r')
                else:
                    self.turn('l')
                break

    def accelerate(self):
        self.commands.append(self.actions['accel'])

    def shoot(self, seeking=False):
        self.commands.append(self.actions['seeking' if seeking else 'missile'])

    # Rate is in "1 shot per x ticks"
    def calculate_shoot_rate(self, distance):
        coeff = 3 # Lower coefficient gives higher shoot rate
        rate = int(coeff * distance)
        return rate if rate != 0 else 1

    def turn(self, direction):
        if direction != 'r' and direction != 'l':
            print('Invalid rotation argument (must be either r or l)')
        else:
            direction = 'right' if direction == 'r' else 'left'
            self.commands.append(self.actions[direction])

    def get_distance(self, v1, v2):
        w = h = 2 # Width and height of grid
        return math.sqrt(min(abs(v1.x-v2.x), w - abs(v1.x-v2.x))**2 +
                         min(abs(v1.y-v2.y), h - abs(v1.y-v2.y))**2)


    def get_closest_opponent(self):
        shortest_dist = 999999
        shortest_dist_opponent = None
        for opponent in self.opponents:
            distance = self.get_distance(self.ship.position, opponent.position)
            if distance < shortest_dist:
                shortest_dist = distance
                shortest_dist_opponent = opponent
        return shortest_dist_opponent

    # Returns True when pointing towards point
    def point_towards(self, point):
        desired_angle = math.atan2(point.y - self.ship.position.y,
                                   point.x - self.ship.position.x)
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

    def simulate(self, rotation):
        target = self.get_closest_opponent()
        if target is not None:
            # Construct a missile
            velocity_x = math.cos(rotation) * 0.05
            velocity_y = math.sin(rotation) * 0.05
            temp_data = {'x': self.ship.position.x, 'y': self.ship.position.y,
                         'velocityX': velocity_x,
                         'velocityY': velocity_y,
                         'type': 'NORMAL',
                         'rotation': rotation, 'energy': 1000, 'owner': 'me'}
            missile = entities.Missile(temp_data)

            target_movement = target.get_movement(2*int(1000/50))
            missile_movement = missile.get_movement(2*int(1000/50))
            for tick in range(min(len(target_movement), len(missile_movement))):
                if (target_movement[tick] - missile_movement[tick]).length() <= 0.1:
                    distance = self.get_distance(target.position, self.ship.position)
                    self.shoot_rate = self.calculate_shoot_rate(distance)
                    return True

        self.shoot_rate = 0
        return False
