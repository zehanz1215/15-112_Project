import math,random,copy,time,pygame
from cmu_112_graphics import *
from drawcubes25D import *
from randomTerrain import *
from featureClass import *
from someRules import *

# From lecture note: Graphics in Tkinter:
# https://www.cs.cmu.edu/~112/notes/notes-graphics.html
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

# app started, initialize the parameters:
def appStarted(app):
    app.mode='Welcome'      # mode: welcome page, help page, cbity design page
    app.pressKeyToStart=True

    app.transferMap=False   # means it is a 2d map at first
    app.margin=10
    app.textHeight=30
    app.text='Begin create your own city!'
    app.score=0.00
    initializeScoreFeature(app)
    app.time0=time.time()

    initialize2DMapSize(app)  
    isometricModeAppStarted(app)
    get2DMapLeftTopDimensions(app)

    get25DMapLeftTopDimensions(app,app.baseMap)

    app.select=None   # select different types of city features

    # bottum coordinates:
    app.botX=app.width-app.margin
    app.botY=app.height-app.margin
    app.sRightX=app.width-app.margin
    app.sLeftX=app.sRightX-372
    app.sUpY=app.margin+app.textHeight*2+420
    app.sDownY=app.sUpY+62

    # Resource: free download picture from the following URL:
    # https://www.pexels.com/photo/gray-concrete-building-exterior-with-geometric-design-3038740/
    app.welcomeImage=app.loadImage('WelcomeImage.jpg')
    # Resource: Self-made by powerpoint then screenshot:
    app.rawHelpImage=app.loadImage('help.png')
    app.helpImage=app.scaleImage(app.rawHelpImage, 1/10)
    # Resource: Self-made by powerpoint then screenshot:
    app.storyImage=app.loadImage('HelpStory.png')

    # From 112 course note:
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#playingSoundsWithPygame
    pygame.mixer.init()
    # Resource: Download from the websit (app), with copyright (already bought,
    # without business use):
    # https://music.163.com/#/song?id=29789678
    app.sound = Sound("Castle in the Sky.mp3")

# From 112 course note, stop sound:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#playingSoundsWithPygame
def appStopped(app):
    app.sound.stop()

################################################################################
############                  Welcome Mode                          ############
################################################################################
# Keypressed for welcome page:
def Welcome_keyPressed(app,event):
    app.mode='Game'

# Mousepressed for welcome page:
def Welcome_mousePressed(app,event):
    if event.x>1375 and event.x<1425 and event.y>125 and event.y<175:
        app.mode='Help'
            # Exit app:
    if (event.x>1375 and event.x<1425 and event.y>50 and event.y<100):
        os._exit(0)

# Timerfired for welcome page:
def Welcome_timerFired(app):
    keyPressTime=time.time()
    if keyPressTime-app.time0>=1:
        app.pressKeyToStart=not app.pressKeyToStart
        app.time0=time.time()

################################################################################
############                  Help Mode                             ############
################################################################################
# Mousepress for help mode:
def Help_mousePressed(app,event):
    if event.x>1375 and event.x<1425 and event.y>125 and event.y<175:
        app.mode='Welcome'
        # Exit app:
    if (event.x>1375 and event.x<1425 and event.y>50 and event.y<100):
        os._exit(0)

# Keypress for help mode:
def Help_keyPressed(app,event):
    if event.key=='Space':
        app.mode='Game'

################################################################################
############                 Game Mode                              ############
################################################################################
# initialize features for scoring:
def initializeScoreFeature(app):
    app.pollution=0.00
    app.absorb=0.00
    app.happyness=0.5
    app.people=0

# initialize the size of the 2D map:
def initialize2DMapSize(app):
    app.mapRow=random.randint(10,16)
    app.mapCol=random.randint(10,16)
    #app.mapRow=16
    #app.mapCol=16
    app.baseMap=[([None] *app.mapCol) for row in range(app.mapRow)]
    app.mapWidth=(app.width-app.margin*2)/app.mapRow
    app.mapHeight=(app.height-app.margin*2-app.textHeight*4)/app.mapCol

