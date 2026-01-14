import math
from vectors_likeablejuniper import Vector
import pygame as pg

from CelestialObject import *

pg.init()
pg.font.init()
mainFont = pg.font.SysFont("Calibri", 20)
screen = pg.display.set_mode((1200, 900))
width, height = pg.display.get_surface().get_size()
screencenter = Vector(width/2, height/2)
offset = Vector(0, 0)
scrollSpeed = 100
zoom = 1.125**(-17)
zoomSpeed = 1.125

trackingIndex = 0
k = 1000

universalGrav = 10 #6.67 * 10**(-11)


def distance(pos1, pos2):
    return math.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)


def getAttractionForce(G, m1, m2, d):
    if d == 0: # Points have 0 distance, attraction infinite
        return float("inf")
    return G*m1*m2 / d**2


def getAttractionVector(f_g, m1Pos, m2Pos) -> Vector:
    """
    Returns a Vector class object pointing in the direction of m2Pos with a magnitude of f_g
    """
    angle = Vector(m2Pos[0]-m1Pos[0], m2Pos[1]-m1Pos[1]).direction()
    
    return Vector(f_g, 0).rotate(angle)


celestialObjects : list[CelestialObject] = [CelestialObject(Vector(screencenter[0]+1000, screencenter[1]), 10, Vector(0, -1), (255, 0, 255))]
celestialObjects.append(CelestialObject(Vector(screencenter[0]-2500, screencenter[1]), 20, Vector(0, 0.5), (0, 255, 100)))
#celestialObjects.append(CelestialObject(Vector(screencenter[0]-1500, screencenter[1]), 20, Vector(0, 0), (0, 0, 100)))
sunIndex = 0
celestialObjects.insert(sunIndex, CelestialObject(Vector(screencenter), 100, Vector(0, 0), (255, 255, 0), isSun=True))

playing = True
paused = False
displayingAcceleration = True
displayingVelocity = True

while playing:
    pg.display.update()
    screen.fill((50, 50, 50))

    if not isinstance(trackingIndex, type(None)):
        print(celestialObjects[trackingIndex].position)
        print(screencenter)
        offset = -1*(celestialObjects[trackingIndex].position)*zoom + screencenter
    
    if not paused:
        for index1, celestialObject1 in enumerate(celestialObjects):
            celestialObject1.accel = 0
            pos1 = list(celestialObject1.position*zoom + offset)

            for index2, celestialObject2 in enumerate(celestialObjects):
                if index1 == index2:
                    continue
                dist = distance(celestialObject1.position, celestialObject2.position)
                
                # Calculate attraction force vector for two celestial objects
                attractionForceVector = getAttractionVector(getAttractionForce(universalGrav, celestialObject1.mass, celestialObject2.mass, dist), celestialObject1.position, celestialObject2.position)
                # Divide by mass
                attractionForceVector /= celestialObject1.mass

                celestialObject1.accel += attractionForceVector

                # Attraction force
                pg.draw.line(screen, (255, 0, 0), pos1, list((celestialObject1.position + attractionForceVector*k*1000)*zoom + offset))
                # difference Vector
                # pg.draw.line(screen, (0, 0, 255), celestialObject1.position, [celestialObject1.position[0]+diffVector.components[0], celestialObject1.position[1]+diffVector.components[1]])

                # Angles
                # difference Vector angle
                # screen.blit(mainFont.render(str(math.degrees(diffVector.angle())), False, (0, 0, 255)), [celestialObject.position[0]+30, celestialObject.position[1]+30])
                # attraction force angle
                # screen.blit(mainFont.render(str(math.degrees(attractionForceVector.angle())), False, (255, 0, 0)), [celestialObject.position[0]+30, celestialObject.position[1]+60])
            
            celestialObject1.v += celestialObject1.accel

            # Update positions by adding velocity
            celestialObject1.position += celestialObject1.v
            diffVector = celestialObject2.position - celestialObject1.position

            pos1 = list(celestialObject1.position*zoom + offset)
            pg.draw.circle(screen, celestialObject1.color, pos1, celestialObject1.radius*zoom)

            # Vectors
            # Accel:
            if displayingAcceleration:
                pg.draw.line(screen, (0, 255, 100), pos1, list((celestialObject1.position+celestialObject1.accel*k*1000)*zoom + offset))
            # Velocity
            if displayingVelocity:
                pg.draw.line(screen, (0, 20, 255), pos1, list((celestialObject1.position+celestialObject1.v*k)*zoom + offset))
    else:
        for celestialObject in celestialObjects:
            pos1 = list(celestialObject.position*zoom+offset)
            pg.draw.circle(screen, celestialObject.color, pos1, celestialObject.radius*zoom)

            # Vectors
            # Accel:
            if displayingAcceleration:
                pg.draw.line(screen, (0, 255, 100), pos1, list((celestialObject.position+celestialObject.accel*k*1000)*zoom + offset))
            
            # Velocity
            if displayingVelocity:
                pg.draw.line(screen, (0, 20, 255), pos1, list((celestialObject.position+celestialObject.v*k)*zoom + offset))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            playing = False
        if event.type == pg.KEYDOWN:
            #manually moving the camera when not tracking
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
            
            if event.key == pg.K_d:
                if any(displayingAcceleration, displayingVelocity):
                    displayingAcceleration, displayingVelocity = False
                else:
                    displayingAcceleration, displayingVelocity = True
            
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
            if event.key == pg.K_4:
                if 4 <= maxInd:
                    trackingIndex = 4
            if event.key == pg.K_5:
                if 5 <= maxInd:
                    trackingIndex = 5
            if event.key == pg.K_6:
                if 6 <= maxInd:
                    trackingIndex = 6
            if event.key == pg.K_7:
                if 7 <= maxInd:
                    trackingIndex = 7
            
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
