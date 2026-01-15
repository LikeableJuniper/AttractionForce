from vectors_likeablejuniper import Vector
import math
from astronomicalMath import *

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

    def applyAttractionForce(self, other: 'CelestialObject') -> Vector:
        dist = distance(self.position, other.position)
                
        # Calculate attraction force vector for two celestial objects
        attractionForceVector = getAttractionVector(getAttractionForce(self.mass, other.mass, dist), self.position, other.position)
        # Divide by mass
        attractionForceVector /= self.mass

        self.accel += attractionForceVector

        return attractionForceVector
    
    def __call__(self):
        self.v += self.accel

        # Update positions by adding velocity
        self.position += self.v
        diffVector = self.position - self.position