# mousepress functions:
def Game_mousePressed(app,event):
    # change mode:
    if (event.x>1375 and event.x<1425 and event.y>5 and event.y<55):
        app.mode='Help'

    # start and stop sound from 15112 lecture note:
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#playingSoundsWithPygame
    if (event.x>1425 and event.x<1475 and event.y>5 and event.y<55):
        if app.sound.isPlaying(): app.sound.stop()
        else: app.sound.start()

    # Exit app:
    if (event.x>1275 and event.x<1325 and event.y>5 and event.y<55):
        os._exit(0)

    # save snapshot:
    if app.transferMap:
        if (event.x>app.botX-200 and event.x<app.botX-100 and event.y<app.botY
            and event.y>app.botY-100):
            app.saveSnapshot()

    boardWidth=min(app.mapHeight,app.mapWidth)

    # Transfer map by bottum:
    if event.x>app.botX-100 and event.x<app.botX:
        if event.y>app.botY-100 and event.y<app.botY:
            app.transferMap = not app.transferMap
    
    # Transfer select by bottum:
    if (event.x>app.sLeftX and event.x<app.sLeftX+62 and event.y>app.sUpY and
        event.y<app.sUpY+62):
        app.select='House'
    elif (event.x>app.sLeftX+62 and event.x<app.sLeftX+124 and event.y>app.sUpY 
        and event.y<app.sUpY+62):
        app.select='Industry'
    elif (event.x>app.sLeftX+124 and event.x<app.sLeftX+186 and event.y>app.sUpY 
        and event.y<app.sUpY+62):
        app.select='Public'
    elif (event.x>app.sLeftX+186 and event.x<app.sLeftX+248 and event.y>app.sUpY 
        and event.y<app.sUpY+62):
        app.select='Road'
    elif (event.x>app.sLeftX+248 and event.x<app.sLeftX+310 and event.y>app.sUpY 
        and event.y<app.sUpY+62):
        app.select='Water'
    elif (event.x>app.sLeftX+310 and event.x<app.sRightX and event.y>app.sUpY 
        and event.y<app.sUpY+62):
        app.select='GreenLand'
    elif (event.x>app.sLeftX and event.x<app.sLeftX+62 and event.y>app.sUpY+72
        and event.y<app.sUpY+134):
        app.select='UpBuildings'
    elif (event.x>app.sLeftX+62 and event.x<app.sLeftX+124 and 
        event.y>app.sUpY+72 and event.y<app.sUpY+134):
        app.select='DownBuildings'
    elif (event.x>app.sLeftX+124 and event.x<app.sLeftX+186 and 
        event.y>app.sUpY+72 and event.y<app.sUpY+134):
        app.select='OtherChange'

    # Random make a house with different size:
    if app.select=='House':
        for row in range(len(app.mapXY)):
            for col in range(len(app.mapXY[row])):
                (leftX,leftY)=app.mapXY[row][col]
                rightX=leftX+boardWidth
                rightY=leftY+boardWidth
                if (event.x>=leftX and event.x<=rightX and event.y>=leftY 
                    and event.y<=rightY):
                    if app.baseMap[row][col]==None:
                        l=random.randint(20, 50)
                        w=random.randint(20, 50)
                        h=random.randint(20, 50)
                        house=House(l,w,h,app.map25DXY[row][col][4])
                        if checkBuildingConnect(app.baseMap,row,col):
                            app.baseMap[row][col]=house
                            tinyMap=buildCommunityMap(app.baseMap,row,col)
                            if checkCommunity(tinyMap):
                                app.text='Community looks great!'
                            else:
                                app.text='Too many houses, overcrowded!'
                        else: app.text='No connection, cannot adding house!'

    # randomly make an industry with different size:
    elif app.select=='Industry':
        for row in range(len(app.mapXY)):
            for col in range(len(app.mapXY[row])):
                (leftX,leftY)=app.mapXY[row][col]
                rightX=leftX+boardWidth
                rightY=leftY+boardWidth
                if (event.x>=leftX and event.x<=rightX and event.y>=leftY 
                    and event.y<=rightY):
                    if app.baseMap[row][col]==None:
                        l=random.randint(20, 50)
                        w=random.randint(20, 50)
                        h=random.randint(20, 40)
                        industry=Industry(l,w,h,app.map25DXY[row][col][4])
                        if (checkBuildingConnect(app.baseMap,row,col) and
                            not checkIndustryPollution(app.baseMap,row,col)):
                            app.baseMap[row][col]=industry
                        elif (checkBuildingConnect(app.baseMap,row,col) and
                            checkIndustryPollution(app.baseMap,row,col)):
                            app.text='Too much pollution, no industry!'
                        else: app.text='No connection, cannot adding industry!'

    # randomly make a public infrastructure with different size:                    
    elif app.select=='Public':
        for row in range(len(app.mapXY)):
            for col in range(len(app.mapXY[row])):
                (leftX,leftY)=app.mapXY[row][col]
                rightX=leftX+boardWidth
                rightY=leftY+boardWidth
                if (event.x>=leftX and event.x<=rightX and event.y>=leftY 
                    and event.y<=rightY):
                    if app.baseMap[row][col]==None:
                        l=random.randint(20, 50)
                        w=random.randint(20, 50)
                        h=random.randint(20, 50)
                        public=Public(l,w,h,app.map25DXY[row][col][4])
                        if (checkBuildingConnect(app.baseMap,row,col) and
                            checkPublicInfrastructure(app.baseMap,row,col)):
                            app.baseMap[row][col]=public
                            app.text='Great! Public infrastructure is serving!'
                        elif (checkBuildingConnect(app.baseMap,row,col) and
                            not checkPublicInfrastructure(app.baseMap,row,col)):
                            app.baseMap[row][col]=public
                            app.text='Public infrastructure is not serving...'
                        else: app.text='No connection, cannot adding public!'

    # randomly make a piece of road:    
    elif app.select=='Road':
        for row in range(len(app.mapXY)):
            for col in range(len(app.mapXY[row])):
                (leftX,leftY)=app.mapXY[row][col]
                rightX=leftX+boardWidth
                rightY=leftY+boardWidth
                if (event.x>=leftX and event.x<=rightX and event.y>=leftY 
                    and event.y<=rightY):
                    if app.baseMap[row][col]==None:
                        road=Road(50,50,app.map25DXY[row][col][4])
                        if checkRoads(app.baseMap,row,col):
                            app.baseMap[row][col]=road
                            app.text='Continue Adding...'
                        else:
                            app.text='Roads are not connected!'

    # randomly make a piece of water:
    elif app.select=='Water':
        for row in range(len(app.mapXY)):
            for col in range(len(app.mapXY[row])):
                (leftX,leftY)=app.mapXY[row][col]
                rightX=leftX+boardWidth
                rightY=leftY+boardWidth
                if (event.x>=leftX and event.x<=rightX and event.y>=leftY 
                    and event.y<=rightY):
                    if app.baseMap[row][col]==None:
                        water=Water(50,50,app.map25DXY[row][col][4])
                        app.baseMap[row][col]=water
                        app.text='Great! More water!'

    # randomly make a piece of green land with different size:           
    elif app.select=='GreenLand':
        for row in range(len(app.mapXY)):
            for col in range(len(app.mapXY[row])):
                (leftX,leftY)=app.mapXY[row][col]
                rightX=leftX+boardWidth
                rightY=leftY+boardWidth
                if (event.x>=leftX and event.x<=rightX and event.y>=leftY 
                    and event.y<=rightY):
                    if app.baseMap[row][col]==None:
                        h=random.randint(10, 50)
                        greenLand=GreenLand(50,50,h,app.map25DXY[row][col][4])
                        app.baseMap[row][col]=greenLand
                        app.text='Great! More green land!'

    # making buildings up:
    elif app.select=='UpBuildings':
        for row in range(len(app.mapXY)):
            for col in range(len(app.mapXY[row])):
                (leftX,leftY)=app.mapXY[row][col]
                rightX=leftX+boardWidth
                rightY=leftY+boardWidth
                if (event.x>=leftX and event.x<=rightX and event.y>=leftY 
                and event.y<=rightY):
                    feature=app.baseMap[row][col]
                    if (isinstance(feature,House) or 
                        isinstance(feature,Industry)):
                        feature.buildingUp()
                    if feature.floor==20:
                        app.text='Building is too high, there is a safety risk!'

    # making buildings down:
    elif app.select=='DownBuildings':
        for row in range(len(app.mapXY)):
            for col in range(len(app.mapXY[row])):
                (leftX,leftY)=app.mapXY[row][col]
                rightX=leftX+boardWidth
                rightY=leftY+boardWidth
                if (event.x>=leftX and event.x<=rightX and event.y>=leftY 
                    and event.y<=rightY):
                    feature=app.baseMap[row][col]
                    if isinstance(feature,House)or isinstance(feature,Industry):
                        feature.buildingDown()  

    # changing the direction of road:
    elif app.select=='OtherChange':
        for row in range(len(app.mapXY)):
            for col in range(len(app.mapXY[row])):
                (leftX,leftY)=app.mapXY[row][col]
                rightX=leftX+boardWidth
                rightY=leftY+boardWidth
                if (event.x>=leftX and event.x<=rightX and event.y>=leftY 
                    and event.y<=rightY):
                    feature=app.baseMap[row][col]
                    if isinstance(feature,Road):
                        feature.changeDirection()

    # delete one piece of city feature:
    elif app.select=='Delete':
        for row in range(len(app.mapXY)):
            for col in range(len(app.mapXY[row])):
                (leftX,leftY)=app.mapXY[row][col]
                rightX=leftX+boardWidth
                rightY=leftY+boardWidth
                if (event.x>=leftX and event.x<=rightX and event.y>=leftY 
                and event.y<=rightY):
                    if app.baseMap[row][col]!=None:
                        app.baseMap[row][col]=None

