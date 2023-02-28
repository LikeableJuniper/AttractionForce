import math
from vectors import *
import pygame as pg

pg.init()
pg.font.init()
mainFont = pg.font.SysFont("Calibri", 20)
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
width, height = pg.display.get_surface().get_size()
screencenter = [width/2, height/2]

SIMULATIONSPEED = 0.1
k = 10
distanceFactor = 0.01

universalGrav = 1.7 # 6.67 * 10**(-11)


class CelestialObject:
    def __init__(self, position : list, mass : float, startAccel : Vector, color : list = (0, 0, 0), radius : float = None, isSun : bool = False):
        self.position = position
        self.mass = mass
        self.color = color
        if radius:
            self.radius = radius
        else:
            self.radius = [50, 100][int(isSun)]/3 * math.sqrt(self.mass)
        self.accel = startAccel
        self.isSun = isSun


def distance(pos1, pos2):
    return math.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)


def getAttractionForce(G, m1, m2, d):
    if d == 0: # Points have 0 distance, attraction infinite
        return float("inf")
    return G*m1*m2 / d**2


def getAttractionVector(f_g, m1Pos, m2Pos):
    """
    Returns a Vector class object pointing in the direction of m2Pos with a magnitude of f_g
    """
    angle = Vector(m2Pos[0]-m1Pos[0], m2Pos[1]-m1Pos[1]).angle()
    
    return Vector(f_g, 0).rotate(angle)


celestialObjects : list[CelestialObject] = [CelestialObject([screencenter[0]+300, screencenter[1]], 6, Vector(0, -20), (255, 0, 255))]
#celestialObjects.append(CelestialObject([screencenter[0]-400, screencenter[1]], 10, Vector(0, 50), (0, 255, 100)))
sunIndex = 0
celestialObjects.insert(sunIndex, CelestialObject(screencenter, 20, Vector(0, 0), (255, 255, 255), isSun=True))

playing = True
objectsCrashed = False

while playing:
    pg.display.update()
    screen.fill((50, 50, 50))
    
    pg.draw.circle(screen, celestialObjects[sunIndex].color, celestialObjects[sunIndex].position, celestialObjects[sunIndex].radius)

    for index, celestialObject1 in enumerate(celestialObjects):
        for index2, celestialObject2 in enumerate(celestialObjects):
            if index == index2:
                continue
            dist = distance(celestialObject1.position, celestialObject2.position)*distanceFactor
            
            # Calculate attraction force vector for two celestial objects
            attractionForceVector1 = getAttractionVector(getAttractionForce(universalGrav, celestialObject1.mass, celestialObject2.mass, dist), celestialObject1.position, celestialObject2.position)
            # Rotate by 180° (math.pi in radians) to get vector in other direction and divide by mass 2
            attractionForceVector2 = attractionForceVector1.rotate(math.pi)/celestialObject2.mass
            # Finally divide by mass 1
            attractionForceVector1 /= celestialObject1.mass

            # Vector addition and scaling by SIMULATIONSPEED for variable simulation speeds
            celestialObject1.accel += attractionForceVector1*SIMULATIONSPEED
            celestialObject2.accel += attractionForceVector2*SIMULATIONSPEED
            
            # Update positions by adding acceleration
            celestialObject1.position = (Vector(celestialObject1.position) + (celestialObject1.accel/celestialObject1.mass)*SIMULATIONSPEED).components
            celestialObject2.position = (Vector(celestialObject2.position) + (celestialObject2.accel/celestialObject2.mass)*SIMULATIONSPEED).components
            diffVector = Vector(celestialObject2.position[0]-celestialObject1.position[0], celestialObject2.position[1]-celestialObject1.position[1])

            pg.draw.circle(screen, celestialObject1.color, celestialObject1.position, celestialObject1.radius)

            # Vectors
            # Accel:
            #pg.draw.line(screen, (0, 255, 100), celestialObject1.position, [celestialObject1.position[0]+celestialObject1.accel.components[0]*k, celestialObject1.position[1]+celestialObject1.accel.components[1]*k], 2)
            # Attraction force
            #pg.draw.line(screen, (255, 0, 0), celestialObject1.position, [celestialObject1.position[0]+attractionForceVector1.components[0]*k*10, celestialObject1.position[1]+attractionForceVector1.components[1]*k*10])
            # difference Vector
            # pg.draw.line(screen, (0, 0, 255), celestialObject1.position, [celestialObject1.position[0]+diffVector.components[0], celestialObject1.position[1]+diffVector.components[1]])

            # Angles
            # difference Vector angle
            # screen.blit(mainFont.render(str(math.degrees(diffVector.angle())), False, (0, 0, 255)), [celestialObject.position[0]+30, celestialObject.position[1]+30])
            # attraction force angle
            # screen.blit(mainFont.render(str(math.degrees(attractionForceVector.angle())), False, (255, 0, 0)), [celestialObject.position[0]+30, celestialObject.position[1]+60])
    
    """celestialObjects.reverse()
    for celestialObject1 in celestialObjects:
        index = celestialObjects.index(celestialObject1)
        for celestialObject2 in celestialObjects[index+1:]:
            dist = distance(celestialObject1.position, celestialObject2.position)/100

            attractionForceVector = getAttractionVector(getAttractionForce(universalGrav, celestialObject1.mass, celestialObject2.mass, dist), celestialObject1.position, celestialObject2.position)/celestialObject1.mass
            celestialObject1.accel = celestialObject1.accel + attractionForceVector*SIMULATIONSPEED
            # celestialObject.position = pg.mouse.get_pos()
            celestialObject1.position = (Vector(celestialObject1.position) + (celestialObject1.accel/celestialObject1.mass)*SIMULATIONSPEED).components
            diffVector = Vector(celestialObject2.position[0]-celestialObject1.position[0], celestialObject2.position[1]-celestialObject1.position[1])

            pg.draw.circle(screen, celestialObject1.color, celestialObject1.position, celestialObject1.radius)

            # Vectors
            # Accel:
            pg.draw.line(screen, (0, 255, 100), celestialObject1.position, [celestialObject1.position[0]+celestialObject1.accel.components[0]*k, celestialObject1.position[1]+celestialObject1.accel.components[1]*k], 2)
            # Attraction force
            pg.draw.line(screen, (255, 0, 0), celestialObject1.position, [celestialObject1.position[0]+attractionForceVector.components[0]*k*10, celestialObject1.position[1]+attractionForceVector.components[1]*k*10])
            # difference Vector
            # pg.draw.line(screen, (0, 0, 255), celestialObject1.position, [celestialObject1.position[0]+diffVector.components[0], celestialObject1.position[1]+diffVector.components[1]])

            # Angles
            # difference Vector angle
            # screen.blit(mainFont.render(str(math.degrees(diffVector.angle())), False, (0, 0, 255)), [celestialObject.position[0]+30, celestialObject.position[1]+30])
            # attraction force angle
            # screen.blit(mainFont.render(str(math.degrees(attractionForceVector.angle())), False, (255, 0, 0)), [celestialObject.position[0]+30, celestialObject.position[1]+60])
    
    celestialObjects.reverse()"""
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            playing = False
