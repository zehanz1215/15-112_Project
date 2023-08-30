import math,random,copy,pygame
from cmu_112_graphics import *
from drawcubes25D import *

# initialize the x and y axis angle, which are the same in other files:
xAxisAngle = deg2Rad(200)
yAxisAngle = deg2Rad(340)

# Class: house:
class House(object):
    def __init__(self,length,width,height,origin=(0,0,0)):
        # in the map: polygon1 == origin
        self.l=l=length
        self.w=w=width
        self.h=h=height
        self.name='House'
        self.origin=origin
        self.floor=1
        self.floorHeight=random.randint(10,self.h)
        
        # initialize the cube with width, height and length:
        self.cube = [[0,0,0], 
                    [l,0,0],  
                    [0,w,0],  
                    [0,0,h],  
                    [l,w,0],  
                    [l,0,h],  
                    [0,w,h],  
                    [l,w,h]]
        
        # Calcualte the new coordinate and find the framework:
        for i in range(len(self.cube)):
            for j in range(len(self.cube[i])):
                self.cube[i][j] += self.origin[j]
        self.framework=self.cube
    
    # House up with more floors:
    def buildingUp(self):
        if self.floor<20:
            self.floor+=1
            self.framework[3][2]+=self.floorHeight
            self.framework[5][2]+=self.floorHeight
            self.framework[6][2]+=self.floorHeight
            self.framework[7][2]+=self.floorHeight
    
    # House down with less floors:
    def buildingDown(self):
        if self.floor>1:
            self.floor-=1
            self.framework[3][2]-=self.floorHeight
            self.framework[5][2]-=self.floorHeight
            self.framework[6][2]-=self.floorHeight
            self.framework[7][2]-=self.floorHeight
    
    # Translate coordiantes from 2.5D to 2D:
    def vec2Graphic(self):
        graphPoints = []
        for vec in self.framework:
            tx = vec[0]*math.cos(xAxisAngle) + vec[1]*(math.cos(yAxisAngle))
            ty = (vec[0]*math.sin(xAxisAngle) 
                + vec[1]*(math.sin(yAxisAngle)) + vec[2])       
            newPoint = [tx,ty]
            graphPoints.append(newPoint)
        return graphPoints
    
    def __repr__(self):
        return f'{self.name}:{self.floor}'

    def __hash__(self):
        return hash(self.name)

# Class: industryL
class Industry(object):
    def __init__(self,length,width,height,origin=(0,0,0)):
        # in the map: polygon1 == origin
        self.l=l=length
        self.w=w=width
        self.h=h=height
        self.name='Industry'
        self.origin=origin
        self.floor=1
        self.floorHeight=random.randint(10,self.h)
        self.chimneyHeight=30
        self.pollutionType=random.randint(1, 3)

        # initialize the cube with width, height and length:
        self.cube = [[0,0,0], 
                    [l,0,0],  
                    [0,w,0],  
                    [0,0,h],  
                    [l,w,0],  
                    [l,0,h],  
                    [0,w,h],  
                    [l,w,h]]
        
        # initialize the chimney on the roof of the industry building:
        self.chimney = [[l/2,w/2,h],
                       [5*l/8,w/2,h],  
                       [l/2,5*w/8,h],  
                       [l/2,w/2,h+self.chimneyHeight],  
                       [5*l/8,5*w/8,h],  
                       [5*l/8,w/2,h+self.chimneyHeight],  
                       [l/2,5*w/8,h+self.chimneyHeight],  
                       [5*l/8,5*w/8,h+self.chimneyHeight]]
        
        # Calcualte the new coordinate and find the framework:
        for i in range(len(self.cube)):
            for j in range(len(self.cube[i])):
                self.cube[i][j] += self.origin[j]
                self.chimney[i][j] += self.origin[j]
        
        self.framework=self.cube
        for row in self.chimney:
            self.framework.append(row)

    # Industry up with more floors:
    def buildingUp(self):
        if self.floor<5:
            self.floor+=1
            self.framework[3][2]+=self.floorHeight
            self.framework[5][2]+=self.floorHeight
            self.framework[6][2]+=self.floorHeight
            self.framework[7][2]+=self.floorHeight
            for i in range(8,16):
                self.framework[i][2]+=self.floorHeight
    
    # Industry down with less floors:
    def buildingDown(self):
        if self.floor>1:
            self.floor-=1
            self.framework[3][2]-=self.floorHeight
            self.framework[5][2]-=self.floorHeight
            self.framework[6][2]-=self.floorHeight
            self.framework[7][2]-=self.floorHeight
            for i in range(8,16):
                self.framework[i][2]-=self.floorHeight
    
    # Translate coordiantes from 2.5D to 2D:
    def vec2Graphic(self):
        graphPoints = []
        for vec in self.framework:
            tx = vec[0]*math.cos(xAxisAngle) + vec[1]*(math.cos(yAxisAngle))
            ty = (vec[0]*math.sin(xAxisAngle) 
                + vec[1]*(math.sin(yAxisAngle)) + vec[2])
            newPoint = [tx,ty]
            graphPoints.append(newPoint)
        return graphPoints
    
    def __repr__(self):
        return f'{self.name}:{self.floor}'

    def __hash__(self):
        return hash(self.name)

