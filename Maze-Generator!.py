'''Maze Generator'''
# fix copy maze into save
# Import modules
import random, csv, pickle, pygame as py, tkinter as tk
from tkinter import filedialog
import tkinter.messagebox
from datetime import datetime 
from trial import *
import newmazetoint as nm
py.init()

# Open new window with Pygame
def pywindow(color):
    py.display.set_caption('Maze Generator')
    Icon = py.image.load('Pictures/pic.png')
    py.display.set_icon(Icon)
    # set_mode is to set screen size
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

# exit from tkinter
def Close():
    root.withdraw()
    if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        global Quit
        Quit=True
        root.destroy()
    else:
        root.deiconify()
    return

# Initialise some variables
scnx=1080; scny=720
savename='save.csv'
fetchedSave=[]
Quit=False # Check if user quit
clock = py.time.Clock()
start_time = py.time.get_ticks() # this start time is for waiting few seconds on opening screen
changing=False # check if user is changing data
scn=str(scnx)+'x'+str(scny)
step=120

# colours
blue=(0,0,100)
green = (100, 0, 40)
black=(0,0,0)
white=(255,255,255)
background = (255,255,255)
colour=(220,20,25)
usr=(50,200,200)
orange = (0,0,0)

# fonts
font1 = py.font.Font('Fonts/Font1.ttf', 75)
font2 = py.font.Font('Fonts/Font2.ttf', 63)
font3 = py.font.Font('Fonts/Font3.ttf', 60)
font4 = py.font.Font('Fonts/Font2.ttf', 17)

# First Screen
window=pywindow(black)
bg = py.image.load("Pictures/bg.png")
bg = py.transform.scale(bg,(scnx-20,scny-20))
# resize and position image
rect = bg.get_rect()
rect = rect.move((10, 10))
window.blit(bg, rect)

# Screen1 just displays image for 2 seconds
running=True
while running and not Quit:
    for Event in py.event.get():
        running,Quit,b=Escape()
        if b: break
    # update the screen
    py.display.update()
    clock.tick(60)
    # Wait for 2 seconds
    Time = py.time.get_ticks()
    if Time - start_time>2000:
        # 2000 here = 2sec in the program
        running=False
        break    
py.quit()

def tkroot():
    # Customisation for base screen
    root=tk.Tk()
    root.title('Maze Generator')
    root.iconphoto(True, tk.PhotoImage(file='Pictures/pic.png'))
    root.configure(background='white')
    root.geometry(scn) # screen size
    root.resizable(0,0) # so that screen size is fixed
    root.bind('<Escape>', lambda e: root.destroy()) # make Esc exit the program
    root.protocol("WM_DELETE_WINDOW", Close) # runs command if user tries to close
    return root

# Open new window
def tkwindow():
    new_window=tk.Toplevel(root)
    # width(x) and height(y)
    new_window.geometry(scn)
    new_window.resizable(False, False)
    if chosen in ['reg','chp','log']:
        for i in range(2):
            buttond[i]['state']='disabled'
            buttond[i]['bg']='grey'
    return new_window

# small function for register button
def reg():
    global chosen
    chosen='reg'
    root.destroy()
    return

# small function for login button
def log():
    global chosen
    chosen='log'
    root.destroy()
    return

# small function for change button
def change():
    global chosen; chosen='chp'
    global changing; changing=True
    root.destroy()
    return

def readfile():
    # reads the binary file containing user information
    file=open('UserInfo.dat','rb')
    D=[]
    while True:
        try:
            D.append(pickle.load(file))
        except:
            file.close()
            break
    return D

def verifypw(txt):
    # methods to validate any new password
    al=['qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM','alphabet']
    S=['!@#$%^&*,.<>?;:-_=+`~1234567890 ','special character']
    for i in [al,S]:
        s=0
        for j in i[0]:
            if j in txt: s+=1
        # password must contain characters from each category
        if not s:
            tk.messagebox.showinfo("-- ERROR --", "Password must have at least 1 "+i[1])
            return False
    for i in txt:
        if (i not in al[0]) and (i not in S[0]):
            # no slash to make it easier to store as string
            tk.messagebox.showinfo("-- ERROR --", "Password must not have characters like slash or any other language ",i[1])
            return False
    return True

