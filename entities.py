from vector import vec


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


class Missile(Entity):
    "Entity-derived class for missiles"
    def update(self, data):
        super(Missile, self).update(data)
        self.type = data['type']
        self.owner = data['owner']
