from cmu_112_graphics import *
import math,copy

def appStarted(app):
    isometricModeAppStarted(app)
    app.countUp=0
    app.countLeft=0
    app.countRight=0

def keyPressed(app,event):
    isometricModeKeyPressed(app, event)

def mousePressed(app,event):
    graph=[[event.x,event.y]]
    tempOrigin=graph2Vecs1(app, graph, z=0)
    tempcube=createCube(50,50,50,tempOrigin)
    app.cubes.append(tempcube)

def redrawAll(app,canvas):
    isometricModeRedrawAll(app, canvas)

# From: Mini-Lecture: 3D-Graphic Sample Code, try to avoid using numpy, instead
# using 2D list:
def isometricModeAppStarted(app):
    # center of our 3D coordinate system
    app.origin = app.width/2, app.height/4
    # x axis is the left hand side axis
    app.xAxisAngle = deg2Rad(200)
    # y axis is the right hand side axis 
    app.yAxisAngle = deg2Rad(340)
    # z axis is simply a vertical axis 
    app.axesVecs = [[300,0,0], [0,300,0], [0,0,300]]
    app.axesPoints = vecs2Graph(app, app.axesVecs)
    app.cube = createCube(50,50,50,[0,0,0])
    app.cubes=[app.cube]

# From: Mini-Lecture: 3D-Graphic Sample Code, try to avoid using numpy, instead
# using 2D list:
# Creates a cube given a length (x), width (y), height(z), and a 3D origin point
def createCube(length, width, height, origin):
    l,w,h = length, width, height
    cube = [[0,0,0], #0
                    [l,0,0],  #1
                    [0,w,0],  #2
                    [0,0,h],  #3
                    [l,w,0],  #4
                    [l,0,h],  #5
                    [0,w,h],  #6
                    [l,w,h]] #7
    for i in range(len(cube)):
        for j in range(len(cube[i])):
            cube[i][j] += origin[j]
    return cube
# From: Mini-Lecture: 3D-Graphic Sample Code
# converts degrees to radians
def deg2Rad(deg): return deg*math.pi/180
# From: Mini-Lecture: 3D-Graphic Sample Code
# regular graph coordinate (with origin at 0,0) --> tkinter x coordinate
def g2x(x, originX): return originX+x
# From: Mini-Lecture: 3D-Graphic Sample Code
# regular graph coordinate (with origin at 0,0) --> tkinter y coordinate
def g2y(y, originY): return originY-y

# From: Mini-Lecture: 3D-Graphic Sample Code, try to avoid using numpy, instead
# using 2D list:
# calculates tkinter (x,y) equivalent of 3D vectors
def vecs2Graph(app, vecs): 
    # takes in 2d ndarray of vecs [x,y,z]
    # returns a 2d ndarray of Tkinter coordinates [x,y]
    graphPoints = []
    for vec in vecs:
        # adding the horizontal components of the vectors 
        tx = vec[0]*math.cos(app.xAxisAngle) + vec[1]*(math.cos(app.yAxisAngle))
        # adding the vertical components of the vectors 
        ty = (vec[0]*math.sin(app.xAxisAngle) 
            + vec[1]*(math.sin(app.yAxisAngle)) + vec[2])      
        # offsets, since prev tx,ty consider 0,0 to be center of the screen 
        tx = g2x(tx, app.origin[0])
        ty = g2y(ty, app.origin[1])
        newPoint = [tx,ty]
        graphPoints.append(newPoint)
    return graphPoints

# Without Numpy: change dimensions:
def graph2Vecs1(app, graph, z=0):
    ox, oy = app.origin
    (sinx,cosx,siny,cosy)=(math.sin(app.xAxisAngle),math.cos(app.xAxisAngle),
                           math.sin(app.yAxisAngle),math.cos(app.yAxisAngle))
    for point in graph:
        # first adjust points
        x = point[0] - ox #x coord in graph (centered at 0,0)
        y = oy - point[1] #y coord in graph (centered at 0,0)
        xVec = (y*cosy - x*siny) / (sinx*cosy - siny*cosx)
        yVec = (y*cosx - x*sinx) / (siny*cosx - cosy*sinx)
        vec=[xVec,yVec,z]
    return vec


