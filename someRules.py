import math,random,copy
from cmu_112_graphics import *
from drawcubes25D import *
from randomTerrain import *
from featureClass import *

# Count the number of roads in the map:
def countRoads(baseMap):
    countOfRoad=0
    for row in range(len(baseMap)):
        for col in range(len(baseMap[row])):
            if isinstance(baseMap[row][col],Road):
                countOfRoad+=1
    return countOfRoad

# Check if the road is connected with other roads or not:
def checkRoads(baseMap,row,col):
    countOfRoad=countRoads(baseMap)
    direction=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    rows,cols=len(baseMap),len(baseMap[0])
    if countOfRoad<1: return True
    elif countOfRoad>=1:
        for (drow,dcol) in direction:
            newRow,newCol=row+drow,col+dcol
            if (newRow>=0 and newRow<rows and newCol>=0 and newCol<cols):
                if isinstance(baseMap[newRow][newCol],Road):
                    return True
    return False

# Calculate the road connect rate for the map:
def roadConnection(baseMap):
    totalConnect=0
    realConnect=0
    rows,cols=len(baseMap),len(baseMap[0])
    for row in range(len(baseMap)):
        for col in range(len(baseMap[row])):
            if isinstance(baseMap[row][col],Road):
                totalConnect+=4
                for newRow,newCol in [(row-1,col),(row+1,col),(row,col-1),(row,col+1)]:
                    if (newRow>=0 and newRow<rows and newCol>=0 and newCol<cols
                        and (isinstance(baseMap[newRow][newCol],House) or
                        isinstance(baseMap[newRow][newCol],Industry) or
                        isinstance(baseMap[newRow][newCol],Public))):
                        realConnect+=1
    if totalConnect==0: return 0
    connectRate=realConnect/totalConnect
    return connectRate

# Count the number of houses in the given community:
def countHouse(tinyMap):
    countOfHouse=0
    countOfPeople=0
    for row in range(len(tinyMap)):
        for col in range(len(tinyMap[row])):
            if isinstance(tinyMap[row][col],House):
                countOfHouse+=1
                floors=tinyMap[row][col].floor
                for floor in range(floors):
                    people=-0.5*(floor**2)+10*floor
                    countOfPeople+=people
    return (countOfHouse,countOfPeople)

# Build a community in a map:
def buildCommunityMap(baseMap,row,col):
    tinyMap=[]
    typeOfCommunity=random.randint(1, 3)
    rows,cols=len(baseMap),len(baseMap[0])
    if isinstance(baseMap[row][col],House) or baseMap[row][col]=='B': #check
        if typeOfCommunity==1:
            r,c=3,3
        elif typeOfCommunity==2:
            r,c=5,5
        elif typeOfCommunity==3:
            r,c=7,7
        for drow in range(r):
            newRow=row+drow
            tinyMapRow=[]
            for dcol in range(c):
                newCol=col+dcol
                if (newRow>=0 and newRow<rows and newCol>=0 and newCol<cols):
                    tinyMapRow.append(baseMap[newRow][newCol])
            tinyMap.append(tinyMapRow)
    return tinyMap

# Check if the community has more houses than it can bearer:
def checkCommunity(tinyMap):
    (countOfHouse,countOfPeople)=countHouse(tinyMap)
    rows,cols=len(tinyMap),len(tinyMap[0])
    if countOfHouse>=0.75*rows*cols:
        return False
    return True

# Check if any kinds of buildings are connecnted with roads:
def checkBuildingConnect(baseMap,row,col):
    direction=[(-1,0),(0,-1),(0,1),(1,0)]
    rows,cols=len(baseMap),len(baseMap[0])
    for (drow,dcol) in direction:
        newRow,newCol=row+drow,col+dcol
        if (newRow>=0 and newRow<rows and newCol>=0 and newCol<cols and 
            isinstance(baseMap[newRow][newCol],Road)):
            return True
    return False

