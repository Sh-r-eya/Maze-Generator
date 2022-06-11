# Import modules 
import random, csv, pygame as py
py.init()

def trialfunc(step):
    '''Maze Generator'''
    def pywindow(color):
        py.display.set_caption('LOADING')
        Icon = py.image.load('Pictures/pic.png')
        py.display.set_icon(Icon)
        window = py.display.set_mode((scnx, scny))
        window.fill(color)
        return window

    # Check if user wants to Quit Game 
    def Escape():
        if Event.type == py.QUIT:
            return False, True, True
        elif Event.type == py.KEYDOWN:
            if Event.key == py.K_ESCAPE:
                return False, True, True
            else:
                return True, False, False
        else:
            return True, False, False

    # Some Variables
    scnx=1080
    scny=720
    Quit=False
    colour=(255,255,255)
    wdt=3
    black=(0,0,0)
    window=pywindow(black)

    #required lists and dictionaries
    openlocs=[]
    corners=(scnx,scny,0)
    turndict={'up':'down','down':'up','left':'right','right':'left'}
    danger=[] #list of occupied points

    #creating the 2D list of coordinates
    # how to draw a line(surface, color, start_pos, end_pos, width)
    coordinates = []

    for y in range(step,scny,step):
        l=[]
        for x in range(step,scnx,step):
            m = []
            m.append((x,y))
            m.append(0)
            l.append(m)
        coordinates.append(l)
        
    #so that the edges of the box are closed
    for i in coordinates[0]: i[1]=1
    for i in coordinates[len(coordinates)-1]: i[1]=1
    for i in coordinates: i[len(i)-1][1]=1
    for i in coordinates: i[0][1]=1
    for i in coordinates:
        for j in i:
            if j[1]==0:
                openlocs.append(j)

    #drawing the outside box
    cornerpts = [(step,step),(scnx-step,step),(scnx-step,scny-step),(step,scny-step)]
    for i in range(4):
        py.draw.polygon(window,colour,cornerpts, width=wdt)
        
    #randomizing the start and end points
    alist=[1,2]
    q=random.choice(alist)

    #start opening
    if q==1: py.draw.line(window,black,(step,step),(step,2*step),wdt)
    else: py.draw.line(window,black,(step,step),(2*step,step),wdt)

    #end opening
    if q==1: py.draw.line(window,black,(scnx-step,scny-step),(scnx-step,scny-(2*step)),wdt)
    else: py.draw.line(window,black,(scnx-step,scny-step),(scnx-(2*step),scny-step),wdt)

    # game loop begins here
    created=False
    saved=False
    save=[]
    running = True
              
    while len(openlocs):
        turns=['up','down','left','right']   
        moves=[]
        point=random.choice(openlocs)
        x=int(point[0][0])
        y=int(point[0][1])
        openlocs.remove(point)
        maindir=random.choice(turns)
        if maindir =='up' or maindir=='down': mainlimit =(len(coordinates)-1)
        else: mainlimit=len(coordinates[0])-1
                   
        #py.draw.circle(window,(200,0,200),(x,y),4)
        for ii in range(0,len(coordinates)): 
            for jj in range(0,len(coordinates[1])):
                if coordinates[ii][jj]==point:
                    exactloc=[ii,jj]
                   
        danger.append(point)
        if point in openlocs: openlocs.remove(point)
                
        ultadir=turndict[maindir]
        possibleturns=turns
        possibleturns.remove(ultadir)
        most=3
        if mainlimit<3: most=mainlimit
        a=random.choice(possibleturns)
        for i in range(random.randint(1,most)):
            moves.append(a)
        possibleturns.remove(maindir)
                    
        for i in moves:
            if i==maindir:
                mainlimit-=1
        while mainlimit!=0:
            if most>mainlimit:
                most=mainlimit
            if moves[len(moves)-1]==maindir:
                a=random.choice(possibleturns)
                t1,t2=0,0
                for i in moves:
                    if i==possibleturns[0]: t1+=1
                    if i==possibleturns[1]: t2+=1
                if t1-t2>2: a=possibleturns[1]
                if t2-t1>2: a=possibleturns[0]
                
                for i in range(random.randint(1,most)):
                    moves.append(a)
            else:
                if mainlimit<5: most=mainlimit
                for i in range(random.randint(1,most)):
                    moves.append(maindir)
                    mainlimit-=1
                 
        for i in range(0,len(danger)):
            for p in coordinates:
                for q in p:
                    if danger[i]==q:
                        q[1]=1
                        danger[i]=q
                        
        checkvar=1
        for spin in range(0,len(moves)):                
            if moves[spin]=='up':
                if (checkvar and coordinates[exactloc[0]][exactloc[1]] not in danger) or not spin :
                    py.draw.line(window,colour,(x,y),(x,y-step),wdt)
                    py.display.update()
                    exactloc[0]-=1
                    if coordinates[exactloc[0]][exactloc[1]] in openlocs :
                        coordinates[exactloc[0]][exactloc[1]][1]=1
                        openlocs.remove(coordinates[exactloc[0]][exactloc[1]])
                        if y-step>0: y-=step
                    else: checkvar=0
                         
            if moves[spin]=='down':
               if (checkvar and coordinates[exactloc[0]][exactloc[1]] not in danger) or not spin:
                    py.draw.line(window,colour,(x,y),(x,y+step),wdt)
                    py.display.update()
                    exactloc[0]+=1
                    if coordinates[exactloc[0]][exactloc[1]] in openlocs :
                        coordinates[exactloc[0]][exactloc[1]][1]=1
                        openlocs.remove(coordinates[exactloc[0]][exactloc[1]])
                        if y+step<scny+1: y+=step
                    else: checkvar=0
                        
            if moves[spin]=='left':
                if checkvar and coordinates[exactloc[0]][exactloc[1]] not in danger or not spin:
                    py.draw.line(window,colour,(x,y),(x-step,y),wdt)
                    py.display.update()
                    exactloc[1]-=1
                    if coordinates[exactloc[0]][exactloc[1]] in openlocs :
                        coordinates[exactloc[0]][exactloc[1]][1]=1
                        openlocs.remove(coordinates[exactloc[0]][exactloc[1]])
                        if x-step>0: x-=step
                    else: checkvar=0
                    
            if moves[spin]=='right':
                if checkvar and coordinates[exactloc[0]][exactloc[1]] not in danger or not spin:
                    py.draw.line(window,colour,(x,y),(x+step,y),wdt)
                    py.display.update()
                    exactloc[1]+=1
                    if coordinates[exactloc[0]][exactloc[1]] in openlocs :
                        coordinates[exactloc[0]][exactloc[1]][1]=1
                        openlocs.remove(coordinates[exactloc[0]][exactloc[1]])
                        if x+step<scnx+1: x+=step
                    else: checkvar=0
                              
            removables=[]
            for i in range(0,len(openlocs)):
                if openlocs[i][1]!=0:
                    removables.append(openlocs[i])
            for i in removables:
                openlocs.remove(i)
                        
    created=True                 
    py.display.update()

    for i in coordinates:
        p=[]
        for j in i:
            right_clr=window.get_at((j[0][0]+step//2,j[0][1]))!=black
            down_clr=window.get_at((j[0][0],j[0][1]+step//2))!=black
            if right_clr: right_clr=1
            else: right_clr=0
            if down_clr: down_clr=1
            else: down_clr=0
            p.append(str(right_clr)+str(down_clr))
        save.append(p)

    py.quit()
    return save
