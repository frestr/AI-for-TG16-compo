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
        self.curr_target = None
        self.curr_target_ticks = 99999
        self.curr_target_rotation = 0

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
        #  Observation: Bots that always fire at full speed, often win
        #  It pays off to be hard on the trigger
        ticks = 2*(1000//50)
        self.calculate_own_orbit(ticks)
        self.calculate_target_orbits(ticks)
        self.calculate_own_missile_orbits('NORMAL', ticks)

        lowest_ticks = self.curr_target_ticks - 1
        lowest_ticks_rotation = None
        lowest_ticks_target = None
        for target in self.opponents:
            ticks, rotation = self.check_collision(target)
            if ticks is not None and rotation is not None and ticks < lowest_ticks:
                lowest_ticks = ticks
                lowest_ticks_rotation = rotation
                lowest_ticks_target = target

        # The logic here is fishy
        if abs(lowest_ticks - self.curr_target_ticks) < 5:
            lowest_ticks_target = self.curr_target
            lowest_ticks_rotation = self.curr_target_rotation
        # the self.curr_* aren't updated
        if (lowest_ticks_rotation is not None and
                lowest_ticks_target is not None and
                self.point_towards(lowest_ticks_rotation)):
            distance = self.get_distance(lowest_ticks_target.position, self.ship.position)
            self.shoot_rate = self.calculate_shoot_rate(distance)
            if (self.shoot_rate != 0 and self.ticks % self.shoot_rate == 0):
                self.shoot('missile')

        #  The bot may come down here doing nothing, since all ifs were false

    def accelerate(self):
        self.commands.append(self.actions['accel'])

    def shoot(self, m_type='missile'):
        self.commands.append(self.actions[m_type])

    # Rate is in "1 shot per x ticks"
    def calculate_shoot_rate(self, distance):
        coeff = 2  # Lower coefficient gives higher shoot rate
        rate = int(coeff * distance)
        return rate if rate != 0 else 1

    def turn(self, direction):
        if direction != 'r' and direction != 'l':
            print('Invalid rotation argument (must be either r or l)')
        else:
            direction = 'right' if direction == 'r' else 'left'
            self.commands.append(self.actions[direction])

    def get_closest_missiles(self, radius):
        """ Returns a list of format [[missile, distance, ...]  """
        if len(self.missiles) == 0:
            return []

        closest_missiles = []
        for m in self.missiles:
            if m.owner == self.ship.id:
                continue
            distance = self.get_distance(self.ship.position, m.position)
            if distance <= radius:
                closest_missiles.append([m, distance])

        return sorted(closest_missiles, key=lambda x: x[1], reverse=True)

    def get_distance(self, v1, v2):
        """ Euclidean distance for torus  """
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

    # Returns True when has correct angle (in degrees)
    def point_towards(self, angle):
        #desired_angle = math.atan2(point.y - self.ship.position.y,
        #                           point.x - self.ship.position.x)
        #desired_angle *= (180.0 / math.pi)  # Convert to degrees
        #ship_rotation = self.ship.rotation
        #if 180 <= ship_rotation < 360:
        #    ship_rotation = ship_rotation - 360
        #angle_diff = (angle - ship_rotation + 180) % 360 - 180
        angle_diff = angle
        if angle_diff > 5:
            self.turn('r')
        elif angle_diff < -5:
            self.turn('l')
        return -5 < angle_diff < 5

    def get_temp_missile(self, m_type, rotation):
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

        temp_data = {'x': self.ship.position.x, 'y': self.ship.position.y,
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
        if 180 <= ship_rotation < 360:
            ship_rotation = ship_rotation - 360
        for rotation in range(0, 360, 10):
            angle_diff = (rotation - ship_rotation + 180) % 360 - 180
            temp_data = self.get_temp_missile(m_type, rotation * (math.pi / 180))
            missile = entities.Missile(temp_data)
            self.own_missile_orbits[angle_diff] = missile.get_movement(ticks)

    def check_collision(self, target):
        lowest_ticks = 99999
        lowest_ticks_rotation = 0
        if target is not None:
            for rotation, missile_orbit in self.own_missile_orbits.items():
                for tick in range(min(len(self.target_orbit[target]), len(missile_orbit), len(self.own_orbit))):
                    if (self.target_orbit[target][tick] - missile_orbit[tick]).t_length() <= 0.1:
                        ticks = tick + abs(rotation) // 10
                        if ticks < lowest_ticks:
                            lowest_ticks = ticks
                            lowest_ticks_rotation = rotation

        if lowest_ticks != 99999:
            return lowest_ticks, lowest_ticks_rotation
        else:
            return None, None

    def simulate_missile(self, missile, self_movement, ticks=int(1000/100)):
        missile_movement = missile.get_movement(ticks)
        for tick in range(min(len(self_movement), len(missile_movement))):
            distance = (self_movement[tick] - missile_movement[tick]).t_length()
            if distance <= 0.1:
                return self_movement[tick]