# Calculate the pollution made by industries:
def calculatePollution(baseMap,row,col):
    totalPollution=0
    direction=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    pollutionRange=random.randint(5, 11)
    rows,cols=len(baseMap),len(baseMap[0])
    for i in range(1,pollutionRange+1):
        for drow,dcol in direction:
            newRow,newCol=row+drow*i,col+dcol*i
            if (newRow>=0 and newRow<rows and newCol>=0 and newCol<cols and 
                isinstance(baseMap[newRow][newCol],Industry)):
                distance=math.sqrt((newRow-row)**2+(newCol-col)**2)
                pollution=baseMap[newRow][newCol].pollutionType*(math.log(distance))
                totalPollution+=pollution
    return totalPollution

# Check if the industry pollutes and impacts the houses around itself:
def checkIndustryPollution(baseMap,row,col):
    direction=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    pollutionRange=random.randint(5, 11)
    rows,cols=len(baseMap),len(baseMap[0])
    for i in range(1,pollutionRange+1):
        for drow,dcol in direction:
            newRow,newCol=row+drow*i,col+dcol*i
            if (newRow>=0 and newRow<rows and newCol>=0 and newCol<cols and 
                isinstance(baseMap[newRow][newCol],House)):
                    pollutionImpact=random.uniform(0,1)
                    if pollutionImpact>0.5:  return True
    return False

# Check if the public infrastructure impacts the house or not:
def checkPublicInfrastructure(baseMap,row,col):
    direction=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    impactRange=random.randint(3,5)
    rows,cols=len(baseMap),len(baseMap[0])
    for i in range(1,impactRange+1):
        for drow,dcol in direction:
            newRow,newCol=row+drow*i,col+dcol*i
            if (newRow>=0 and newRow<rows and newCol>=0 and newCol<cols and 
                isinstance(baseMap[newRow][newCol],House)):
                    return True
    return False

# Calculate the pollution air which has been absorbed by the public
# infrastructures near by:
def pollutionAbsorb(baseMap,row,col):
    totalAbsorb=0
    direction=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    absorbRange=random.randint(5, 11)
    rows,cols=len(baseMap),len(baseMap[0])
    for i in range(1,absorbRange+1):
        for drow,dcol in direction:
            newRow,newCol=row+drow*i,col+dcol*i
            if (newRow>=0 and newRow<rows and newCol>=0 and newCol<cols and 
                isinstance(baseMap[newRow][newCol],Industry)):
                distance=math.sqrt((newRow-row)**2+(newCol-col)**2)
                absorb=baseMap[row][col].absorb*(math.log(distance))
                totalAbsorb+=absorb
            if (newRow>=0 and newRow<rows and newCol>=0 and newCol<cols and 
                isinstance(baseMap[newRow][newCol],Industry)):
                distance=math.sqrt((newRow-row)**2+(newCol-col)**2)
                absorb=baseMap[row][col].absorb*(math.log(distance))
                totalAbsorb+=absorb
    return totalAbsorb

# Count features:
def countFeature(baseMap,feature):
    count=0
    for row in range(len(baseMap)):
        for col in range(len(baseMap[row])):
            if isinstance(baseMap[row][col],feature):
                count+=1
    return count

# Count the happyness caused by the public infrastructures:
def countHappy(baseMap,happyness):
    direction=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    rows,cols=len(baseMap),len(baseMap[0])
    for row in range(len(baseMap)):
        for col in range(len(baseMap[row])):
            if isinstance(baseMap[row][col],House):
                for drow,dcol in direction:
                    newRow,newCol=row+drow,col+dcol
                    if (newRow>=0 and newRow<rows and newCol>=0 and newCol<cols 
                    and isinstance(baseMap[newRow][newCol],Industry)):
                        happyness-=0.03
                    elif (newRow>=0 and newRow<rows and newCol>=0 and 
                    newCol<cols and isinstance(baseMap[newRow][newCol],Water)):
                        happyness+=0.05
                    elif (newRow>=0 and newRow<rows and newCol>=0 and 
                    newCol<cols and isinstance(baseMap[newRow][newCol],GreenLand)):
                        happyness+=0.06
    return happyness