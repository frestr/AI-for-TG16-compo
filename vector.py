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
        """ Assume int/float  """
        x = self.x * other
        y = self.y * other
        return vec(x, y)

    def length(self):
        return np.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        length = self.length()
        if length == 0:
            length = 1
            self.x /= length
            self.y /= length
