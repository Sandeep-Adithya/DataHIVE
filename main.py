import os
from tkinter import *
from tkinter import ttk
from SETUP import *

def call_mainroot(splash):
    splash.destroy()
    login_main = Tk()
    Login_UI(login_main)
    
def splash_scr():
    splash=Tk()
    SplashScreen(splash)
    splash.after(6000,lambda:call_mainroot(splash))

def Setup_sch():
    Dir=os.listdir()
    files=["FILE.bin","School_details.txt","sql.bin","USER-RECORDS.csv"]
    for i in files:
        if i in Dir:
            continue
        else:
            root = Tk()
            School_Setup(root)
            mainloop()
            break
    else:
        return True


if __name__ == "__main__":
    if Setup_sch():
        print("o.k")
        from splashscreen import *
        from Login import *
        splash_scr()
        mainloop()