# keypress functions:
def Game_keyPressed(app,event):
    if event.key=='t':
        app.transferMap = not app.transferMap
        if app.select!=None:
            app.select=None
    elif event.key=='h':
        app.select='House'
    elif event.key=='i':
        app.select='Industry'
    elif event.key=='p':
        app.select='Public'
    elif event.key=='r':
        app.select='Road'
    elif event.key=='w':
        app.select='Water'
    elif event.key=='g':
        app.select='GreenLand'
    elif event.key=='Delete':
        app.select='Delete'
    elif event.key=='Up':
        app.select='UpBuildings'
    elif event.key=='Down':
        app.select='DownBuildings'
    elif event.key=='Left':
        app.select='OtherChange'
    elif event.key=='Space':
        app.select=None

def Game_timerFired(app):
    if app.mode=='Game':
        getScore(app)

        if app.text!='Begin create your own city!':
            timeforNow=time.time()
            if timeforNow-app.time0>=5:
                app.text='Continuing create your own city!'
                app.time0=time.time()

# get a score for the whole city:
def getScore(app):
    initializeScoreFeature(app)
    rows,cols=(len(app.baseMap),len(app.baseMap[0]))
    app.roadNum=countRoads(app.baseMap)
    roadConnectRate=roadConnection(app.baseMap)
    roadConnectScore=min(roadConnectRate*20,15)

    app.houseNumber=countFeature(app.baseMap,House)
    app.industryNumber=countFeature(app.baseMap,Industry)
    app.publicNumber=countFeature(app.baseMap,Public)
    app.waterNumber=countFeature(app.baseMap,Water)
    app.greenNumber=countFeature(app.baseMap,GreenLand)

    numberScore=min(((0.5*app.houseNumber+0.1*app.industryNumber
                     +0.1*app.publicNumber+0.1*app.waterNumber+
                     0.2*app.greenNumber)/(rows*cols-app.roadNum)),35)

    for row in range(len(app.baseMap)):
        for col in range(len(app.baseMap[0])):
            if isinstance(app.baseMap[row][col],House):
                feature=app.baseMap[row][col]
                floors=feature.floor
                for floor in range(floors):
                    people=-0.5*(floor**2)+10*floor
                    app.people+=people
                tinyMap=buildCommunityMap(app.baseMap,row,col)
                numOfHouse,numOfPeople=countHouse(tinyMap)
                
            pollution=calculatePollution(app.baseMap,row,col)
            app.pollution+=pollution
            if (isinstance(app.baseMap[row][col],Water) or 
                isinstance(app.baseMap[row][col],GreenLand)):
                absorb=pollutionAbsorb(app.baseMap,row,col)
                app.absorb+=absorb

    peopleScore=min((app.people/100000)*10,15)
    pollutionScore=min((app.absorb*0.5-app.pollution*0.05,15))
    app.happyness=countHappy(app.baseMap,app.happyness)
    happynessScore=min(abs(app.happyness-0.5)*20,20)
    app.score=(roadConnectScore+numberScore+peopleScore+
               pollutionScore+happynessScore)
    return app.score

