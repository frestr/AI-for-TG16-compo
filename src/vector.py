from math import sqrt, atan2


class vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x+other.x
        y = self.y+other.y
        return vec(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return vec(x, y)

    def __mul__(self, other):
        """ Assume int/float. In other word, NOT dot product  """
        x = self.x * other
        y = self.y * other
        return vec(x, y)

    def __truediv__(self, other):
        """ Assume  int/float. """
        x = self.x / other
        y = self.y / other
        return vec(x, y)

    def __repr__(self):
        return '[{0.x}, {0.y}]'.format(self)

    def length(self):
        return sqrt(self.x**2 + self.y**2)

    def t_length(self):
        """ Euclidean distance for torus  """
        w = h = 2  # Width and height of grid
        return sqrt(min(abs(self.x), w - abs(self.x))**2 +
                    min(abs(self.y), h - abs(self.y))**2)

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def normalize(self):
        length = self.length()
        if length == 0:
            length = 1
        self.x /= length
        self.y /= length

    def atan2(self):
        return atan2(self.y, self.x)

    def perpendicular(self):
        return vec(-self.y, -self.x)


def dot(A, B):
    return A.x*B.x + A.y*B.y
