from vectors_likeablejuniper import Vector
import math

class CelestialObject:
    def __init__(self, position : Vector, mass : float, v : Vector, color : list = (0, 0, 0), radius : float = 0.0, isSun : bool = False):
        self.position = position
        self.mass = mass
        self.color = color
        if radius:
            self.radius = radius
        else:
            self.radius = [50, 100][int(isSun)]/3 * math.sqrt(self.mass)
        self.v = v
        self.accel = Vector(0, 0)
        self.isSun = isSun