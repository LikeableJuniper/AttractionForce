import math
from vectors import *
import pygame as pg

pg.init()
pg.font.init()
mainFont = pg.font.SysFont("Calibri", 20)
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
width, height = pg.display.get_surface().get_size()
screencenter = Vector([width/2, height/2])
offset = Vector(0, 0)
scrollSpeed = 100
zoom = 1
zoomSpeed = 1.125

trackingIndex = 0

SIMULATIONSPEED = 0.1
k = 10
distanceFactor = 0.01

universalGrav = 1.7 # 6.67 * 10**(-11)


class CelestialObject:
    def __init__(self, position : Vector, mass : float, startAccel : Vector, color : list = (0, 0, 0), radius : float = 0.0, isSun : bool = False):
        self.position = position
        self.mass = mass
        self.color = color
        if radius:
            self.radius = radius
        else:
            self.radius = [50, 100][int(isSun)]/3 * math.sqrt(self.mass)
        self.accel: Vector = startAccel
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


celestialObjects : list[CelestialObject] = [CelestialObject(Vector(screencenter[0]+2000, screencenter[1]), 5, Vector(0, -50), (255, 0, 255))]
#celestialObjects.append(CelestialObject(Vector(screencenter[0]-3000, screencenter[1]), 4, Vector(0, 50), (0, 255, 100)))
sunIndex = 0
celestialObjects.insert(sunIndex, CelestialObject(Vector(screencenter), 100, Vector(0, 0), (255, 255, 255), isSun=True))

playing = True
paused = False
objectsCrashed = False

while playing:
    pg.display.update()
    screen.fill((50, 50, 50))

    if not isinstance(trackingIndex, type(None)):
        offset = -1*(celestialObjects[trackingIndex].position)*zoom + screencenter
    
    if not paused:
        for index1, celestialObject1 in enumerate(celestialObjects):
            for index2, celestialObject2 in enumerate(celestialObjects):
                if index1 == index2:
                    continue
                dist = distance(celestialObject1.position, celestialObject2.position)*distanceFactor
                
                # Calculate attraction force vector for two celestial objects
                attractionForceVector = getAttractionVector(getAttractionForce(universalGrav, celestialObject1.mass, celestialObject2.mass, dist), celestialObject1.position, celestialObject2.position)
                # Divide by mass
                attractionForceVector /= celestialObject1.mass

                # Vector addition and scaling by SIMULATIONSPEED for variable simulation speeds
                celestialObject1.accel += attractionForceVector*SIMULATIONSPEED
                
                # Update positions by adding acceleration
                celestialObject1.position = Vector(celestialObject1.position) + (celestialObject1.accel/celestialObject1.mass)*SIMULATIONSPEED
                diffVector = celestialObject2.position - celestialObject1.position

                pos1 = list(celestialObject1.position*zoom+offset)
                pg.draw.circle(screen, celestialObject1.color, pos1, celestialObject1.radius*zoom)

                # Vectors
                # Accel:
                pg.draw.line(screen, (0, 255, 100), pos1, list((celestialObject1.position+celestialObject1.accel*k)*zoom + offset))
                # Attraction force
                pg.draw.line(screen, (255, 0, 0), pos1, list((celestialObject1.position + attractionForceVector*k*10)*zoom + offset))
                # difference Vector
                # pg.draw.line(screen, (0, 0, 255), celestialObject1.position, [celestialObject1.position[0]+diffVector.components[0], celestialObject1.position[1]+diffVector.components[1]])

                # Angles
                # difference Vector angle
                # screen.blit(mainFont.render(str(math.degrees(diffVector.angle())), False, (0, 0, 255)), [celestialObject.position[0]+30, celestialObject.position[1]+30])
                # attraction force angle
                # screen.blit(mainFont.render(str(math.degrees(attractionForceVector.angle())), False, (255, 0, 0)), [celestialObject.position[0]+30, celestialObject.position[1]+60])
    else:
        for celestialObject in celestialObjects:
            pos1 = list(celestialObject.position*zoom+offset)
            pg.draw.circle(screen, celestialObject.color, pos1, celestialObject.radius*zoom)

            # Vectors
            # Accel:
            pg.draw.line(screen, (0, 255, 100), pos1, list((celestialObject.position+celestialObject.accel*k)*zoom + offset))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            playing = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                offset[1] += scrollSpeed
            if event.key == pg.K_DOWN:
                offset[1] -= scrollSpeed
            if event.key == pg.K_LEFT:
                offset[0] += scrollSpeed
            if event.key == pg.K_RIGHT:
                offset[0] -= scrollSpeed
            
            if event.key == pg.K_s: # Stop tracking current object
                trackingIndex = None
            
            maxInd = len(celestialObjects)-1
            if event.key == pg.K_0:
                if 0 <= maxInd:
                    trackingIndex = 0
            if event.key == pg.K_1:
                if 1 <= maxInd:
                    trackingIndex = 1
            if event.key == pg.K_2:
                if 2 <= maxInd:
                    trackingIndex = 2
            if event.key == pg.K_3:
                if 3 <= maxInd:
                    trackingIndex = 3
            
            if event.key == pg.K_SPACE:
                paused = paused == False
        
        if event.type == pg.MOUSEWHEEL:
            mousePos = Vector(pg.mouse.get_pos())
            if event.y < 0:
                zoom /= zoomSpeed
                offset = mousePos + ((offset-mousePos) / zoomSpeed)
            elif event.y > 0:
                zoom *= zoomSpeed
                offset = mousePos + ((offset-mousePos) * zoomSpeed)
