import math

class Vector: # Create dummy class with necessary class variables to have correct code highlighting/coloring in actual class definition
    def __init__(self):
        self.components = []
        self.dimensions = 0

class Vector:
    def __init__(self, *args):
        if len(args) == 1 and type(args[0]) == list: # If a list containing a list of coordinates is submitted, get the coordinates from that list.
            self.components = list(args[0])
        else:
            self.components = list(args)
        self.dimensions = len(self.components)
    
    def __repr__(self):
        return str(self.components)

    # Its assumed for r to be a Vector class too to have correct code highlighting/coloring, a case for "type(r) == int" is defined though
    def __add__(self, r : Vector):
        result = None
        if type(r) == int or type(r) == float:
            result = Vector([self.components[i]+r for i in range(self.dimensions)])
        elif type(r) == Vector:
            if self.dimensions != r.dimensions:
                raise ValueError("Vector dimensions do not match.")
            result = Vector([self.components[i]+r.components[i] for i in range(self.dimensions)])
        return result
    
    def __sub__(self, r : Vector):
        result = None
        if type(r) == int or type(r) == float:
            result = Vector([self.components[i]-r for i in range(self.dimensions)])
        elif type(r) == Vector:
            if self.dimensions != r.dimensions:
                raise ValueError("Vector dimensions do not match.")
            result = Vector([self.components[i]-r.components[i] for i in range(self.dimensions)])
        return result
    
    def __mul__(self, r : Vector):
        result = None
        if type(r) == int or type(r) == float:
            result = Vector([self.components[i]*r for i in range(self.dimensions)])
        elif type(r) == Vector:
            if self.dimensions != r.dimensions:
                raise ValueError("Vector dimensions do not match.")
            result = Vector([self.components[i]*r.components[i] for i in range(self.dimensions)])
        return result
    
    def __truediv__(self, r : Vector):
        result = None
        if type(r) == int or type(r) == float:
            result = Vector([self.components[i]/r for i in range(self.dimensions)])
        elif type(r) == Vector:
            if self.dimensions != r.dimensions:
                raise ValueError("Vector dimensions do not match.")
            result = Vector([self.components[i]/r.components[i] for i in range(self.dimensions)])
        return result
    
    def magnitude(self):
        res = 0
        for component in self.components:
            res += component**2
        return math.sqrt(res)
    
    def angle(self):
        """Returns angle of the Vector relative to the x-axis. Repeats every 2*math.pi"""
        if self.components[0] == 0: # Avoiding ZeroDivisionError being raised
            if self.components[1] > 0:
                angle = math.pi/2 # 90°
            elif self.components[1] < 0:
                angle = math.pi * 1.5 # 360°-90° = 270°
            else:
                return None # Vector consists of (0, 0) and therefore has no angle, return "None"
        elif self.components[0] < 0:
            angle = math.pi + math.atan(self.components[1]/self.components[0])
        elif self.components[0] > 0:
            angle = (math.atan(self.components[1]/self.components[0]) + math.pi*2) % (math.pi*2)
        else:
            angle = math.atan(self.components[1]/self.components[0])
    
        return angle

    def rotate(self, angle): # "angle" is the angle by which the vector should be rotated
        originalMagnitude = self.magnitude()
        rotateAngle = (self.angle() + angle)
        self.components[0] = originalMagnitude * math.cos(rotateAngle)
        self.components[1] = originalMagnitude * math.sin(rotateAngle)
        # Following if statements correct inaccuracies with math.sin and math.cos functions only close to zero when they should be zero
        if rotateAngle == math.pi/2:
            self.components[0] = 0
        if rotateAngle == math.pi:
            self.components[1] = 0
        if rotateAngle == math.pi * 3/2:
            self.components[0] = 0
        return self


def dotProduct(v1 : Vector, v2 : Vector):
    if v1.dimensions != v2.dimensions:
        raise ValueError("Vector Dimensions do not match.")
    return sum([v1.components[i]*v2.components[i] for i in range(v1.dimensions)])
