from collections import deque
import math
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
        if data.is_dead or data.is_end_of_round:
            self.ticks = 0
            self.shoot_rate = 0
        else:
            self.ticks += 1

        self.ship = data.myself
        self.opponents = data.opponents
        self.missiles = data.missiles

    def make_decisions(self):
        ticks = 2*(1000//50)
        self.calculate_own_orbit(ticks)
        self.calculate_target_orbits(ticks)
        self.calculate_own_missile_orbits('NORMAL', ticks)

        lowest_ticks = 99999
        lowest_ticks_rotation = 370
        lowest_ticks_target = None
        for target in self.opponents:
            ticks, rotation = self.check_collision(target)
            if ticks is not None and rotation is not None and ticks < lowest_ticks:
                lowest_ticks = ticks
                lowest_ticks_rotation = rotation
                lowest_ticks_target = target
        if (lowest_ticks_rotation is not None and
                lowest_ticks_target is not None and
                self.point_towards(lowest_ticks_rotation)):
            
            distance = self.get_distance(lowest_ticks_target.position, self.ship.position)
            self.shoot_rate = self.calculate_shoot_rate(distance)
            if (self.shoot_rate != 0 and 
                    self.ticks % self.shoot_rate == 0 and
                    self.ship.energy - 10*lowest_ticks > 0):
                self.shoot('missile')

    def accelerate(self):
        self.commands.append(self.actions['accel'])

    def shoot(self, m_type='missile'):
        self.commands.append(self.actions[m_type])

    # Rate is in "1 shot per x ticks"
    def calculate_shoot_rate(self, distance):
        coeff = 2  # Lower coefficient gives higher shoot rate
        rate = int(coeff * distance)
        return 1
        #return rate if rate != 0 else 1

    def turn(self, direction):
        if direction != 'r' and direction != 'l':
            print('Invalid rotation argument (must be either r or l)')
        else:
            direction = 'right' if direction == 'r' else 'left'
            self.commands.append(self.actions[direction])

    def get_distance(self, v1, v2):
        """ Euclidean distance for torus  """
        w = h = 2  # Width and height of grid
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

    # Returns True when has correct angle (in degrees)
    def point_towards(self, angle: 'degrees'):
        angle_diff = angle
        if angle_diff > 5:
            self.turn('r')
        elif angle_diff < -5:
            self.turn('l')
        return angle == 0

    def get_temp_missile(self, m_type, rotation: 'radians', position):
        if m_type == 'MINE':
            rotation = self.ship.position.atan2()
            velocity_x = math.cos(rotation) * 0.005
            velocity_y = math.sin(rotation) * 0.005
            energy = 5000
        elif m_type == 'SEEKING':
            velocity_x = math.cos(rotation) * 0.03
            velocity_y = math.sin(rotation) * 0.03
            energy = 1000
        else:
            velocity_x = math.cos(rotation) * 0.05
            velocity_y = math.sin(rotation) * 0.05
            energy = 1000

        temp_data = {'x': position.x, 'y': position.y,
                     'velocityX': velocity_x,
                     'velocityY': velocity_y,
                     'type': m_type,
                     'rotation': rotation, 'energy': energy,
                     'owner': 'me'}

        return temp_data

    def calculate_own_orbit(self, ticks):
        self.own_orbit = self.ship.get_movement(ticks)

    def calculate_target_orbits(self, ticks):
        self.target_orbit = {}
        for target in self.opponents:
            self.target_orbit[target] = target.get_movement(ticks)

    def calculate_own_missile_orbits(self, m_type, ticks):
        self.own_missile_orbits = {}
        ship_rotation = self.ship.rotation
        rotations = [((r + 180) % 360 - 180) for r in range(0, 360, 10)]
        for rotation in rotations:
            actual_rotation = rotation + ship_rotation
            pos = self.own_orbit[abs(rotation) % 10]  # Correct for ticks passed
            temp_data = self.get_temp_missile(m_type, actual_rotation * (math.pi / 180),pos)
            missile = entities.Missile(temp_data)
            self.own_missile_orbits[rotation] = missile.get_movement(ticks)

    def check_collision(self, target):
        lowest_ticks = 99999
        lowest_ticks_rotation = 0
        if target is not None:
            for rotation, missile_orbit in self.own_missile_orbits.items():
                for tick in range(len(missile_orbit)):
                    if (self.target_orbit[target][tick] - missile_orbit[tick]).t_length() <= 0.1:
                        ticks = tick + math.ceil(abs(rotation) / 10)
                        if ticks < lowest_ticks:
                            lowest_ticks = ticks
                            lowest_ticks_rotation = rotation
        if lowest_ticks != 99999:
            return lowest_ticks, lowest_ticks_rotation
        else:
            return None, None