# Class: public infrastructures:
class Public(object):
    def __init__(self,length,width,height,origin=(0,0,0)):
        # in the map: polygon1 == origin
        self.l=l=length
        self.w=w=width
        self.h=h=height
        self.name='Public'
        self.origin=origin
        self.fenceHeight=10

        # initialize the cube with width, height and length:
        self.cube = [[0,0,0], 
                    [l,0,0],  
                    [0,w,0],  
                    [0,0,h],  
                    [l,w,0],  
                    [l,0,h],  
                    [0,w,h],  
                    [l,w,h]]
        
        # initialize the fence on the roof of the public building:
        self.fence = [[l/8,w/8,h],
                       [7*l/8,w/8,h],  
                       [l/8,7*w/8,h],  
                       [l/8,w/8,h+self.fenceHeight],  
                       [7*l/8,7*w/8,h],  
                       [7*l/8,w/8,h+self.fenceHeight],  
                       [l/8,7*w/8,h+self.fenceHeight],  
                       [7*l/8,7*w/8,h+self.fenceHeight]]

        # Calcualte the new coordinate and find the framework:
        for i in range(len(self.cube)):
                for j in range(len(self.cube[i])):
                    self.cube[i][j] += self.origin[j]
                    self.fence[i][j] += self.origin[j]
        
        self.framework=self.cube
        for row in self.fence:
            self.framework.append(row)
    
    # Translate coordiantes from 2.5D to 2D:
    def vec2Graphic(self):
        graphPoints = []
        for vec in self.framework:
            tx = vec[0]*math.cos(xAxisAngle) + vec[1]*(math.cos(yAxisAngle))
            ty = (vec[0]*math.sin(xAxisAngle) 
                + vec[1]*(math.sin(yAxisAngle)) + vec[2])
            newPoint = [tx,ty]
            graphPoints.append(newPoint)
        return graphPoints

    def __repr__(self):
        return f'{self.name}'

    def __hash__(self):
        return hash(self.name)

# Class: road:
class Road(object):
    def __init__(self,length,width,origin=(0,0,0)):
        # in the map: polygon1 == origin
        self.l=l=length
        self.w=w=width
        self.h=h=5
        self.name='Road'
        self.origin=origin
        self.direction=1

        # initialize the cube with width, height and length:
        self.cube = [[0,0,0], 
                    [l,0,0],  
                    [0,w,0],  
                    [0,0,h],  
                    [l,w,0],  
                    [l,0,h],  
                    [0,w,h],  
                    [l,w,h]]
        
        # initialize the white logo on the road:
        self.whiteLogo = [[l/8,3*w/8,h],   
                          [7*l/8,3*w/8,h],  
                          [l/8,5*w/8,h],  
                          [7*l/8,5*w/8,h]]
        
        # Calcualte the new coordinate and find the framework:
        for i in range(len(self.cube)):
                for j in range(len(self.cube[i])):
                    self.cube[i][j] += self.origin[j]
        for i in range(len(self.whiteLogo)):
                for j in range(len(self.whiteLogo[i])):
                    self.whiteLogo[i][j] += self.origin[j]
        
        self.framework=self.cube
        for row in self.whiteLogo:
            self.framework.append(row)

    # Change the direction of the road and the white logo on it:
    def changeDirection(self):
        l,w,h=self.l,self.w,self.h
        if self.direction==1:
            self.direction=0
            self.whiteLogo = [[3*l/8,w/8,h],   
                              [3*l/8,7*w/8,h],  
                              [5*l/8,w/8,h],  
                              [5*l/8,7*w/8,h]]
            for i in range(len(self.whiteLogo)):
                for j in range(len(self.whiteLogo[i])):
                    self.whiteLogo[i][j] += self.origin[j]
            self.framework=self.framework[:-4]
            for row in self.whiteLogo:
                self.framework.append(row)
        elif self.direction==0:
            self.direction=1
            self.whiteLogo = [[l/8,3*w/8,h],   
                             [7*l/8,3*w/8,h],  
                             [l/8,5*w/8,h],  
                              [7*l/8,5*w/8,h]]
            for i in range(len(self.whiteLogo)):
                for j in range(len(self.whiteLogo[i])):
                    self.whiteLogo[i][j] += self.origin[j]
            self.framework=self.framework[:-4]
            for row in self.whiteLogo:
                self.framework.append(row)

    # Translate coordiantes from 2.5D to 2D:
    def vec2Graphic(self):
        graphPoints = []
        for vec in self.framework:
            tx = vec[0]*math.cos(xAxisAngle) + vec[1]*(math.cos(yAxisAngle))
            ty = (vec[0]*math.sin(xAxisAngle) 
                + vec[1]*(math.sin(yAxisAngle)) + vec[2])
            newPoint = [tx,ty]
            graphPoints.append(newPoint)
        return graphPoints
        
    def __repr__(self):
        return f'{self.name}:{self.direction}'

    def __hash__(self):
        return hash(self.name)

