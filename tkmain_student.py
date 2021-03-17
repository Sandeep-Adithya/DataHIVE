import sys
sys.path.append(sys.path[0]+"\packages")
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import time
import datetime
import os
from tkinter import messagebox
import ctypes
import mysql.connector as sql
import Login
import csv
from tkinter import scrolledtext
import pickle

width, height = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

with open("sql.bin","rb") as sql_file:
    d=pickle.load(sql_file)
    mydb = sql.connect(host="localhost",user=d["user"],passwd=d["passwd"],database="School_Manager",auth_plugin="mysql_native_password")
mycur = mydb.cursor()

no_of_students=None
no_of_teachers=None
no_of_staffs=None

def GET_USER_DETAILS() :
    with open('TEMPORARY.txt','r') as File_Open :
        return File_Open.read().split(',')  

def student_data():
    sdata=[]
    mycur.execute('SELECT * FROM lkg_ukg')
    for i in mycur.fetchall():
        i=i[0:len(i)-6]+("-","-","-")+i[len(i)-6:]
        sdata.append(i)
    mycur.execute('SELECT * FROM i_viii')
    for i in mycur.fetchall():
        i=i[0:len(i)-6]+("-",)+i[len(i)-6:]
        sdata.append(i)
    mycur.execute('SELECT * FROM ix_x')
    for i in mycur.fetchall():
        i=i[0:len(i)-6]+("-","-")+i[len(i)-6:]
        sdata.append(i)
    mycur.execute('SELECT * FROM xi_xii')
    for i in mycur.fetchall():
        i=i[0:len(i)-7]+("-","-")+i[len(i)-7:]
        sdata.append(i)
    sdata.sort()
    return sdata

def close_window():
    if messagebox.askyesno("DATAHIVE","Are you sure? Do you want to exit"):
        root.destroy()
    else:
        pass

def logout(self):
    mydb.close()
    self.root.destroy()
    Login.call_logout()

def launch_manager():
    global root
    root=Tk()
    Manager_student(root)
    root.protocol("WM_DELETE_WINDOW",close_window)

