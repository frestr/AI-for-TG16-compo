from vector import vec
from math import cos, sin

# Global constants
MISSILE_MAX_SPEED = 0.05


class Entity:
    def __init__(self, data):
        "Rudimentary class for entities"
        self.update(data)

    def speed(self):
        return self.velocity.length()

    def update(self, data):
        self.position = vec(data['x'], data['y'])
        self.velocity = vec(data['velocityX'], data['velocityY'])
        self.rotation = data['rotation']
        self.energy = data['energy']


class Ship(Entity):
    "Entity-derived class for AI/human ships"
    def update(self, data):
        super(Ship, self).update(data)
        self.id = data['id']

    def get_movement(self, number_of_ticks):

        positions = []
        # Initial conditions
        pos = self.position
        vel = self.velocity
        energy = self.energy
        is_dead = False
        for t in range(number_of_ticks):
            if energy <= 0 or is_dead:
                positions.append(vec(0, 0))
                continue

            angle = pos.atan2()

            if pos.length() < 0.1:
                is_dead = True
                positions.append(vec(0,0))
                continue

            force = pos.length() / energy
            vel.x -= cos(angle) * force
            vel.y -= sin(angle) * force

            if vel.x > 0.05: vel.x = 0.05
            if vel.y > 0.05: vel.y = 0.05
            if vel.x < -0.05: vel.x = -0.05
            if vel.y < -0.05: vel.y = -0.05

            pos += vel
            energy -= 1

            if pos.x > 1.0: pos.x = -1.0
            elif pos.x < -1.0: pos.x = 1.0
            if pos.y > 1.0: pos.y = -1.0
            elif pos.y < -1.0: pos.y = 1.0

            positions.append(pos)

        return positions


class Missile(Entity):
    "Entity-derived class for missiles"
    def update(self, data):
        super(Missile, self).update(data)
        self.type = data['type']
        self.owner = data['owner']

    def get_movement(self, number_of_ticks):

        positions = []
        # Initial conditions
        pos = self.position
        vel = self.velocity
        energy = self.energy
        rotation = self.rotation
        is_dead = False
        for t in range(number_of_ticks):
            if is_dead:
                positions.append(vec(0, 0))
                continue
            elif pos.length() < 0.1:
                is_dead = True
                positions.append(vec(0, 0))
                continue

            if vel.length() > MISSILE_MAX_SPEED:
                velocityAngle = vel.atan2()
                vel.x = cos(velocityAngle) * MISSILE_MAX_SPEED
                vel.y = sin(velocityAngle) * MISSILE_MAX_SPEED

            # Force only depends on distance from the sun
            force = pos.length() / 1000
            angle = pos.atan2()
            vel.x -= cos(angle) * force
            vel.y -= sin(angle) * force

            pos += vel

            if pos.x > 1.0: pos.x = -1.0
            elif pos.x < -1.0: pos.x = 1.0
            if pos.y > 1.0: pos.y = -1.0
            elif pos.y < -1.0: pos.y = 1.0

            positions.append(pos)

            # Always point in the right direction
            if self.type == "NORMAL":
                rotation = vel.atan2()

            # Might be a bug. Logically, this should be before pos+=vel
            if energy < 10:
                vel /= 1.01
                continue

            if self.type == "MINE":
                vel.x += cos(rotation) * 0.0005
                vel.y += sin(rotation) * 0.0005
                energy -= 1
                continue

            energy -= 50

            if self.type == "NORMAL":
                vel.x += cos(rotation) * (energy / 1000000.0)
                vel.y += sin(rotation) * (energy / 1000000.0)
            elif self.type == "SEEKING":
                vel.x += cos(rotation) * (energy / 100000.0)
                vel.y += sin(rotation) * (energy / 100000.0)

        return positions