# find the top left dimensions of the 2D map:
def get2DMapLeftTopDimensions(app):
    boardWidth=min(app.mapHeight,app.mapWidth)
    app.mapXY=[]
    for row in range(app.mapRow):
        rowMap=[]
        for col in range(app.mapCol):
                
                leftX=app.margin*4+boardWidth*row
                leftY=app.margin+app.textHeight*2+boardWidth*col
                rowMap.append((leftX,leftY))
        app.mapXY.append(rowMap)
    return app.mapXY

# transfer the 2D map to 2.5D map:
def get25DMapLeftTopDimensions(app,baseMap):
    baseMap=app.baseMap
    mapZ=make25DTerrain(baseMap)
    app.map25DXY=[]
    for row in range(len(mapZ)):
        map25DXYRow=[]
        for col in range(len(mapZ[row])):
            z=mapZ[row][col]
            polygon1=[50*col,50*row,0]
            polygon2=[50*(col+1),50*row,0]
            polygon3=[50*(col+1),50*(row+1),0]
            polygon4=[50*col,50*(row+1),0]
            polygon5=[50*col,50*row,z]
            polygon6=[50*(col+1),50*row,z]
            polygon7=[50*(col+1),50*(row+1),z]
            polygon8=[50*col,50*(row+1),z]
            polygon=[polygon1,polygon2,polygon3,polygon4,polygon5,
                     polygon6,polygon7,polygon8]
            map25DXYRow.append(polygon)
        app.map25DXY.append(map25DXYRow)
    return app.map25DXY

def transFeatureXY(app,vecs):
    for vec in vecs:
        vec[0]=app.width/2+vec[0]
        vec[1]=app.height/4-vec[1]
    return vecs

################################################################################
############                  Draw Function                         ############
################################################################################
# Draw the welcome page:
def Welcome_redrawAll(app,canvas):
    canvas.create_image(app.width/2,app.height/2,
                        image=ImageTk.PhotoImage(app.welcomeImage))
    r=random.randint(1,255)
    g=random.randint(1,255)
    b=random.randint(1,255)
    color=rgbString(r,g,b)
    canvas.create_text(app.width/2,app.margin+app.textHeight*5,
                       text='15-112 CITY DESIGNER',fill=color,
                       font='Helvetica 50 bold')
    if app.pressKeyToStart:
        canvas.create_text(app.width/2,app.height-200,
                        text='press any key to start',fill='black',
                        font='Helvetica 20 bold')
    canvas.create_image(1400,150,image=ImageTk.PhotoImage(app.helpImage))
    canvas.create_text(1350,150,text='HELP',fill='white',
                        font='Helvetica 10 bold')
    canvas.create_rectangle(1375,50,1425,100,fill='red',outline='white')
    canvas.create_text(1400,75,text='Exit',font='Helvetica 10')

# Draw the help page:
def Help_redrawAll(app,canvas):
    canvas.create_image(1400,150,image=ImageTk.PhotoImage(app.helpImage))
    canvas.create_image(app.width/2,app.height/2,
                        image=ImageTk.PhotoImage(app.storyImage))
    canvas.create_text(1350,150,text='BACK',fill='red',
                        font='Helvetica 10 bold')
    canvas.create_rectangle(1375,50,1425,100,fill='red',outline='white')
    canvas.create_text(1400,75,text='Exit',font='Helvetica 10')

# Draw the game:
def Game_redrawAll(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,
                            fill=rgbString(240,248,255))
    drawBottum(app,canvas)
    canvas.create_rectangle(1275,5,1325,55,fill='red',outline='white')
    canvas.create_text(1300,30,text='Exit',font='Helvetica 10')
    if not app.transferMap:
        drawScoreAndText(app,canvas)
        draw2DMap(app,canvas)
        draw2DBottum(app,canvas)
    if app.transferMap:
        drawScoreAndText25D(app,canvas)
        draw25DMap(app,canvas)

# Draw the bottum:
def drawBottum(app,canvas):
    canvas.create_rectangle(app.botX-100,app.botY-100,app.botX,app.botY,
                            fill=rgbString(176,224,230))
    canvas.create_text(app.botX-50,app.botY-50,text='Transfer Map',
                       font='Helvetica 10')
    canvas.create_image(1400,30,image=ImageTk.PhotoImage(app.helpImage))
    canvas.create_text(1350,30,text='HELP',font='Helvetica 10 bold')
    canvas.create_oval(1425,5,1475,55)
    canvas.create_polygon(1433,15,1450,30,1433,45)
    canvas.create_rectangle(1450,15,1455,45)
    canvas.create_rectangle(1460,15,1465,45)