# Class: water:
class Water(object):
    def __init__(self,length,width,origin=(0,0,0)):
        # in the map: polygon1 == origin
        self.l=l=length
        self.w=w=width
        self.name='Water'
        self.origin=origin
        self.absorb=random.randint(1,4)

        # initialize the cube with width, height and length:
        self.cube = [[0,0,0], 
                    [l,0,0],  
                    [0,w,0],    
                    [l,w,0]]

        # Calcualte the new coordinate and find the framework:
        for i in range(len(self.cube)):
                for j in range(len(self.cube[i])):
                    self.cube[i][j] += self.origin[j]

        self.framework=self.cube

    # Translate coordiantes from 2.5D to 2D:
    def vec2Graphic(self):
        graphPoints = []
        for vec in self.framework:
            tx = vec[0]*math.cos(xAxisAngle) + vec[1]*(math.cos(yAxisAngle))
            ty = (vec[0]*math.sin(xAxisAngle) 
                + vec[1]*(math.sin(yAxisAngle)) + vec[2])
            newPoint = [tx,ty]
            graphPoints.append(newPoint)
        return graphPoints
        
    def __repr__(self):
        return f'{self.name}'

    def __hash__(self):
        return hash(self.name)

# Class: green land:
class GreenLand(object):
    def __init__(self,length,width,height,origin=(0,0,0)):
        # in the map: polygon1 == origin
        self.l=l=length
        self.w=w=width
        self.h=h=height
        self.name='GreenLand'
        self.origin=origin
        self.absorb=random.randint(1,4)

        # initialize the cube with width, height and length:
        self.cube = [[0,0,0], 
                    [l,0,0],  
                    [0,w,0],  
                    [0,0,h],  
                    [l,w,0],  
                    [l,0,h],  
                    [0,w,h],  
                    [l,w,h]]

        # Calcualte the new coordinate and find the framework:
        for i in range(len(self.cube)):
            for j in range(len(self.cube[i])):
                 self.cube[i][j] += self.origin[j]

        self.framework=self.cube

    # Translate coordiantes from 2.5D to 2D:
    def vec2Graphic(self):
        graphPoints = []
        for vec in self.framework:
            tx = vec[0]*math.cos(xAxisAngle) + vec[1]*(math.cos(yAxisAngle))
            ty = (vec[0]*math.sin(xAxisAngle) 
                + vec[1]*(math.sin(yAxisAngle)) + vec[2])
            newPoint = [tx,ty]
            graphPoints.append(newPoint)
        return graphPoints

    def __repr__(self):
        return f'{self.name}'

    def __hash__(self):
        return hash(self.name)

# Class:music:
# From: 112 courese note:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#playingSoundsWithPygame
class Sound(object):
    def __init__(self, path):
        self.path = path
        self.loops = 1
        pygame.mixer.music.load(path)

    # Returns True if the sound is currently playing
    def isPlaying(self):
        return bool(pygame.mixer.music.get_busy())

    # Loops = number of times to loop the sound.
    # If loops = 1 or 1, play it once.
    # If loops > 1, play it loops + 1 times.
    # If loops = -1, loop forever.
    def start(self, loops=1):
        self.loops = loops
        pygame.mixer.music.play(loops=loops)

    # Stops the current sound from playing
    def stop(self):
        pygame.mixer.music.stop()