from tkinter import *
from tkinter import ttk
import ctypes
import os
import random

width, height = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

class SplashScreen:
    
    def __init__(self,root):

        self.root=root
        self.root.geometry('440x250+'+str(int((width/2)-220))+"+"+str(int((height/2)-120)))
        self.root.configure(bg='#00264d')
        self.root.overrideredirect(True)
        self.s = ttk.Style()
        self.s.theme_use("default")
        self.s.configure("TProgressbar", foreground='#4da6ff', background='#4da6ff',troughcolor='#004080', thickness=10,borderwidth=0)

        self.logo = Canvas(root,width = 125, height = 125,highlightthickness=False)
        img = PhotoImage(file='icons\\logo.png')
        self.root.img=img
        self.logo.create_image(62,62,anchor=CENTER,image = img)
        self.logo.pack(pady=10,padx=5)

        self.t1 = Label(root,text="DATA HIVE",font=(('Segoe UI Light'), 21 ),fg='#d9d9d9',bg='#00264d')
        self.t1.pack()

        self.t2 = Label(root,text="School Manager",font=(('Segoe UI'), 15 ),fg='#d9d9d9',bg='#00264d')
        self.t2.pack()

        self.pixel = Label(root,text="Copyright "+u"\u00A9"+"2020 Pixel DATA Corporation",font=(('Segoe UI'), 8 ),fg='#d9d9d9',bg='#00264d')
        self.pixel.pack(side=BOTTOM)

        self.bar=DoubleVar()
        self.bar.set(0)
        self.i=0
        self.c=0
        self.progress = ttk.Progressbar(root, orient = HORIZONTAL,length = 440, variable=self.bar, mode = 'determinate',style="TProgressbar")
        self.progress.pack(side=BOTTOM,pady=3)
        self.Dir=os.listdir()
        self.files=["Login_authentication_St.bin","Login_authentication_Ts.bin","announcement.csv","events.csv"]
        self.update()

    def update(self):
        l2=[1,1.5,2,2.5,3]
        x = self.bar.get()
        try:
            if x<self.c:
                if self.files[self.i] in self.Dir:
                    self.i+=1
                else:
                    if self.files[self.i].endswith('.bin'):
                        with open(self.files[self.i],"wb") as file:
                            pass
                    else:
                        with open(self.files[self.i],"w") as file:
                            pass
                    self.i+=1
        except:
            pass
        self.c+=10
        self.bar.set(x+random.choice(l2))
        if self.bar.get() < 100:
            self.root.after(100,self.update)
        else:
            if "Time Table" not in self.Dir:
                os.mkdir("Time Table")