# Draw the text in 2D map:
def drawScoreAndText(app,canvas):
    canvas.create_text(app.width/2,app.margin*2+app.textHeight/2,
                       text='112 CITY DESIGNER 2D MAP',font='Helvetica 50 bold')
    rightX=app.width-app.margin
    lX=rightX-375
    middleX=(lX+rightX)/2
    upY=app.margin+app.textHeight*2
    canvas.create_rectangle(lX,upY,rightX,upY+400,fill=rgbString(147, 197, 114))
    canvas.create_text(middleX,upY+50,text=f'Score:{round(app.score,2)}',
                       fill='red',font='Helvetica 30 bold')
    
    canvas.create_text(middleX,upY+100,text=f'Density:{app.people}',
                       font='Helvetica 25 bold')
    canvas.create_text(middleX,upY+150,text=f'Happyness:{round(app.happyness,2)}'
                       ,font='Helvetica 25 bold')
    canvas.create_text(middleX,upY+200,text=f'Pollution:{round(app.pollution,2)}'
                       ,font='Helvetica 25 bold')
    canvas.create_text(middleX,upY+300,text=f'Note:{app.text}',
                        font='Helvetica 10')

# Draw 2D map:
def draw2DMap(app,canvas):
    boardWidth=min(app.mapHeight,app.mapWidth)
    for row in range(app.mapRow):
        for col in range(app.mapCol):
            feature=app.baseMap[row][col]
            if isinstance(feature,House):
                color='yellow'
            elif isinstance(feature,Industry):
                color='brown'
            elif isinstance(feature,Public):
                color=rgbString(0,153,204)
            elif isinstance(feature,Road):
                color='gray'
            elif isinstance(feature,Water):
                color=rgbString(0,255,255)
            elif isinstance(feature,GreenLand):
                color='green'
            elif app.baseMap[row][col]==None:
                h=app.map25DXY[row][col][4][2]
                if h>=0:
                    color=rgbString(255-h,191,128)
                else: color=rgbString(176,224,230)
            drawEmptyBoard(app,canvas,row,col,color)
            if isinstance(feature,House) or isinstance(feature,Industry):
                x=app.margin*4+boardWidth*(row+0.5)
                y=app.margin+app.textHeight*2+boardWidth*(col+0.5)
                canvas.create_text(x,y,text=f'{feature.floor}')

# Draw each grid in the board:
def drawEmptyBoard(app,canvas,row,col,color):
    boardWidth=min(app.mapHeight,app.mapWidth)
    leftX=app.margin*4+boardWidth*row
    leftY=app.margin+app.textHeight*2+boardWidth*col
    canvas.create_rectangle(leftX,leftY,leftX+boardWidth,
                            leftY+boardWidth,fill=color)

# Draw bottums in 2D map:
def draw2DBottum(app,canvas):
    canvas.create_rectangle(app.sLeftX,app.sUpY,app.sLeftX+62,app.sUpY+62,
                            fill='yellow')
    canvas.create_text(app.sLeftX+31,app.sUpY+31,text='H',font='Helvetica 20')
    canvas.create_rectangle(app.sLeftX+62,app.sUpY,app.sLeftX+124,app.sUpY+62,
                            fill='brown')
    canvas.create_text(app.sLeftX+93,app.sUpY+31,text='I',font='Helvetica 20')
    canvas.create_rectangle(app.sLeftX+124,app.sUpY,app.sLeftX+186,app.sUpY+62,
                            fill=rgbString(0,153,204))
    canvas.create_text(app.sLeftX+155,app.sUpY+31,text='P',font='Helvetica 20')
    canvas.create_rectangle(app.sLeftX+186,app.sUpY,app.sLeftX+248,app.sUpY+62,
                            fill='gray')
    canvas.create_text(app.sLeftX+217,app.sUpY+31,text='R',font='Helvetica 20')
    canvas.create_rectangle(app.sLeftX+248,app.sUpY,app.sLeftX+310,app.sUpY+62,
                            fill=rgbString(0,255,255))
    canvas.create_text(app.sLeftX+279,app.sUpY+31,text='W',font='Helvetica 20')
    canvas.create_rectangle(app.sLeftX+310,app.sUpY,app.sLeftX+372,app.sUpY+62,
                            fill='green')
    canvas.create_text(app.sLeftX+341,app.sUpY+31,text='G',font='Helvetica 20')

    canvas.create_rectangle(app.sLeftX,app.sUpY+72,app.sLeftX+62,app.sUpY+134,
                            fill='black',outline='white')
    canvas.create_text(app.sLeftX+31,app.sUpY+103,text='Up',fill='white',
                       font='Helvetica 13')
    canvas.create_rectangle(app.sLeftX+62,app.sUpY+72,app.sLeftX+124,
                            app.sUpY+134,fill='black',outline='white')
    canvas.create_text(app.sLeftX+93,app.sUpY+103,text='Down',fill='white',
                       font='Helvetica 13')
    canvas.create_rectangle(app.sLeftX+124,app.sUpY+72,app.sLeftX+186,
                            app.sUpY+134,fill='black',outline='white')
    canvas.create_text(app.sLeftX+155,app.sUpY+103,text='Direct',fill='white',
                       font='Helvetica 13')
    canvas.create_text(app.sLeftX+186,app.sUpY+160,text='Press Delete to delete'
                       ,font='Helvetica 13')
    canvas.create_text(app.sLeftX+186,app.sUpY+180,
                text='Press Space to refresh selection',font='Helvetica 13')

