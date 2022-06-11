def playmaze(uname):
    # Initialise some variables
    import pygame as py, csv, pickle
    py.init()
    savename='save.csv'
    fetchedSave=[]
    scnx=1080; scny=720
    Quit=False # Check if user quit
    from datetime import datetime 

    # colours
    green = (200, 200, 255)
    blue=(150,145,220)
    white=(255,255,255)
    background = (0,0,0)
    colour=white
    usr=(105,200,200)
    orange = (0,0,0)
    
    # fonts    
    font1 = py.font.Font('Fonts/Font1.ttf', 75)
    font2 = py.font.Font('Fonts/Font2.ttf', 63)
    font3 = py.font.Font('Fonts/Font3.ttf', 60)
    font4 = py.font.Font('Fonts/Font2.ttf', 24)
    
    # Open new window with py
    def pywindow(color):
        py.display.set_caption('Maze Generator')
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

    def fetchSave():   
        #savename=input('enter a name for this save')     
        with open(savename,'r') as csvfile:
            csvreader=csv.reader(csvfile)
            for row in csvreader:
                fetchedSave.append(row)
            save=[]
            for i in fetchedSave:
                if i!=[]:
                    save.append(i)
        return save

    def saveMaze(save,uname):
        global savename
        savename=(uname+'_maze'+datetime.now().strftime("%d-%m-%y_%H-%M-%S")+'.csv')
        with open(savename,'w', newline='') as csvfile:
            csvwriter=csv.writer(csvfile)
            csvwriter.writerows(save)
        return

    def best(uname,lev,t):
        file=open('UserInfo.dat','rb')
        L=[]
        while True:
            try:
                d=pickle.load(file)
                if d[0]==uname:
                    HS= d[2][lev-1]
                    if HS==0 or HS>t:
                        HS=t
                    d[2][lev-1]=HS
                L.append(d)
            except:
                file.close()
                break
        file=open('UserInfo.dat','wb')
        for i in L:
            pickle.dump(i,file)
        file.close()
        return HS

    # to check if the main dxn is left to right or top to bottom based on where the op is
    def startpt(window):
        clr=window.get_at((step*3//2,step))
        if clr==background:
            return 1
        else:
            return 2

    save=fetchSave()
    window = pywindow(background)

    #calculating the required step 11,17,23,29
    r=len(save)
    step=scnx
    if r==11:
        step=60; lev=1
    if r==17:
        step=40; lev=2
    if r==23:
        step=30; lev=3
    if r==29:
        step=24; lev=4

    #creating the 2D list of coordinates
    corners=(scnx,scny,0)
    points = []
    for y in range(step,scny,step):
        l=[]
        for x in range(step,scnx,step):
            l.append((x,y))
        points.append(l)
    running = True

    # Making the lines
    def drawmaze():
        for i in range(0,len(points)):
            for j in range(0,len(points[i])):
                k=save[i][j]
                if k[0]=='1': py.draw.line(window, colour, points[i][j], (points[i][j][0]+step,points[i][j][1]), width=2)
                if k[1]=='1': py.draw.line(window, colour, points[i][j], (points[i][j][0],points[i][j][1]+step), width=2)        
        py.display.update()
        return

    drawmaze()
    # set starting position, ending position, and draw arrows
    # Also fix the first move
    ran=startpt(window)
    if ran==2:
        first='r'
        x1, y1 = step//2, step*3//2
        x2, y2 = scnx - (step//2), scny - (step*3//2)
        py.draw.line(window,colour,(x1-10,y1+10),(x1,y1),4)
        py.draw.line(window,colour,(x1-10,y1-10),(x1,y1),4)
        py.draw.line(window,colour,(x2-10,y2+10),(x2,y2),4)
        py.draw.line(window,colour,(x2-10,y2-10),(x2,y2),4)
    else:
        first='d'
        x1, y1 = step*3//2, step//2
        x2, y2 = scnx - (step*3//2), scny - (step//2)
        py.draw.line(window,colour,(x1-10,y1-10),(x1,y1),4)
        py.draw.line(window,colour,(x1+10,y1-10),(x1,y1),4)
        py.draw.line(window,colour,(x2-10,y2-10),(x2,y2),4)
        py.draw.line(window,colour,(x2+10,y2-10),(x2,y2),4)

    py.display.update()

    # Loop for retrying same maze
    running=True
    winner = lost = False
    # Game loop 5
    lost=False
    i=1
    t2=0
    moo=''
    draws=[]
    xdraw,ydraw=x1,y1
    keys=[py.K_w, py.K_a, py.K_DOWN, py.K_UP, py.K_RIGHT, py.K_LEFT, py.K_BACKSPACE, py.K_d, py.K_s]

    # Start timer
    start_time = py.time.get_ticks()
    while running and not Quit:
        for Event in py.event.get():
            running,Quit,b=Escape()
            if b: break
                        
            elif Event.type== py.KEYDOWN and not lost:
                t2+=2
                # Undo last move
                if Event.key == py.K_BACKSPACE and i>1:
                    if draws[i-2]=='r':
                        py.draw.line(window,background,(xdraw,ydraw),(xdraw-step,ydraw),4)
                        xdraw-=step
                    elif draws[i-2]=='l':
                        py.draw.line(window,background,(xdraw,ydraw),(xdraw+step,ydraw),4)
                        xdraw+=step
                    elif draws[i-2]=='d':
                        py.draw.line(window,background,(xdraw,ydraw),(xdraw,ydraw-step),4)
                        ydraw-=step
                    elif draws[i-2]=='u':
                        py.draw.line(window,background,(xdraw,ydraw),(xdraw,ydraw+step),4)
                        ydraw+=step
                    draws.pop()
                    i-=1
                    if(xdraw==x1 and ydraw==y1): t2 = 0
                    
                moo=''

                # Move Right
                if Event.key == py.K_RIGHT or Event.key == py.K_d:
                    clr=window.get_at((xdraw+step//2,ydraw))
                    if(clr==colour or clr==usr): lost = True
                    moo='r'
                    py.draw.line(window,usr,(xdraw,ydraw),(xdraw+step,ydraw),4)
                    xdraw+=step
                    
                # Move Left
                elif Event.key == py.K_LEFT or Event.key == py.K_a:
                    moo='l'
                    clr=window.get_at((xdraw-step//2,ydraw))
                    if(clr==colour or clr==usr): lost = True
                    py.draw.line(window,usr,(xdraw,ydraw),(xdraw-step,ydraw),4)
                    xdraw-=step
                    
                # Move Down
                elif Event.key == py.K_DOWN or Event.key == py.K_s:
                   clr=window.get_at((xdraw,ydraw+step//2))
                   if(clr==colour or clr==usr): lost = True
                   moo='d'
                   py.draw.line(window,usr,(xdraw,ydraw),(xdraw,ydraw+step),4)
                   ydraw+=step

                # Move Up
                elif Event.key == py.K_UP or Event.key == py.K_w:
                   clr=window.get_at((xdraw,ydraw-step//2))
                   if(clr==colour or clr==usr): lost = True
                   moo='u'
                   py.draw.line(window,usr,(xdraw,ydraw),(xdraw,ydraw-step),4)
                   ydraw-=step

                # common for all moves
                if(moo):
                    if t2==2 and moo!=first: lost=True
                    # for debugging print(xdraw,ydraw)
                    i+=1
                    draws.append(moo)

                # Check if user lost
                if lost:
                    lbut = font4.render(' You Lost! ', True, green, white)
                    TRec = lbut.get_rect()
                    TRec.center = (scnx//2 - 150, 15)
                    window.blit(lbut, TRec)
                        
                    lbut = font4.render('Try again', True, blue, white)
                    TRec = lbut.get_rect()
                    TRec.center = (scnx//2 + 50, 15)
                    window.blit(lbut, TRec)

                    lbut = font4.render('Done', True, blue, white)
                    DRect = lbut.get_rect()
                    DRect.center = (scnx//2 + 200, 15)
                    window.blit(lbut, DRect)
                        
                    py.display.update()
                    break

                if xdraw==x2 and ydraw==y2:
                    winner=True
                    end_time=py.time.get_ticks()
                    t = (end_time-start_time) //1000
                    running=False
                    break
        
            # If user wants to end game
            elif Event.type == py.MOUSEBUTTONDOWN:
                mousex, mousey = Event.pos
                if lost and DRect.collidepoint(mousex,mousey):
                    text='Don\'t give up!'
                    running=False
                    break

                # If user wants to try again
                elif lost and TRec.collidepoint(mousex,mousey):
                    if(step<=30):py.draw.rect(window,white,py.Rect(100, 0,700,20))
                    else: py.draw.rect(window,white,py.Rect(scnx//2 - 300, 0,700,30))
                    window.fill(background)
                    draws=[]
                    drawmaze()
                    i=1
                    t2=0
                    lost=False
                    xdraw,ydraw=x1,y1
                    break
            
        # update the scn
        py.display.update()

    # Game Loop 7
    if winner:
        window = pywindow(background)
        window.fill((255,255,255))
        text='You won!'
                    
        wpic = py.image.load("Pictures/cup.png")
        wpic = py.transform.scale(wpic,(scnx//3,scny//3))
        wrect = wpic.get_rect()
        wrect = wrect.move((2*scnx//3, scny//2))
        window.blit(wpic, wrect)

        wbut = font3.render(' Time taken: '+str(t)+'s', True, orange, white)
        Rec = wbut.get_rect()
        Rec.center = (scnx//3, (scny//4))
        window.blit(wbut, Rec)

        #uname='User1'
        # take from other prg
        wbut = font3.render(' Your Best Time: '+str(best(uname,lev,t))+'s', True, orange, white)
        Rec = wbut.get_rect()
        Rec.center = (scnx//3, (scny//2))
        window.blit(wbut, Rec)
                
        wbut = font3.render('press any key to continue', True, green, white)
        Rec = wbut.get_rect()
        Rec.center = (scnx//3, (3*scny//4))
        window.blit(wbut, Rec)

        # code for moving to next screen if any key pressed
        py.display.update()
        running=True
        while running and not Quit:
            for Event in py.event.get():
                running,Quit,b=Escape()
                if b: break
                elif Event.type== py.KEYDOWN:
                    running=False
                    break

    # Game Loop 6
    if not Quit:
        window = pywindow(background)   
        window.fill((255,255,255))
        
        lbut = font2.render(' Add to favourites ', True, orange, green)
        SRec = lbut.get_rect()
        SRec.center = (scnx//2, (scny//3)-50)
        window.blit(lbut, SRec)

        lbut = font2.render(' Don\'t save maze ', True, orange, green)
        DRec = lbut.get_rect()
        DRec.center = (scnx//2, (scny*2//3))
        window.blit(lbut, DRec)
        py.display.update()

        running=True
        while running and not Quit:
            for Event in py.event.get():
                running,Quit,b=Escape()
                if b: break
                elif Event.type == py.MOUSEBUTTONDOWN:
                    mousex, mousey = Event.pos
                    if DRec.collidepoint(mousex,mousey):
                        
                        Quit=True
                        break
                    elif SRec.collidepoint(mousex,mousey):
                        
                        Quit=True
                        saveMaze(save,uname)
                        break

                py.display.update()
    py.quit()
