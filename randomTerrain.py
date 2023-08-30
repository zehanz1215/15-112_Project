import math,random,copy
from cmu_112_graphics import *
from drawcubes25D import *

# give a number of hills which seems valid:
def checkHillNum(mapZ):
    rows,cols=len(mapZ),len(mapZ[0])
    numberOfCube=rows*cols
    if numberOfCube<=200:
        numberOfHill=1
    elif numberOfCube<=300:
        numberOfHill=2
    else:
        numberOfHill=3
    return numberOfHill

# randomly set the height of the hill:
def getRandomHillTop(mapZ,number):
    rows,cols=len(mapZ),len(mapZ[0])
    hillTop=[]
    for i in range(number):
        randomRow=random.randint(0,rows-1)
        randomCol=random.randint(0,cols-1)
        randomHeight=random.randint(100,200)
        mapZ[randomRow][randomCol]=randomHeight
        hillTop.append((randomRow,randomCol))
    return hillTop

# randomly set the decrease height for the hill, which makes different hills:
def terrainDown(row,col,mapZ,changeRange):
    dHeight=30
    rows,cols=len(mapZ),len(mapZ[0])
    height=mapZ[row][col]
    if height>=0:          
        for drow,dcol in changeRange:
            trow,tcol=row+drow,col+dcol
            if trow>=0 and trow<rows and tcol>=0 and tcol<cols:
                theight=height-dHeight
                if mapZ[trow][tcol]==0:
                    mapZ[trow][tcol]=theight
                elif 0<mapZ[trow][tcol]<theight:
                    mapZ[trow][tcol]=theight
    return mapZ

# Follow the rules above to make a 2.5D map:
def make25DTerrain(baseMap):
    rows,cols=len(baseMap),len(baseMap[0])
    mapZ=[([0] *cols) for row in range(rows)]
    num=checkHillNum(mapZ)
    hillTop=getRandomHillTop(mapZ,num)  
    changeRange=[(-1,-1),(-1,0),(-1,1),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for i in range(min(rows,cols)):
        for row,col in hillTop:
            terrainDown(row,col,mapZ,changeRange)
        hillTop=[]
        for row in range(rows):
            for col in range(cols):
                if mapZ[row][col]!=0: hillTop.append((row,col))
    return mapZ