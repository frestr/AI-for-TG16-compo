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

    def getMovement(self, number_of_ticks):

        positions = []
        # Initial conditions
        pos = self.position
        vel = self.velocity
        for t in range(number_of_ticks):
            angle = self.position.atan2()

            # Lose 1 energy per tick
            force = pos.length()/(self.energy - t)
            vel.x -= cos(angle) * force
            vel.y -= sin(angle) * force

            if vel.x > 0.05:
                vel.x = 0.05
            if vel.y > 0.05:
                vel.y = 0.05
            if vel.x < -0.05:
                vel.x = -0.05
            if vel.y < -0.05:
                vel.y = -0.05

            pos += vel

            if pos.x > 1.0:
                pos.x = -1.0
            elif pos.x < -1.0:
                pos.x = 1.0
            if pos.y > 1.0:
                pos.y = -1.0
            elif pos.y < -1.0:
                pos.y = 1.0

            positions.append(pos)

        return positions


class Missile(Entity):
    "Entity-derived class for missiles"
    def update(self, data):
        super(Missile, self).update(data)
        self.type = data['type']
        self.owner = data['owner']

    def getMovement(self, number_of_ticks):

        positions = []
        # Initial conditions
        pos = self.position
        vel = self.velocity
        for t in range(number_of_ticks):
            angle = self.position.atan2()

            if vel.length() > MISSILE_MAX_SPEED:
                velocityAngle = vel.atan2()
                vel.x = cos(velocityAngle) * MISSILE_MAX_SPEED
                vel.y = sin(velocityAngle) * MISSILE_MAX_SPEED

            # Lose 50 energy per tick
            force = pos.length()/(self.energy - 50*t)
            vel.x -= cos(angle) * force
            vel.y -= sin(angle) * force

            pos += vel

            if pos.x > 1.0:
                pos.x = -1.0
            elif pos.x < -1.0:
                pos.x = 1.0
            if pos.y > 1.0:
                pos.y = -1.0
            elif pos.y < -1.0:
                pos.y = 1.0

            if (self.energy - t) < 10:
                vel /= 1.01

            positions.append(pos)

        return positions