def isometricModeKeyPressed(app, event):
    if event.key == 'e': # moves cube +z
        for cube in app.cubes:
            for i in range(len(cube)):
                cube[i][2]+=10
    elif event.key == 's': # moves cube -z
        for cube in app.cubes:
            for i in range(len(cube)):
                cube[i][2]-=10
    elif event.key == 'a': # moves cube +x
        for cube in app.cubes:
            for i in range(len(cube)):
                cube[i][0]+=10
    elif event.key == 'd': # moves cube -x
        for cube in app.cubes:
            for i in range(len(cube)):
                cube[i][0]-=10
    elif event.key == 'z': # moves cube -y
        for cube in app.cubes:
            for i in range(len(cube)):
                cube[i][1]-=10
    elif event.key == 'x': # moves cube +y
        for cube in app.cubes:
            for i in range(len(cube)):
                cube[i][1]+=10
    elif event.key == 'Up':
        app.countUp+=1
        upCubeList=[]
        for cube in app.cubes:
            tempPoint=copy.copy(cube[0])
            if tempPoint[2] == 50*(app.countUp-1):
                upCubeList.append(tempPoint)
        for point in upCubeList:
            newOrigin = point
            newOrigin[2]+=50
            upCube=createCube(50,50,50,newOrigin)
            app.cubes.append(upCube)
    elif event.key == 'Left':
        app.countLeft+=1
        leftCube=createCube(50,50,50,(50*app.countLeft,0,0))
        app.cubes.append(leftCube)
    elif event.key == 'Right':
        app.countRight-=1
        rightCube=createCube(50,50,50,(50*app.countRight,0,0))
        app.cubes.append(rightCube)

# From: Mini-Lecture: 3D-Graphic Sample Code:
def drawCube(app, canvas, cube, color='grey'):
    for cube in app.cubes:
        p = vecs2Graph(app, cube)
        canvas.create_line(p[0][0], p[0][1], p[1][0], p[1][1], fill=color) # 0-1
        canvas.create_line(p[0][0], p[0][1], p[2][0], p[2][1], fill=color) # 0-2
        canvas.create_line(p[0][0], p[0][1], p[3][0], p[3][1], fill=color) # 0-3

        canvas.create_polygon(p[1][0], p[1][1], p[4][0], p[4][1], p[7][0], p[7][1], p[5][0], p[5][1], fill='lightGrey')
        canvas.create_polygon(p[4][0], p[4][1], p[2][0], p[2][1], p[6][0], p[6][1], p[7][0], p[7][1], fill='lightGrey')
        canvas.create_polygon(p[5][0], p[5][1], p[7][0], p[7][1], p[6][0], p[6][1], p[3][0], p[3][1], fill='lightGrey')
        
        canvas.create_line(p[1][0], p[1][1], p[4][0], p[4][1], fill=color) # 1-4
        canvas.create_line(p[2][0], p[2][1], p[4][0], p[4][1], fill=color) # 2-4 
        canvas.create_line(p[3][0], p[3][1], p[5][0], p[5][1], fill=color) # 3-5
        canvas.create_line(p[3][0], p[3][1], p[6][0], p[6][1], fill=color) # 3-6
        canvas.create_line(p[5][0], p[5][1], p[7][0], p[7][1], fill=color) # 5-7
        canvas.create_line(p[6][0], p[6][1], p[7][0], p[7][1], fill=color) # 6-7
        canvas.create_line(p[1][0], p[1][1], p[5][0], p[5][1], fill=color) # 1-5
        canvas.create_line(p[4][0], p[4][1], p[7][0], p[7][1], fill=color) # 4-7
        canvas.create_line(p[2][0], p[2][1], p[6][0], p[6][1], fill=color) # 2-6
# From: Mini-Lecture: 3D-Graphic Sample Code:
def drawAxes(app, canvas):
    ox, oy = app.origin
    for px, py in app.axesPoints:
        canvas.create_line(ox,oy,px,py)
# From: Mini-Lecture: 3D-Graphic Sample Code:
def isometricModeRedrawAll(app, canvas):
    drawAxes(app, canvas)
    drawCube(app, canvas, app.cube)

#runApp(width=600, height=600)