# Draw text and score in 2.5D map:
def drawScoreAndText25D(app,canvas):
    canvas.create_text(app.width/2,app.margin*2+app.textHeight/2,
                      text='112 CITY DESIGNER 2.5D MAP',font='Helvetica 50 bold')
    lX=app.margin+100
    middleY=(app.margin*2+app.textHeight*2+app.height/4-50)/2
    canvas.create_rectangle(lX,app.margin*2+app.textHeight*2,app.width-lX,
                            app.height/4-50,fill=rgbString(147, 197, 114))
    canvas.create_text(lX+120,middleY,text=f'Score:{round(app.score,2)}',
                       font='Helvetica 25 bold')
    canvas.create_text(lX+400,middleY,text=f'Density:{app.people}',
                       font='Helvetica 25 bold')
    canvas.create_text(lX+700,middleY,text=f'Happyness:{round(app.happyness,2)}'
                       ,font='Helvetica 25 bold')
    canvas.create_text(lX+1000,middleY,
            text=f'Pollution:{round(app.pollution,2)}',font='Helvetica 25 bold')
    canvas.create_rectangle(app.botX-200,app.botY-100,app.botX-100,app.botY,
                            fill=rgbString(255,250,210))
    canvas.create_text(app.botX-150,app.botY-50,text='ScreenShot',
                       font='Helvetica 10')

# Draw the 2.5D map:
def draw25DMap(app,canvas):
    for row in range(len(app.map25DXY)):
        for col in range(len(app.map25DXY[row])):
            mapPolygon=app.map25DXY[row][col]
            p=vecs2Graph(app,mapPolygon)
            initColor=rgbString(255,191,128)
            h=mapPolygon[4][2]
            if mapPolygon[4][2]>=mapPolygon[0][2]:
                canvas.create_polygon(p[4][0],p[4][1],p[5][0],p[5][1],p[6][0], 
                        p[6][1],p[7][0],p[7][1],fill=rgbString(255-h,191,128))
                canvas.create_polygon(p[5][0],p[5][1],p[1][0],p[1][1], p[2][0], 
                        p[2][1],p[6][0],p[6][1],fill=rgbString(255-h,191,128))
                canvas.create_polygon(p[6][0],p[6][1],p[2][0],p[2][1],p[3][0], 
                        p[3][1],p[7][0],p[7][1],fill=rgbString(255-h,191,128))          
                canvas.create_line(p[1][0], p[1][1],p[2][0],p[2][1],fill='gray')
                canvas.create_line(p[2][0], p[2][1],p[3][0],p[3][1],fill='gray')
                canvas.create_line(p[1][0], p[1][1],p[5][0],p[5][1],fill='gray')
                canvas.create_line(p[2][0], p[2][1],p[6][0],p[6][1],fill='gray')
                canvas.create_line(p[3][0], p[3][1],p[7][0],p[7][1],fill='gray')
                canvas.create_line(p[4][0], p[4][1],p[5][0],p[5][1],fill='gray')
                canvas.create_line(p[5][0], p[5][1],p[6][0],p[6][1],fill='gray')
                canvas.create_line(p[6][0], p[6][1],p[7][0],p[7][1],fill='gray')
                canvas.create_line(p[7][0], p[7][1],p[4][0],p[4][1],fill='gray')
            elif mapPolygon[4][2]<mapPolygon[0][2]:
                canvas.create_polygon(p[4][0],p[4][1],p[5][0],p[5][1],p[6][0], 
                            p[6][1],p[7][0],p[7][1],fill=rgbString(176,224,230))
                canvas.create_line(p[5][0], p[5][1],p[4][0],p[4][1],fill='gray')
                canvas.create_line(p[4][0], p[4][1],p[7][0],p[7][1],fill='gray')
                canvas.create_line(p[7][0], p[7][1],p[6][0],p[6][1],fill='gray')
                canvas.create_line(p[6][0], p[6][1],p[5][0],p[5][1],fill='gray')
                canvas.create_line(p[1][0], p[1][1],p[5][0],p[5][1],fill='gray')
                canvas.create_line(p[2][0], p[2][1],p[6][0],p[6][1],fill='gray')
                canvas.create_line(p[3][0], p[3][1],p[7][0],p[7][1],fill='gray')
                canvas.create_line(p[0][0], p[0][1],p[4][0],p[4][1],fill='gray')
            
            feature=app.baseMap[row][col]
            if isinstance(feature,House):
                drawHouse(app,canvas,feature)
            elif isinstance(feature,Industry):
                drawIndustry(app,canvas,feature)
            elif isinstance(feature,Public):
                drawPublic(app,canvas,feature)
            elif isinstance(feature,Road):
                drawRoad(app,canvas,feature)
            elif isinstance(feature,Water):
                drawWater(app,canvas,feature)
            elif isinstance(feature,GreenLand):
                drawGreenLand(app,canvas,feature)
            elif feature==None: continue