def submit_sc3():
    # command to submit input and password while registering
    inp_u=name_var.get()
    inp_p=passw_var.get()
    global UsrName # this will be used while deleting data
    UsrName=inp_u
    L=[inp_u,inp_p]
    ok=True # ok is to check if entered information is okay or not
    # first step is to verify password length
    if len(inp_p)<8:
        tk.messagebox.showinfo("-- ERROR --", "Password must be at least 8 characters")
        ok=False
        return
    # remaining criteria verified in the function
    if not verifypw(inp_p):
        ok=False
        return
    # read data from file
    D=readfile()
    for data in D:
        # for debugging
        #print(L,data[0:2])
        # duplicate accounts avoided
        if data[0:2]==L:
            tk.messagebox.showinfo("-- ERROR --", "Username already exists")
            ok=False
            return
    # if no errors then add the user to file
    if ok:
        file=open('UserInfo.dat','ab')
        pickle.dump([name_var.get(),passw_var.get(),[0,0,0,0]],file)
        file.close()
        tk.messagebox.showinfo("-- COMPLETE --", "Register successful")
        root.destroy()
        return

def new_login():
    # command to submit input and password to change credentials
    inp_u=name_var.get()
    inp_p=passw_var.get()
    global UsrName # this will be used while deleting data
    UsrName=inp_u
    ok=False # ok is to check if entered information is okay or not
    # first step is to verify password length
    if len(inp_p)<8:
        tk.messagebox.showinfo("-- ERROR --", "Password must be at least 8 characters")
        ok=False
        return
    # remaining criteria verified in the function
    if not verifypw(inp_p):
        ok=False
        return
    # read data from file
    D=readfile()
    file=open('UserInfo.dat','wb')
    for data in D:
        if data[0]==inp_u:
            # password edit complete
            tk.messagebox.showinfo("-- COMPLETE --", "password edit successful")
            pickle.dump([inp_u,inp_p,data[2]],file)
            ok=True
        else:
            pickle.dump(data,file)
    file.close()
    # if username not in the data in D
    if not ok:
        tk.messagebox.showinfo("-- ERROR --", "Username doesn\'t exists")
    root.destroy()
    return

# command to submit input and password to login
def try_login():
    # read data from file
    D=readfile()
    inp_p=passw_var.get()
    inp_u=name_var.get()
    global UsrName # this will be used while deleting data
    UsrName=inp_u
    okay=False # ok is to check if entered information is okay or not
    L=[inp_u,inp_p]
    # for debugging print(L)
    for data in D:
        # for debugging
        #print(data[0:2])
        if data[0:2]==L:
            tk.messagebox.showinfo("-- COMPLETE --", "Successful")
            okay=True
            root.destroy()
            return True
    # if username not in records
    if not okay:
        tk.messagebox.showinfo("-- ERROR --", "Invalid username or password")
        return False

# function to delete all data for a user
def deletu():
    if tk.messagebox.askokcancel("Confirm", "Do you want to delete all data?"):
        root.destroy()
        D=readfile()
        file=open('UserInfo.dat','wb')
        for i in D:
            # add all except this record to a list
            if i[0]!=UsrName:
                pickle.dump(i,file)
        file.close()        
    return

def fetchSave(savename):   
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

def saveMaze(save, savename='save.csv'):
    with open(savename,'w', newline='') as csvfile:
        csvwriter=csv.writer(csvfile)
        csvwriter.writerows(save)
    return

def play():
    playmaze(UsrName)
    return

# Select Level
def pick_L(variable,win):
    r = variable.get()
    r=int(r[-1])
    #print(r,type(r))
    if r==1: step=60
    if r==2: step=40
    if r==3: step=30
    if r==4: step=24
    win.destroy()
    save=nm.trialfunc(step)
    # savename=(UsrName+'_maze'+datetime.now().strftime("%d-%m-%y_%H-%M-%S")+'.csv')
    saveMaze(save)
    play()
    return

# function to select a maze from computer
def browseFiles(label,win):
    filename = tk.filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Csv files", "*.csv"),("all files","*.*")))
    ind=filename.find('Maze1.1')
    filename=filename[ind+8:]
    #print(filename)
    win.destroy()
    data=fetchSave(filename)
    saveMaze(data)
    play()
    return