class Manager_student:

    def __init__(self,root):
        self.root = root
        self.root.geometry('1080x500+150+100')
        self.root.minsize(width=1080,height=550)
        self.root.iconbitmap('icons\\icon.ico')
        
        self.root.title("Data Hive - School Manager")

        self.s=ttk.Style()
        self.s.theme_use("vista")
        self.s.configure("TButton", relief="flat",background="#101724",foreground="white",width='0',height='30',font=('Segoe UI Light', 12),anchor=W)
        self.s.map('TButton', background=[('active','#000817')])
        self.s.configure("Line.TSeparator", background="#101724")
        
        #menu
        self.menu=Frame(root,width=40,height=550,bg="#101724")

        self.img = PhotoImage(file='icons\\logo2.png')
        self.logo=Label(self.menu,image=self.img,bg='#101724')
        self.logo.image=self.img
        self.logo.pack()

        #dashboard button
        self.dash_ico = PhotoImage(file = "icons\\dashboard.png")
        self.root.da=self.dash_ico
        self.dash=Button(self.menu,image = self.dash_ico,fg="white",bd=0,justify=LEFT,bg="#101724",activeforeground="white",activebackground="#000817",cursor="arrow",height=38,compound ='c',command=lambda: self.show_frame(dashboard),anchor="center")
        self.dash.pack(anchor="center",fill=X)

        #time table button
        self.ttable_ico = PhotoImage(file = "icons\\timetable.png") 
        self.root.ttable=self.ttable_ico
        self.ttable=Button(self.menu,image = self.ttable_ico,fg="white",bd=0,justify=RIGHT,bg="#101724",activeforeground="white",activebackground="#000817",cursor="arrow",height=38,compound ='c',command=lambda: self.show_frame(time_table),anchor="center")
        self.ttable.pack(anchor="center",fill=X)

        #report card button
        self.rcard_ico = PhotoImage(file = "icons\\report-card.png") 
        self.root.rcard=self.rcard_ico
        self.rcard=Button(self.menu,image = self.rcard_ico,fg="white",bd=0,justify=RIGHT,bg="#101724",activeforeground="white",activebackground="#000817",cursor="arrow",height=38,compound ='c',command=lambda: self.show_frame(report_card),anchor="center")
        self.rcard.pack(anchor="center",fill=X)

        #logout
        self.lout_ico = PhotoImage(file = "icons\\logout.png") 
        self.root.lt=self.lout_ico
        self.lout=Button(self.menu,image = self.lout_ico,fg="white",bd=0,justify=RIGHT,bg="#101724",activeforeground="white",activebackground="#000817",cursor="arrow",height=38,compound ='c',anchor="center",command=lambda: logout(self))
        self.lout.pack(anchor="center",fill=X,side=BOTTOM)

        #about
        self.abt_ico = PhotoImage(file = "icons\\about.png") 
        self.root.abt=self.abt_ico
        self.abt=Button(self.menu,image = self.abt_ico,fg="white",bd=0,justify=RIGHT,bg="#101724",activeforeground="white",activebackground="#000817",cursor="arrow",height=38,compound ='c',command=lambda: self.show_frame(about_software),anchor="center")
        self.abt.pack(anchor="center",fill=X,side=BOTTOM)

        self.menu.pack(side=LEFT,fill=Y)
        self.menu.pack_propagate(0)

        #topbar
        self.topbar=Frame(root,height=40,bg="#4da6ff")
        #toggle button
        self.btnpic = PhotoImage(file="icons\\menu.png")
        self.root.togg=self.btnpic
        self.toggle_btn=Button(self.topbar,image=self.btnpic,bd=0,justify=LEFT,bg="#4da6ff",activebackground="#000817",cursor="arrow",height=38,width=46,compound='left',command=self.extend_menu)
        self.toggle_btn.pack(side=LEFT)
        self.location=Label(self.topbar,text="",font=(('Segoe UI'), 14 ),fg='white',bg='#4da6ff')
        self.location.pack(side=LEFT)
        
        #username
        user_detials=GET_USER_DETAILS()
        self.user = Label(self.topbar,font=('Segoe UI',10),justify=LEFT,text=user_detials[3]+' ('+user_detials[0]+')'+'\n'+user_detials[1],bg='#4da6ff',fg="#101724")
        self.user.pack(side=RIGHT)

        ttk.Separator(self.topbar, orient='vertical',style="Line.TSeparator").pack(fill=Y,side=RIGHT,pady=3)

        #Date and Time
        self.Date_Time = Label(self.topbar,font=('Segoe UI',10),justify=LEFT,bg='#4da6ff')
        self.Date_Time.pack(side=RIGHT)
        self.clock()

        self.topbar.pack(fill=X)

        #main container
        container = Frame(self.root)
        container.pack(side=LEFT, fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages={}
        page_list=[loading,dashboard,time_table,report_card,about_software]
        for F in page_list:
            frame = F(container, self)
            self.pages[str(F)] = frame
            frame.grid(row=0, column=0,sticky=N+S+E+W)
            self.show_frame(loading)
        self.root.after(800,lambda: self.show_frame(dashboard))

    def clock(self):
        time_string = time.strftime("%H:%M:%S")
        date_string = time.strftime("%d/%m/%Y")
        self.Date_Time.config(text='Date : '+date_string+"\n"+"Time : "+time_string)
        self.Date_Time.after(200,self.clock)

    def show_frame(self, controller):
        frame = self.pages[str(controller)]
        frame_name = str(frame)[10:].replace("_"," ")
        if "loading" in frame_name:
            self.location.config(text="Loading...")
        else:
            self.location.config(text=frame_name.title())
        frame.tkraise()

    def extend_menu(self):
        if self.menu.winfo_width()>70:
            self.menu.config(width=40)
            self.dash.config(text="",compound='c',anchor="center")
            self.lout.config(text="",compound='c',anchor="center")
            self.rcard.config(text="",compound='c',anchor="center")
            self.lout.config(text="",compound='c',anchor="center")
            self.abt.config(text="",compound='c',anchor="center")
        else:
            self.menu.config(width=140)
            self.dash.config(text=" Dashboard",compound=LEFT,anchor=W)
            self.lout.config(text=" Logout",compound=LEFT,anchor=W)
            self.abt   .config(text=" About",compound=LEFT,anchor=W)
            self.ttable.config(text=" Time Table",compound=LEFT,anchor=W)
            self.rcard .config(text=" Report Card",compound=LEFT,anchor=W)

class dashboard(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.configure(background="#ecf0f5")

        # logo name address
        self.lna=Frame(self,background="#ecf0f5",width=500,height=135)
        self.schlogo=Canvas(self.lna,width = 100,height = 100,highlightthickness=True,bg="#ecf0f5")
        img = PhotoImage(file='icons/School.png')
        self.schlogo.img=img
        self.schlogo.create_image(50,50,anchor=CENTER,image = img)
        self.schlogo.pack(side=LEFT)
        self.schtext=Frame(self.lna,background="#ecf0f5")
        file = open("School_details.txt","r")
        School_details=file.readlines()
        file.close()
        words=School_details[0].split()
        r=""
        l=0
        for i in words:
            if l+len(i)>35:
                r+="\n"
                l=0
            if len(i)<35:
                l+=len(i)+1
                r+=i+" "

        Label(self.schtext, text=r,font=(('Segoe UI'), 18 ),justify=LEFT,bg="#ecf0f5").pack(anchor=W)
        Label(self.schtext, text=School_details[1][:len(School_details[1])-2],font=(('Segoe UI Light'), 9 ),justify=LEFT,bg="#ecf0f5").pack(anchor=W)
        Label(self.schtext, text=School_details[2][:len(School_details[2])-1]+" - "+School_details[3][:len(School_details[0])-2],font=(('Segoe UI Light'), 9 ),justify=LEFT,bg="#ecf0f5").pack(anchor=W)
        self.schtext.pack(side=LEFT,padx=10)
        self.lna.pack(fill=BOTH,side=TOP,anchor=W,pady=15,padx=20)
        self.frm=Frame(self)
        self.frm1=Frame(self.frm,width=300,height=150,background="#ecf0f5")
        self.Announcement = Frame(self.frm1,background="#ecf0f5")
        self.scrollbar = Scrollbar(self.Announcement)
        self.scrollbar.pack(side = RIGHT, fill = BOTH)
        self.Announcement_listbox = ttk.Treeview(self.Announcement, show="headings",yscrollcommand = self.scrollbar.set)
        self.Announcement_listbox.pack(side = LEFT, fill = BOTH,expand=True)
        self.Announcement_listbox['columns']=("Announcements")
        self.Announcement_listbox.heading("Announcements",text="Announcements")
        self.Announcement_listbox.column("Announcements",minwidth=0)
        self.scrollbar.config(command = self.Announcement_listbox.yview)
        self.Announcement.pack(fill=BOTH,pady=10,padx=10,expand=True)
        self.frm1.pack(side=LEFT,fill=BOTH,expand=True)
        self.frm2=Frame(self.frm,width=300,height=150,background="#ecf0f5")
        self.Event = Frame(self.frm2,background="#ecf0f5",width=40)
        self.scrollbar = Scrollbar(self.Event)
        self.scrollbar.pack(side = RIGHT, fill = BOTH)
        self.Event_listbox = ttk.Treeview(self.Event, show="headings",yscrollcommand = self.scrollbar.set)
        self.Event_listbox.pack(side = LEFT, fill = BOTH,expand=True)
        self.Event_listbox['columns']=("Date","Events")
        self.Event_listbox.heading("Date",text="Date")
        self.Event_listbox.column("Date",minwidth=0, width=120, stretch=NO)
        self.Event_listbox.heading("Events",text="Events")
        self.Event_listbox.column("Events",minwidth=0, stretch=YES)
        self.scrollbar.config(command = self.Event_listbox.yview)
        self.Event.pack(fill=BOTH,pady=10,padx=10,expand=True)
        self.frm2.pack(side=RIGHT,fill=BOTH,expand=True)
        self.frm.pack(side=BOTTOM,fill=BOTH,padx=10,pady=10,expand=True)

        self.update_Event()
        self.update_Announcement()

    def update_Event(self):
        try:
            self.Event_listbox.delete(*self.Event_listbox.get_children())
        except:
            pass
        try:
            event_file = open("events.csv","r")
            r=csv.reader(event_file)
            for i in r:
                if i[3]=="1":
                    self.Event_listbox.insert('','end',values=i[:1]+[i[1].replace(u'\u00AF','\n')]+i[2:])
            event_file.close()
        except:
            pass
        self.Event_listbox.after(400,self.update_Event)

    def update_Announcement(self):
        try:
            self.Announcement_listbox.delete(*self.Announcement_listbox.get_children())
        except:
            pass
        try:
            announcement_file = open("announcement.csv","r")
            r=csv.reader(announcement_file)
            for i in r:
                if i[2]=="1":
                    if i[3]=="0":
                        self.Announcement_listbox.insert('','end',values=[i[0].replace(u'\u00AF','\n')])
                    else:
                        for j in student_data():
                            if GET_USER_DETAILS()[0] == str(j[0]):
                                Class=j[4]
                                Section=j[5]
                                break
                        if i[4]==Class and i[5]==Section :
                            self.Announcement_listbox.insert('','end',values=[i[0].replace(u'\u00AF','\n')])
                    
            announcement_file.close()
        except:
            pass
        self.Announcement_listbox.after(400,self.update_Announcement)

class loading(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.configure(background="#ecf0f5")
        self.logo = Canvas(self,width = 500, height = 500,highlightthickness=False,background="#ecf0f5")
        img = PhotoImage(file="icons\\DATAHIVE-logo.png")
        self.logo.img=img
        self.logo.create_image(250,250,anchor=CENTER,image = img)
        self.logo.pack(expand=True)

class about_software(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.configure(background="#ecf0f5")
        Label(self,background="#ecf0f5",foreground="black",font=(('Segoe UI Light'), 30 ),text='A SOFTWARE BY').pack(side=TOP,pady=10)
        self.logo = Canvas(self,width = 300, height = 270,highlightthickness=False,background="#ecf0f5")
        img = PhotoImage(file="icons\\pixeldata.png")
        self.logo.img=img
        self.logo.create_image(150,150,anchor=CENTER,image = img)
        self.logo.pack(expand=True)
        Label(self,background="#ecf0f5",foreground="black",font=(('Segoe UI Light'), 11 ),text="Copyright "+u"\u00A9"+"2021 Pixel DATA Corporation").pack(side=BOTTOM,pady=3)
        Label(self,background="#ecf0f5",foreground="black",font=(('Segoe UI Light'), 9 ),text="PixelDATA and the pixel cloud symbol are registered trademarks of PixelDATA Corporation. All other trademarks remain the property of their respective owners.").pack(pady=2,side=BOTTOM)
        Button(self,text="Visit PixelDATA website",width=20,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: webbrowser.open("https://pixeldatacorporation.ml")).pack(side=BOTTOM,expand=True)
        self.dev_frm=Frame(self,background="#ecf0f5")
        Label(self.dev_frm,background="#ecf0f5",font=(('Segoe UI Light'), 20 ),text="DEVELOPERS").grid(row=0,column=0,columnspan=4)
        Label(self.dev_frm,background="#ecf0f5",font=(('Segoe UI '), 15 ),text="Sandeep Adithya K").grid(row=1,column=0,padx=35,pady=5)
        Label(self.dev_frm,background="#ecf0f5",font=(('Segoe UI '), 15 ),text="Sharvesh G").grid(row=1,column=1,pady=5)
        Label(self.dev_frm,background="#ecf0f5",font=(('Segoe UI '), 15 ),text="Thirumalai B").grid(row=1,column=2,padx=35,pady=5)
        Label(self.dev_frm,background="#ecf0f5",font=(('Segoe UI '), 15 ),text="Vishwa G").grid(row=1,column=3,pady=5)
        self.dev_frm.pack(side=BOTTOM,expand=True)
        

Entry_L=[]
Label_L=[]

class time_table(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.configure(background="#ecf0f5")
        self.row=12
        self.column=7
        self.Form_canvas=Canvas(self,background="#ecf0f5",bd=0)
        self.scroll=ttk.Scrollbar(self,orient=HORIZONTAL,command = self.Form_canvas.xview)
        self.table_frm=Frame(self.Form_canvas,bg="black",bd=0)
        self.table_frm.bind("<Configure>",lambda e: self.Form_canvas.configure(scrollregion=self.Form_canvas.bbox("all")))
        self.Form_canvas.create_window(0,0, window=self.table_frm,anchor="center")
        self.Form_canvas.update_idletasks()
        self.Form_canvas.config(xscrollcommand = self.scroll.set)

        days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        d=0
        for i in range(13):
            if i in [1,3,5,7,9,11]:
                day_lbl=Label(self.table_frm,text=days[d],bg="white",font=('Segoe UI',12,'normal'),width=11)
                day_lbl.grid(row=i,column=0,rowspan=2,pady=1,padx=2,sticky=NSEW)
                d+=1
            l=[]
            for j in range(-1,6):
                if (i==0 and j<0) or j==-1:
                    pass
                elif i==0 and j>0:
                    lbl=Label(self.table_frm,text="Period "+str(j),bg="white",font=('Segoe UI',11,'normal'))
                    lbl.grid(row=i,column=j+1,pady=1,padx=1,sticky=NSEW)
                elif i!=0:
                    if j==0:
                        if i%2!=0:
                            Label(self.table_frm,text="Subject",bg="white",font=('Segoe UI',11,'normal')).grid(row=i,column=j+1,pady=1,padx=1,sticky=NSEW)
                        else:
                            Label(self.table_frm,text="Teacher",bg="white",font=('Segoe UI',11,'normal')).grid(row=i,column=j+1,pady=1,padx=1,sticky=NSEW)
                    else:
                        e=Entry(self.table_frm)
                        e.grid(row=i,column=j+1,pady=1,padx=1,sticky=NSEW)
                        l.append(e)
            Entry_L.append(l)

        self.Form_canvas.pack(fill=BOTH,expand=True,anchor="center")
        self.scroll.pack( side = BOTTOM, fill = X )
        self.open_file()

    def open_file(self):
        global Entry_L
        try:
            for i in student_data():
                if GET_USER_DETAILS()[0] == str(i[0]):
                    self.class_section=[i[4],i[5]]
                    break
            
            timetable = open("Time Table//"+self.class_section[0]+self.class_section[1]+".csv","r",newline="")
            r = csv.reader(timetable)
            periods=next(r)
            self.column=len(periods)+2
            self.table_frm.destroy()
            self.table_frm=Frame(self.Form_canvas,bg="black",bd=0)
            self.table_frm.bind("<Configure>",lambda e: self.Form_canvas.configure(scrollregion=self.Form_canvas.bbox("all")))
            self.Form_canvas.create_window(0,0, window=self.table_frm,anchor="center")
            Entry_L=[]
            days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
            d=0
            for i in range(13):
                if i in [1,3,5,7,9,11]:
                    day_lbl=Label(self.table_frm,text=days[d],bg="white",font=('Segoe UI',12,'normal'),width=11)
                    day_lbl.grid(row=i,column=0,rowspan=2,pady=1,padx=2,sticky=NSEW)
                    d+=1
                l=[]
                for j in range(-1,len(periods)+1):
                    if (i==0 and j<0) or j==-1:
                        pass
                    elif i==0 and j>0:
                        lbl=Label(self.table_frm,text="Period "+str(j),bg="white",font=('Segoe UI',11,'normal'))
                        lbl.grid(row=i,column=j+1,pady=1,padx=1,sticky=NSEW)
                    elif i!=0:
                        if j==0:
                            if i%2!=0:
                                Label(self.table_frm,text="Subject",bg="white",font=('Segoe UI',11,'normal')).grid(row=i,column=j+1,pady=1,padx=1,sticky=NSEW)
                            else:
                                Label(self.table_frm,text="Teacher",bg="white",font=('Segoe UI',11,'normal')).grid(row=i,column=j+1,pady=1,padx=1,sticky=NSEW)
                        else:
                            e=Entry(self.table_frm)
                            e.grid(row=i,column=j+1,pady=1,padx=1,sticky=NSEW)
                            l.append(e)
                Entry_L.append(l)
            
            Entry_L.pop(0)
            for i1,i2 in zip(r,Entry_L):
                for j1,j2 in zip(i1,i2):
                    j2.insert(0,j1)
            timetable.close()
        except:
            pass
    
class report_card(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.configure(background="#ecf0f5")

        self.row=12
        self.column=5

        self.Frame1 = self

        self.Frame2 = Frame(self.Frame1,background="#ecf0f5")
        self.Frame2.pack(fill=X,anchor=N,padx=5,pady=8)

        self.ncs_frm = Frame(self.Frame2,background="#ecf0f5")
        self.ncs_frm.pack(fill=X,anchor=NW,padx=5,pady=8,side=LEFT)
        self.Name=StringVar()
        self.Class=StringVar()
        self.Section=StringVar()
        Label(self.ncs_frm,text="Name",font=(('Segoe UI'), 12 ),background="#ecf0f5").grid(row=0,column=0,sticky=W)
        Label(self.ncs_frm,text="Class",font=(('Segoe UI'), 12 ),background="#ecf0f5").grid(row=1,column=0,sticky=W)
        Label(self.ncs_frm,text="Section",font=(('Segoe UI'), 12 ),background="#ecf0f5").grid(row=2,column=0,sticky=W)
        Label(self.ncs_frm,textvariable=self.Name,font=(('Segoe UI'), 12 ),background="#ecf0f5").grid(row=0,column=1,sticky=W)
        Label(self.ncs_frm,textvariable=self.Class,font=(('Segoe UI'), 12 ),background="#ecf0f5").grid(row=1,column=1,sticky=W)
        Label(self.ncs_frm,textvariable=self.Section,font=(('Segoe UI'), 12 ),background="#ecf0f5").grid(row=2,column=1,sticky=W)
        Button(self.Frame2,text="EXPORT",font=('Segoe UI',11,'normal'),width=10,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda:self.print_file()).pack(side=RIGHT)

        self.Form_canvas=Canvas(self.Frame1,background="#ecf0f5",bd=0)
        self.scroll=ttk.Scrollbar(self.Frame1,command = self.Form_canvas.yview)
        self.table_frm=Frame(self.Form_canvas,bg="black",bd=0)
        self.table_frm.bind("<Configure>",lambda e: self.Form_canvas.configure(scrollregion=self.Form_canvas.bbox("all")))
        self.Form_canvas.create_window(0,0, window=self.table_frm,anchor="center")
        self.Form_canvas.update_idletasks()

        self.Form_canvas.config(yscrollcommand = self.scroll.set)

        subjects=["Subject 1","Subject 2","Subject 3","Subject 4","Subject 5"]

        self.report_l={}
        Label(self.table_frm,text="Subject",bg="white",font=('Segoe UI',11,'normal')).grid(row=1,column=0,columnspan=2,pady=1,padx=1,sticky=NSEW)
        Label(self.table_frm,text="Mid Term",bg="white",font=('Segoe UI',11,'normal')).grid(row=1,column=2,pady=1,padx=1,sticky=NSEW)
        Label(self.table_frm,text="Quaterly",bg="white",font=('Segoe UI',11,'normal')).grid(row=1,column=3,pady=1,padx=1,sticky=NSEW)
        Label(self.table_frm,text="Half Yearly",bg="white",font=('Segoe UI',11,'normal')).grid(row=1,column=4,pady=1,padx=1,sticky=NSEW)
        Label(self.table_frm,text="Annual",bg="white",font=('Segoe UI',11,'normal')).grid(row=1,column=5,pady=1,padx=1,sticky=NSEW)
        row = 2
        for j in subjects:
            Label(self.table_frm,text=j,bg="white",font=('Segoe UI',11,'normal')).grid(row=row,column=0,rowspan=3,ipadx=5,pady=1,padx=1,sticky=NSEW)
            Label(self.table_frm,text="Theory",bg="white",font=('Segoe UI',11,'normal')).grid(row=row,column=1,pady=1,padx=1,sticky=NSEW)
            Label(self.table_frm,text="Practicals",bg="white",font=('Segoe UI',11,'normal')).grid(row=row+1,column=1,pady=1,padx=1,sticky=NSEW)
            Label(self.table_frm,text="Total",bg="white",font=('Segoe UI',11,'normal')).grid(row=row+2,column=1,pady=1,padx=1,sticky=NSEW)
            temp_theory=[]
            for i in range(4):
                e=Entry(self.table_frm)
                e.grid(row=row,column=i+2,pady=1,padx=1,sticky=NSEW)
                temp_theory.append(e)
            temp_internal=[]
            for i in range(4):
                e=Entry(self.table_frm)
                e.grid(row=row+1,column=i+2,pady=1,padx=1,sticky=NSEW)
                temp_internal.append(e)
            temp_total=[]
            for i in range(4):
                e=Entry(self.table_frm)
                e.grid(row=row+2,column=i+2,pady=1,padx=1,sticky=NSEW)
                temp_total.append(e)
            row+=3
            self.report_l[j]={"Theory":temp_theory,"Internal":temp_internal,"Total":temp_total}
        Label(self.table_frm,text="Total",bg="white",font=('Segoe UI',11,'normal')).grid(row=row,column=0,columnspan=2,pady=1,padx=1,sticky=NSEW)
        temp_total=[]
        for i in range(4):
            e=Entry(self.table_frm)
            e.grid(row=row,column=i+2,pady=1,padx=1,sticky=NSEW)
            temp_total.append(e)
        self.report_l["Total"]=temp_total


        self.Form_canvas.pack(side=LEFT,fill=BOTH,expand=True,anchor="center")
        self.scroll.pack( side = RIGHT, fill = Y )
        self.open_file()

    def open_file(self):
        self.table_frm.destroy()
        self.table_frm=Frame(self.Form_canvas,bg="black",bd=0)
        self.table_frm.bind("<Configure>",lambda e: self.Form_canvas.configure(scrollregion=self.Form_canvas.bbox("all")))
        self.Form_canvas.create_window(0,0, window=self.table_frm,anchor="center")
        report_l=[]
        Label(self.table_frm,text="Subject",bg="white",font=('Segoe UI',11,'normal')).grid(row=1,column=0,columnspan=2,pady=1,padx=1,sticky=NSEW)
        Label(self.table_frm,text="Mid Term",bg="white",font=('Segoe UI',11,'normal')).grid(row=1,column=2,pady=1,padx=1,sticky=NSEW)
        Label(self.table_frm,text="Quaterly",bg="white",font=('Segoe UI',11,'normal')).grid(row=1,column=3,pady=1,padx=1,sticky=NSEW)
        Label(self.table_frm,text="Half Yearly",bg="white",font=('Segoe UI',11,'normal')).grid(row=1,column=4,pady=1,padx=1,sticky=NSEW)
        Label(self.table_frm,text="Annual",bg="white",font=('Segoe UI',11,'normal')).grid(row=1,column=5,pady=1,padx=1,sticky=NSEW)

        self.name_class_section=[]

        for i in student_data():
            if GET_USER_DETAILS()[0] == str(i[0]):
                self.name_class_section=[i[1]+" "+i[2],i[4],i[5]]
                break

        try:
            self.Name.set(self.name_class_section[0])
            self.Class.set(self.name_class_section[1])
            self.Section.set(self.name_class_section[2])

            if self.name_class_section[1] in ["I","II","III","IV","V","VI","VII","VIII"]:
                mycur.execute('SELECT * FROM MARKS_I_VIII WHERE ADMNO = {}'.format(GET_USER_DETAILS()[0]))
            elif self.name_class_section[1] in ["X","IX"]:
                mycur.execute('SELECT * FROM MARKS_IX_X WHERE ADMNO = {}'.format(GET_USER_DETAILS()[0]))
            elif self.name_class_section[1] in ["XI","XII"]:
                mycur.execute('SELECT * FROM MARKS_XI_XII WHERE ADMNO = {}'.format(GET_USER_DETAILS()[0]))
            elif self.name_class_section[1] in ["LKG","UKG"]:
                mycur.execute('SELECT * FROM MARKS_LKG_UKG WHERE ADMNO = {}'.format(GET_USER_DETAILS()[0]))

            self.marks=mycur.fetchall()

            if self.name_class_section[1] in ["I","II","III","IV","V","VI","VII","VIII"]:
                self.subjects=["English","Mathaematics","Social Science","Science","Second Language","Third Language"]
            elif self.name_class_section[1] in ["X","IX"]:
                self.subjects=["English","Mathaematics","Social Science","Science","Second Language"]
            elif self.name_class_section[1] in ["XI","XII"]:
                self.subjects=["English","Mathematics/\nMarketing","CSC / EG /\nBiology / Accountancy","Chemistry/\nBusiness Studies","Physics/\nEconomics"]
            elif self.name_class_section[1] in ["LKG","UKG"]:
                subjects=["English","Mathaematics","Language","General Awareness","EVS"]
            else:
                self.subjects=["Subject 1","Subject 2","Subject 3","Subject 4","Subject 5"]

            if self.marks != []:
                self.marks=self.marks[0]
        except:
            self.subjects=["Subject 1","Subject 2","Subject 3","Subject 4","Subject 5"]
            self.marks=[]

        
        counter=1
        self.report_l={}
        row = 2
        for j in self.subjects:
            Label(self.table_frm,text=j,bg="white",font=('Segoe UI',11,'normal')).grid(row=row,column=0,rowspan=3,ipadx=5,pady=1,padx=1,sticky=NSEW)
            Label(self.table_frm,text="Theory",bg="white",font=('Segoe UI',11,'normal')).grid(row=row,column=1,pady=1,padx=1,sticky=NSEW)
            Label(self.table_frm,text="Practicals",bg="white",font=('Segoe UI',11,'normal')).grid(row=row+1,column=1,pady=1,padx=1,sticky=NSEW)
            Label(self.table_frm,text="Total",bg="white",font=('Segoe UI',11,'normal')).grid(row=row+2,column=1,pady=1,padx=1,sticky=NSEW)
            
            temp_theory=[]
            for i in range(4):
                e=Entry(self.table_frm)
                e.grid(row=row,column=i+2,pady=1,padx=1,sticky=NSEW)
                if self.marks != []:
                    e.insert(0,self.marks[counter])
                    counter+=1
                temp_theory.append(e)
                
            temp_internal=[]
            for i in range(4):
                e=Entry(self.table_frm)
                e.grid(row=row+1,column=i+2,pady=1,padx=1,sticky=NSEW)
                if self.marks != []:
                    e.insert(0,self.marks[counter])
                    counter+=1
                temp_internal.append(e)
                
            temp_total=[]
            for i in range(4):
                e=Entry(self.table_frm)
                e.grid(row=row+2,column=i+2,pady=1,padx=1,sticky=NSEW)
                if self.marks != []:
                    e.insert(0,self.marks[counter])
                    counter+=1
                temp_total.append(e)
                
            row+=3
            self.report_l[j]={"Theory":temp_theory,"Internal":temp_internal,"Total":temp_total}
        Label(self.table_frm,text="Total",bg="white",font=('Segoe UI',11,'normal')).grid(row=row,column=0,columnspan=2,pady=1,padx=1,sticky=NSEW)
        temp_total=[]
        for i in range(4):
            e=Entry(self.table_frm)
            e.grid(row=row,column=i+2,pady=1,padx=1,sticky=NSEW)
            if self.marks != []:
                e.insert(0,self.marks[counter])
                counter+=1
            temp_total.append(e)
        self.report_l["Total"]=temp_total

    def print_file(self):

        file = open("School_details.txt","r")
        School_details=file.readlines()
        file.close()

        for i in student_data():
            if GET_USER_DETAILS()[0] == str(i[0]):
                self.name_class_section=[i[1]+" "+i[2],i[4],i[5]]
                break
            else:
                self.name_class_section=[]
                        
        if self.name_class_section != []:
            data_dict = {
                "info":{
                        "admno":GET_USER_DETAILS()[0],
                        "name":self.name_class_section[0],
                        "class":self.name_class_section[1],
                        "sec":self.name_class_section[2],
                        "school name": School_details[0]
                    },
                "subjects":self.subjects,
                "midterm":[],
                "quaterly":[],
                "halfyearly":[],
                "annual":[]
            }        
            
            for i,j in self.report_l.items():
                if i == "Total":
                    pass
                else:
                    data_dict["midterm"].append([int(j["Theory"][0].get()),int(j["Internal"][0].get())])
                    data_dict["quaterly"].append([int(j["Theory"][1].get()),int(j["Internal"][1].get())])
                    data_dict["halfyearly"].append([int(j["Theory"][2].get()),int(j["Internal"][2].get())])
                    data_dict["annual"].append([int(j["Theory"][3].get()),int(j["Internal"][3].get())])
                        
            data_dict["midterm_total"]=sum([j for j in ([sum(i) for i in data_dict["midterm"]])])
            data_dict["quaterly_total"]=sum([j for j in ([sum(i) for i in data_dict["quaterly"]])])
            data_dict["halfyearly_total"]=sum([j for j in ([sum(i) for i in data_dict["halfyearly"]])])
            data_dict["annual_total"]=sum([j for j in ([sum(i) for i in data_dict["annual"]])])

            school_name=f'{data_dict["info"]["school name"]:^70}\n'

            report_string = f'''Admin No: {data_dict["info"]["admno"]}
Name: {data_dict["info"]["name"]}
Class: {data_dict["info"]["class"]}
Section: {data_dict["info"]["sec"]}

+{"":-^36}+{"":-<15}+{"":-<15}+{"":-<15}+{"":-<15}+
|{"Subject":^36}|{"Mid Term":^15}|{"Quaterly":^15}|{"Half Yearly":^15}|{"Annual":^15}|
+{"":-^36}+{"":-<15}+{"":-<15}+{"":-<15}+{"":-<15}+'''
    

            mark_string = ''
            for i in range(len(data_dict["subjects"])):
                mark_string += f'''|{"":^20}|{"Theory":^15}|{(data_dict["midterm"][i][0]):^15}|{(data_dict["quaterly"][i][0]):^15}|{(data_dict["halfyearly"][i][0]):^15}|{(data_dict["annual"][i][0]):^15}|
|{"":^20}|{"":-<15}+{"":-<15}+{"":-<15}+{"":-<15}+{"":-<15}+
|{data_dict["subjects"][i]:^20}|{"Practicals":^15}|{data_dict["midterm"][i][1]:^15}|{data_dict["quaterly"][i][1]:^15}|{data_dict["halfyearly"][i][1]:^15}|{data_dict["annual"][i][1]:^15}|
|{"":^20}|{"":-<15}+{"":-<15}+{"":-<15}+{"":-<15}+{"":-<15}+
|{"":^20}|{"Total":^15}|{(data_dict["midterm"][i][0]+data_dict["midterm"][i][1]):^15}|{(data_dict["quaterly"][i][0]+data_dict["quaterly"][i][1]):^15}|{(data_dict["halfyearly"][i][0]+data_dict["halfyearly"][i][1]):^15}|{(data_dict["annual"][i][0]+data_dict["annual"][i][1]):^15}|
+{"":-^20}+{"":-<15}+{"":-<15}+{"":-<15}+{"":-<15}+{"":-<15}+
'''

            total=f'''|{"Total":^36}|{data_dict["midterm_total"]:^15}|{data_dict["quaterly_total"]:^15}|{data_dict["halfyearly_total"]:^15}|{data_dict["annual_total"]:^15}|
+{"":-^36}+{"":-<15}+{"":-<15}+{"":-<15}+{"":-<15}+'''

            f = open('reportcard.txt', 'w')
            f.write(school_name + '\n' + report_string + '\n' + mark_string + total + "\n" + '''\n\n**This is a computer generated Report Card''')
            f.close()
        else:
            messagebox.showerror("DataHIVE","Unable to Print Report Card")

if __name__ == "__main__":
    root=Tk()
    Manager_student(root)
    root.mainloop()
