import math
from vectors_likeablejuniper import Vector

UNIVERSAL_GRAVITY = 10 #6.67 * 10**(-11)

def distance(pos1, pos2):
    return math.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)


def getAttractionForce(m1, m2, d):
    if d == 0: # Points have 0 distance, attraction infinite
        return float("inf")
    return UNIVERSAL_GRAVITY*m1*m2 / d**2


def getAttractionVector(f_g, m1Pos, m2Pos) -> Vector:
    """
    Returns a Vector class object pointing in the direction of m2Pos with a magnitude of f_g
    """
    angle = Vector(m2Pos[0]-m1Pos[0], m2Pos[1]-m1Pos[1]).direction()
    
    return Vector(f_g, 0).rotate(angle)