# Draw houses:            
def drawHouse(app,canvas,feature):
    p=feature.vec2Graphic()
    p=transFeatureXY(app,p)
    
    canvas.create_polygon(p[1][0], p[1][1], p[4][0], p[4][1], p[7][0], 
                        p[7][1], p[5][0], p[5][1], fill='lightYellow')
    canvas.create_polygon(p[4][0], p[4][1], p[2][0], p[2][1], p[6][0], 
                        p[6][1], p[7][0], p[7][1], fill='lightYellow')
    canvas.create_polygon(p[5][0], p[5][1], p[7][0], p[7][1], p[6][0], 
                        p[6][1], p[3][0], p[3][1], fill='lightYellow')
    canvas.create_line(p[1][0],p[1][1],p[4][0],p[4][1],fill='yellow')
    canvas.create_line(p[4][0],p[4][1],p[7][0],p[7][1],fill='yellow')
    canvas.create_line(p[7][0],p[7][1],p[5][0],p[5][1],fill='yellow')
    canvas.create_line(p[5][0],p[5][1],p[1][0],p[1][1],fill='yellow')
    canvas.create_line(p[4][0],p[4][1],p[2][0],p[2][1],fill='yellow')
    canvas.create_line(p[2][0],p[2][1],p[6][0],p[6][1],fill='yellow')
    canvas.create_line(p[6][0],p[6][1],p[7][0],p[7][1],fill='yellow')
    canvas.create_line(p[6][0],p[6][1],p[3][0],p[3][1],fill='yellow')
    canvas.create_line(p[3][0],p[3][1],p[5][0],p[5][1],fill='yellow')

# Draw industries:
def drawIndustry(app,canvas,feature):
    p=feature.vec2Graphic()
    p=transFeatureXY(app,p)

    canvas.create_polygon(p[1][0], p[1][1], p[4][0], p[4][1], p[7][0], 
                        p[7][1], p[5][0], p[5][1], fill='brown')
    canvas.create_polygon(p[4][0], p[4][1], p[2][0], p[2][1], p[6][0], 
                        p[6][1], p[7][0], p[7][1], fill='brown')
    canvas.create_polygon(p[5][0], p[5][1], p[7][0], p[7][1], p[6][0], 
                        p[6][1], p[3][0], p[3][1], fill='brown')
    canvas.create_line(p[1][0],p[1][1],p[4][0],p[4][1],fill='black')
    canvas.create_line(p[4][0],p[4][1],p[7][0],p[7][1],fill='black')
    canvas.create_line(p[7][0],p[7][1],p[5][0],p[5][1],fill='black')
    canvas.create_line(p[5][0],p[5][1],p[1][0],p[1][1],fill='black')
    canvas.create_line(p[4][0],p[4][1],p[2][0],p[2][1],fill='black')
    canvas.create_line(p[2][0],p[2][1],p[6][0],p[6][1],fill='black')
    canvas.create_line(p[6][0],p[6][1],p[7][0],p[7][1],fill='black')
    canvas.create_line(p[6][0],p[6][1],p[3][0],p[3][1],fill='black')
    canvas.create_line(p[3][0],p[3][1],p[5][0],p[5][1],fill='black')
    # draw chimney
    canvas.create_polygon(p[9][0], p[9][1], p[12][0], p[12][1], p[15][0], 
                        p[15][1], p[13][0], p[13][1], fill='brown')
    canvas.create_polygon(p[12][0], p[12][1], p[10][0], p[10][1], p[14][0], 
                        p[14][1], p[15][0], p[15][1], fill='brown')
    canvas.create_polygon(p[13][0], p[13][1], p[15][0], p[15][1], p[14][0], 
                        p[14][1], p[11][0], p[11][1], fill='brown')
    canvas.create_line(p[9][0],p[9][1],p[12][0],p[12][1],fill='black')
    canvas.create_line(p[12][0],p[12][1],p[15][0],p[15][1],fill='black')
    canvas.create_line(p[15][0],p[15][1],p[13][0],p[13][1],fill='black')
    canvas.create_line(p[13][0],p[13][1],p[9][0],p[9][1],fill='black')
    canvas.create_line(p[12][0],p[12][1],p[10][0],p[10][1],fill='black')
    canvas.create_line(p[10][0],p[10][1],p[14][0],p[14][1],fill='black')
    canvas.create_line(p[14][0],p[14][1],p[15][0],p[15][1],fill='black')
    canvas.create_line(p[14][0],p[14][1],p[11][0],p[11][1],fill='black')
    canvas.create_line(p[11][0],p[11][1],p[13][0],p[13][1],fill='black')