# Existing saved maze
def sav_m():
    new_window=tkwindow()
    # Create a File Explorer label
    label_exp = tk.Label(new_window, text = "File Explorer:",font='Verdana 18', width = 100, height = 4, fg = "blue")	
    button_explore = tk.Button(new_window, text = "Browse Files", font='Verdana 18', 
                               command = lambda: browseFiles(label_exp,new_window))
    button_exit = tk.Button(new_window, text = "Exit", command = Close,font='Verdana 18')
    label_exp.pack()
    button_explore.pack(pady=50)
    button_exit.pack(pady=50)
    new_window.mainloop()
    return
    
# New maze
def new_m():
    new_window=tkwindow()
    variable = tk.StringVar() # variable is tkinter function for dropdown
    List = ['Level 1','Level 2', 'Level 3','Level 4']
    variable.set('Select Level')
    dropdown = tk.OptionMenu(new_window, variable, *List, command=lambda x: pick_L(variable,new_window))
    dropdown.config(width=10, height=2, bg='#58F',font='Verdana 18')
    dropdown['menu'].configure(font=('Verdana 18'))
    dropdown.pack(pady=30)
    print('running')
    new_window.mainloop()
    return

# Screen2 with 2 buttons - login and register
# another variable to control whether the next screen should open or not
while not Quit:
    if not changing:
        root=tkroot()
        buttond={}
        txtL= ['Create New User', 'Login With Username']
        cmd=[reg,log]
        chosen=None
        for i in range(2):
           buttond[i]=tk.Button(root, text=txtL[i], bg='blue', fg='black', font='Verdana 24', command = cmd[i])
           buttond[i].pack(pady=50)
        root.mainloop()
    
    # Screen3 with 2 labels - username and password
    if Quit: break
    root=tkroot()
    name_var=tk.StringVar()
    passw_var=tk.StringVar()
    #Creating the username & password entry boxes
    name_label = tk.Label(root, text = 'Username', font='Verdana 20')
    name_entry = tk.Entry(root,textvariable = name_var, font='Verdana 20')
    passw_label = tk.Label(root, text = 'Password', font = 'Verdana 20')
    passw_entry=tk.Entry(root, textvariable = passw_var, font = 'Verdana 20', show = '*')
    # different commands for the submit button depending on what the user is trying to do
    if chosen=='reg':
        sub_btn=tk.Button(root,text = 'Submit', command = submit_sc3, font='Verdana 20')
    elif chosen=='log':
        sub_btn=tk.Button(root,text = 'Submit', command = try_login, font='Verdana 20')
    elif chosen=='chp':
        sub_btn=tk.Button(root,text = 'Submit', command = new_login, font='Verdana 20')

    # pack is for arranging and aligning all elements in a screen automatically
    name_label.pack()
    name_entry.pack()
    passw_label.pack()
    passw_entry.pack()
    sub_btn.pack()
    root.mainloop()

    # Screen4 with 5 buttons - this is home screen
    if Quit: break
    root=tkroot()
    chosen='none'
    buttons={}
    txtL= ['Play maze', 'Create new maze']
    cmdL=[sav_m, new_m]    
    for i in range(2):
       buttons[i]=tk.Button(root, text=txtL[i], bg='#58F', fg='black', font='Verdana 21', command = cmdL[i], state='normal')
       buttons[i].pack(pady=30)
    but3=tk.Button(root, text='change password', bg='brown', fg='black', font='Verdana 20', command = change)
    but3.pack(pady=30)
    but4=tk.Button(root, text='delete user', bg='brown', fg='black', font='Verdana 20', command = deletu)
    but4.pack(pady=30)
    but5=tk.Button(root, text='logout', bg='red', fg='black', font='Verdana 20', command = Close)
    but5.pack(pady=30)
    root.mainloop()

'''
# It stores all the variable names defined
all_variables = dir()
for name in all_variables:
    # Print the item if it doesn't start with '__'
    if not name.startswith('__'):
        myvalue = eval(name)
        print(name, "is", type(myvalue))
'''