# Draw public infrastructures:
def drawPublic(app,canvas,feature):
    p=feature.vec2Graphic()
    p=transFeatureXY(app,p)
    fillColor=rgbString(0,153,204)
    lineColor=rgbString(0,96,128)

    canvas.create_polygon(p[1][0], p[1][1], p[4][0], p[4][1], p[7][0], 
                        p[7][1], p[5][0], p[5][1], fill=fillColor)
    canvas.create_polygon(p[4][0], p[4][1], p[2][0], p[2][1], p[6][0], 
                        p[6][1], p[7][0], p[7][1], fill=fillColor)
    canvas.create_polygon(p[5][0], p[5][1], p[7][0], p[7][1], p[6][0], 
                        p[6][1], p[3][0], p[3][1], fill=fillColor)
    canvas.create_line(p[1][0],p[1][1],p[4][0],p[4][1],fill=lineColor)
    canvas.create_line(p[4][0],p[4][1],p[7][0],p[7][1],fill=lineColor)
    canvas.create_line(p[7][0],p[7][1],p[5][0],p[5][1],fill=lineColor)
    canvas.create_line(p[5][0],p[5][1],p[1][0],p[1][1],fill=lineColor)
    canvas.create_line(p[4][0],p[4][1],p[2][0],p[2][1],fill=lineColor)
    canvas.create_line(p[2][0],p[2][1],p[6][0],p[6][1],fill=lineColor)
    canvas.create_line(p[6][0],p[6][1],p[7][0],p[7][1],fill=lineColor)
    canvas.create_line(p[6][0],p[6][1],p[3][0],p[3][1],fill=lineColor)
    canvas.create_line(p[3][0],p[3][1],p[5][0],p[5][1],fill=lineColor)
    #draw fence
    canvas.create_polygon(p[9][0], p[9][1], p[8][0], p[8][1], p[11][0], 
                        p[11][1], p[13][0], p[13][1], fill=fillColor)
    canvas.create_polygon(p[8][0], p[8][1], p[10][0], p[10][1], p[14][0], 
                        p[14][1], p[11][0], p[11][1], fill=fillColor)
    canvas.create_polygon(p[9][0], p[9][1], p[12][0], p[12][1], p[15][0], 
                        p[15][1], p[13][0], p[13][1], fill=fillColor)
    canvas.create_polygon(p[12][0], p[12][1], p[10][0], p[10][1], p[14][0], 
                        p[14][1], p[15][0], p[15][1], fill=fillColor)
    canvas.create_line(p[9][0],p[9][1],p[12][0],p[12][1],fill=lineColor)
    canvas.create_line(p[12][0],p[12][1],p[15][0],p[15][1],fill=lineColor)
    canvas.create_line(p[15][0],p[15][1],p[13][0],p[13][1],fill=lineColor)
    canvas.create_line(p[13][0],p[13][1],p[9][0],p[9][1],fill=lineColor)
    canvas.create_line(p[12][0],p[12][1],p[10][0],p[10][1],fill=lineColor)
    canvas.create_line(p[10][0],p[10][1],p[14][0],p[14][1],fill=lineColor)
    canvas.create_line(p[14][0],p[14][1],p[15][0],p[15][1],fill=lineColor)
    canvas.create_line(p[14][0],p[14][1],p[11][0],p[11][1],fill=lineColor)
    canvas.create_line(p[11][0],p[11][1],p[13][0],p[13][1],fill=lineColor)       

# Draw roads:
def drawRoad(app,canvas,feature):
    p=feature.vec2Graphic()
    p=transFeatureXY(app,p)

    canvas.create_polygon(p[1][0], p[1][1], p[4][0], p[4][1], p[7][0], 
                        p[7][1], p[5][0], p[5][1], fill='gray')
    canvas.create_polygon(p[4][0], p[4][1], p[2][0], p[2][1], p[6][0], 
                        p[6][1], p[7][0], p[7][1], fill='gray')
    canvas.create_polygon(p[5][0], p[5][1], p[7][0], p[7][1], p[6][0], 
                        p[6][1], p[3][0], p[3][1], fill='gray')
    canvas.create_line(p[1][0],p[1][1],p[4][0],p[4][1],fill='black')
    canvas.create_line(p[4][0],p[4][1],p[7][0],p[7][1],fill='black')
    canvas.create_line(p[7][0],p[7][1],p[5][0],p[5][1],fill='black')
    canvas.create_line(p[5][0],p[5][1],p[1][0],p[1][1],fill='black')
    canvas.create_line(p[4][0],p[4][1],p[2][0],p[2][1],fill='black')
    canvas.create_line(p[2][0],p[2][1],p[6][0],p[6][1],fill='black')
    canvas.create_line(p[6][0],p[6][1],p[7][0],p[7][1],fill='black')
    canvas.create_line(p[6][0],p[6][1],p[3][0],p[3][1],fill='black')
    canvas.create_line(p[3][0],p[3][1],p[5][0],p[5][1],fill='black')
    #draw white logo
    canvas.create_polygon(p[9][0], p[9][1], p[8][0], p[8][1], p[10][0], 
                        p[10][1], p[11][0], p[11][1], fill='white')

# Draw water:
def drawWater(app,canvas,feature):
    p=feature.vec2Graphic()
    p=transFeatureXY(app,p)
    color=rgbString(0,255,255)

    canvas.create_polygon(p[0][0], p[0][1], p[1][0], p[1][1], p[3][0], 
                        p[3][1], p[2][0], p[2][1], fill=color)

# Draw green lands:
def drawGreenLand(app,canvas,feature):
    p=feature.vec2Graphic()
    p=transFeatureXY(app,p)
    
    canvas.create_polygon(p[1][0], p[1][1], p[4][0], p[4][1], p[7][0], 
                        p[7][1], p[5][0], p[5][1], fill='lightGreen')
    canvas.create_polygon(p[4][0], p[4][1], p[2][0], p[2][1], p[6][0], 
                        p[6][1], p[7][0], p[7][1], fill='lightGreen')
    canvas.create_polygon(p[5][0], p[5][1], p[7][0], p[7][1], p[6][0], 
                        p[6][1], p[3][0], p[3][1], fill='lightGreen')
    canvas.create_line(p[1][0],p[1][1],p[4][0],p[4][1],fill='green')
    canvas.create_line(p[4][0],p[4][1],p[7][0],p[7][1],fill='green')
    canvas.create_line(p[7][0],p[7][1],p[5][0],p[5][1],fill='green')
    canvas.create_line(p[5][0],p[5][1],p[1][0],p[1][1],fill='green')
    canvas.create_line(p[4][0],p[4][1],p[2][0],p[2][1],fill='green')
    canvas.create_line(p[2][0],p[2][1],p[6][0],p[6][1],fill='green')
    canvas.create_line(p[6][0],p[6][1],p[7][0],p[7][1],fill='green')
    canvas.create_line(p[6][0],p[6][1],p[3][0],p[3][1],fill='green')
    canvas.create_line(p[3][0],p[3][1],p[5][0],p[5][1],fill='green')

# Let's design our own cities!!!
runApp(width=1500, height=800)