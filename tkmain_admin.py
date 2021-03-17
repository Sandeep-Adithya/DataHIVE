import sys
sys.path.append(sys.path[0]+"\packages")
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkcalendar import DateEntry
import time
import datetime
import os
from tkinter import messagebox
import ctypes
import mysql.connector as sql
import csv
import webbrowser
import Login
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

def teacher_data():
    tdata=[]
    mycur.execute('SELECT * FROM TEACHERS ORDER BY EMPNO')
    tdata=mycur.fetchall()
    return tdata

def staff_data():
    stdata=[]
    mycur.execute('SELECT * FROM STAFFS ORDER BY EMPNO')
    stdata=mycur.fetchall()
    return stdata

def update_dash():
    no_of_students.set(len(student_data()))
    no_of_teachers.set(len(teacher_data()))
    no_of_staffs.set(len(staff_data()))

def update_table(table,table_name):
    try:
        table.delete(*table.get_children())
    except:
        pass
    if table_name == "student":
        for i in student_data():
            table.insert('','end',values=i)
    elif table_name == "teacher":
        for i in teacher_data():
            table.insert('','end',values=i)
    elif table_name == "staff":
        for i in staff_data():
            table.insert('','end',values=i)

def update_table_with_checks(table,table_name):
    try:
        table.delete(*table.get_children())
    except:
        pass
    if table_name == "student":
        for i in student_data():
            table.insert('','end',values=i,tags="unchecked")
    elif table_name == "teacher":
        for i in teacher_data():
            table.insert('','end',values=i,tags="unchecked")
    elif table_name == "staff":
        for i in staff_data():
            table.insert('','end',values=i,tags="unchecked")

def close_window_main():
    if messagebox.askyesno("DATAHIVE","Are you sure? Do you want to exit"):
        Main.destroy()
    else:
        pass

def logout(self):
    mydb.close()
    self.root.destroy()
    Login.call_logout()

def launch_manager():
    global root
    root=Tk()
    Manager_admin(root)
    root.protocol("WM_DELETE_WINDOW",close_window)

class Manager_admin:

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

        #students button
        self.stu_ico = PhotoImage(file = "icons\\student.png") 
        self.root.st=self.stu_ico
        self.stu=Button(self.menu,image = self.stu_ico,fg="white",bd=0,justify=LEFT,bg="#101724",activeforeground="white",activebackground="#000817",cursor="arrow",height=38,compound ='c',command=lambda: self.show_frame(students_details),anchor="center")
        self.stu.pack(anchor="center",fill=X)

        #teachers button
        self.teac_ico = PhotoImage(file = "icons\\teacher.png") 
        self.root.te=self.teac_ico
        self.teac=Button(self.menu,image = self.teac_ico,fg="white",bd=0,justify=LEFT,bg="#101724",activeforeground="white",activebackground="#000817",cursor="arrow",height=38,compound ='c',command=lambda: self.show_frame(teachers),anchor="center")
        self.teac.pack(anchor="center",fill=X)

        #staffs button
        self.staf_ico = PhotoImage(file = "icons\\staffs.png") 
        self.root.st=self.staf_ico
        self.staf=Button(self.menu,image = self.staf_ico,fg="white",bd=0,justify=RIGHT,bg="#101724",activeforeground="white",activebackground="#000817",cursor="arrow",height=38,compound ='c',command=lambda: self.show_frame(staffs),anchor="center")
        self.staf.pack(anchor="center",fill=X)

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

        #announcement
        self.ann_ico = PhotoImage(file = "icons\\announcement.png") 
        self.root.ann=self.ann_ico
        self.ann=Button(self.menu,image = self.ann_ico,fg="white",bd=0,justify=RIGHT,bg="#101724",activeforeground="white",activebackground="#000817",cursor="arrow",height=38,compound ='c',command=lambda: self.show_frame(announcements),anchor="center")
        self.ann.pack(anchor="center",fill=X)

        #event
        self.event_ico = PhotoImage(file = "icons\\event.png") 
        self.root.event=self.event_ico
        self.event=Button(self.menu,image = self.event_ico,fg="white",bd=0,justify=RIGHT,bg="#101724",activeforeground="white",activebackground="#000817",cursor="arrow",height=38,compound ='c',command=lambda: self.show_frame(events),anchor="center")
        self.event.pack(anchor="center",fill=X)

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
        user_details=GET_USER_DETAILS()
        self.user = Label(self.topbar,font=('Segoe UI',10),justify=LEFT,text=user_details[0]+'\n'+user_details[1],bg='#4da6ff',fg="#101724")
        self.user.pack(side=RIGHT)

        ttk.Separator(self.topbar, orient='vertical',style="Line.TSeparator").pack(fill=Y,side=RIGHT,pady=3,padx=5)

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
        page_list=[loading, dashboard, time_table, report_card, about_software, announcements, events,
                    students_details, add_new_student, modify_student_details, delete_student, search_student, 
                    teachers, add_new_teacher, modify_teacher_details, delete_teacher, search_teacher, 
                    staffs, add_new_staff, modify_staff_details, delete_staff, search_staff]
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
            self.stu.config(text="",compound='c',anchor="center")
            self.teac.config(text="",compound='c',anchor="center")
            self.staf.config(text="",compound='c',anchor="center")
            self.lout.config(text="",compound='c',anchor="center")
            self.abt.config(text="",compound='c',anchor="center")
            self.ttable.config(text="",compound='c',anchor="center")
            self.rcard.config(text="",compound='c',anchor="center")
            self.ann.config(text="",compound='c',anchor="center")
            self.event.config(text="",compound='c',anchor="center")
        else:
            self.menu.config(width=140)
            self.dash  .config(text=" Dashboard",compound=LEFT,anchor=W)
            self.stu   .config(text=" Students",compound=LEFT,anchor=W)
            self.teac  .config(text=" Teachers",compound=LEFT,anchor=W)
            self.staf  .config(text=" Staffs",compound=LEFT,anchor=W)
            self.lout  .config(text=" Logout",compound=LEFT,anchor=W)
            self.abt   .config(text=" About",compound=LEFT,anchor=W)
            self.ttable.config(text=" Time Table",compound=LEFT,anchor=W)
            self.rcard .config(text=" Report Card",compound=LEFT,anchor=W)
            self.ann   .config(text=" Announcement",compound=LEFT,anchor=W)
            self.event .config(text=" Events",compound=LEFT,anchor=W)

#students
class students_details(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(background="#ecf0f5")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        stu_add=PhotoImage(file = "icons\\student-add-100.png")
        add=Button(self,image=stu_add,width=400,height=200,text="                 ADD",font=('Segoe UI', 30),bg="#443085",bd=0,activebackground="#000817",compound ='left',command=lambda: controller.show_frame(add_new_student))
        add.image=stu_add
        add.grid(row=0,column=0,sticky=N+S+E+W,padx=10,pady=10)

        stu_modify=PhotoImage(file = "icons\\student-modify-100.png")
        modify=Button(self,image=stu_modify,width=400,height=200,text="           MODIFY",font=('Segoe UI', 30),bg="#f39c12",bd=0,activebackground="#000817",compound ='left',command=lambda: controller.show_frame(modify_student_details))
        modify.image=stu_modify
        modify.grid(row=0,column=1,sticky=N+S+E+W,padx=10,pady=10)

        stu_search=PhotoImage(file = "icons\\student-search-100.png")
        search=Button(self,image=stu_search,width=400,height=200,text="           SEARCH",font=('Segoe UI', 30),bg="#00a65a",bd=0,activebackground="#000817",compound ='left',command=lambda: controller.show_frame(search_student))
        search.image=stu_search
        search.grid(row=1,column=0,sticky=N+S+E+W,padx=10,pady=10)

        stu_delete=PhotoImage(file = "icons\\student-delete-100.png")
        delete=Button(self,image=stu_delete,width=400,height=200,text="             DELETE",font=('Segoe UI', 30),bg="#f56954",bd=0,activebackground="#000817",compound ='left',command=lambda: controller.show_frame(delete_student))
        delete.image=stu_delete
        delete.grid(row=1,column=1,sticky=N+S+E+W,padx=10,pady=10)     

class add_new_student(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(background="#ecf0f5")

        self.s=ttk.Style()
        self.s.theme_use("vista")

        self.Admno=StringVar()
        self.F_Name=StringVar()
        self.L_Name=StringVar()
        self.EMIS=StringVar()
        self.Class=StringVar()
        self.Section=StringVar()
        self.DOB=StringVar()
        self.DOJ=StringVar()
        self.Gender=StringVar()
        self.Nationality=StringVar()
        self.MotherTongue=StringVar()
        self.lang2=StringVar()
        self.lang3=StringVar() 
        self.Course=StringVar()
        self.fathername=StringVar()
        self.fatherno=StringVar()
        self.mothername=StringVar()
        self.motherno=StringVar()
        self.Email_Address=StringVar()
        
        self.Form_canvas=Canvas(self,background="#ecf0f5")
        self.scroll=ttk.Scrollbar(self,command = self.Form_canvas.yview)
        self.Form_main=Frame(self.Form_canvas,bg="white",bd=0)
        self.Form_main.bind("<Configure>",lambda e: self.Form_canvas.configure(scrollregion=self.Form_canvas.bbox("all")))
        self.Scroll_Form = self.Form_canvas.create_window(0,0, window=self.Form_main,anchor="nw")
        self.Form_canvas.config(yscrollcommand = self.scroll.set)

        Canvas(self.Form_main,height=80,bg="#ecf0f5",borderwidth=0).pack(fill=X,ipadx=150)

        Label(self.Form_main,text="Student Information",bg="white",font=('Segoe UI Light',20,'normal')).pack(padx=5,pady=15)

        self.Adm_frm=Frame(self.Form_main,bg="white")
        Label(self.Adm_frm,text="Admission Number",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Adm_entry_box = LabelFrame(self.Adm_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Adm_entry = Entry(self.Adm_entry_box,textvariable = self.Admno,bd=0,font=('Segoe UI', 11))
        self.Adm_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Adm_entry_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Adm_frm.pack(padx=20,anchor=W)
        
        self.Name_frm = Frame(self.Form_main,bg="white")
        Label(self.Name_frm,text="Name",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.F_Name_entry_box = LabelFrame(self.Name_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.F_Name_entry = Entry(self.F_Name_entry_box,textvariable = self.F_Name,bd=0,font=('Segoe UI', 11))
        self.F_Name_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.F_Name_entry_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.L_Name_entry_box = LabelFrame(self.Name_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.L_Name_entry = Entry(self.L_Name_entry_box,textvariable = self.L_Name,bd=0,font=('Segoe UI', 11))
        self.L_Name_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.L_Name_entry_box.grid(row=1,column=1,padx=6,sticky=N+S+W+E)
        Label(self.Name_frm,text="First Name ",bg="white",font=('Segoe UI',10,'normal')).grid(row=2,column=0,sticky=W)
        Label(self.Name_frm,text="Last Name ",bg="white",font=('Segoe UI',10,'normal')).grid(row=2,column=1,sticky=W,padx=6)
        self.Name_frm.pack(padx=20,anchor=W)

        self.EMIS_frm = Frame(self.Form_main,bg="white")
        Label(self.EMIS_frm,text="EMIS Number ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.EMIS_entry_box = LabelFrame(self.EMIS_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.EMIS_entry = Entry(self.EMIS_entry_box,textvariable = self.EMIS,bd=0,font=('calibre',10,'normal'))
        self.EMIS_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.EMIS_entry_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.EMIS_frm.pack(padx=20,anchor=W)

        self.Class_Section_frm = Frame(self.Form_main,bg="white")
        Label(self.Class_Section_frm,text="Class ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Class_DD_box = LabelFrame(self.Class_Section_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Class_DD = ttk.Combobox(self.Class_DD_box,textvariable = self.Class)
        self.Class_DD["values"]=["LKG","UKG","I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"]
        self.Class_DD.pack(fill=BOTH,ipady=8)
        self.Class_DD_box.grid(row=1,column=0,sticky=N+S+W+E)
        Label(self.Class_Section_frm,text="Section ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=1,padx=6,pady=3,sticky=W)
        self.Section_DD_box = LabelFrame(self.Class_Section_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Section_DD = ttk.Combobox(self.Section_DD_box,textvariable = self.Section)
        self.Section_DD["values"]=["A","B","C","D","E"]
        self.Section_DD.pack(fill=BOTH,ipady=8)
        self.Section_DD_box.grid(row=1,column=1,sticky=N+S+W+E,padx=6)
        self.Class_Section_frm.pack(padx=20,anchor=W)

        self.Date_frm = Frame(self.Form_main,bg="white")
        Label(self.Date_frm,text="Date of Birth",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.DOB_box = LabelFrame(self.Date_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.DOB_entry = DateEntry(self.DOB_box,textvariable=self.DOB,width=20,background='#00264d',foreground='#ecf0f5',date_pattern="yyyy-mm-dd")
        self.DOB_entry.pack(fill=BOTH,ipady=8)
        self.DOB_box.grid(row=1,column=0,sticky=N+S+W+E)
        Label(self.Date_frm,text="Date of Join",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=1,padx=6,pady=3,sticky=W)
        self.DOJ_box = LabelFrame(self.Date_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.DOJ_entry = DateEntry(self.DOJ_box,textvariable=self.DOJ,width=20,background='#00264d',foreground='#ecf0f5',date_pattern="yyyy-mm-dd")
        self.DOJ_entry.pack(fill=BOTH,ipady=8)
        self.DOJ_box.grid(row=1,column=1,sticky=N+S+W+E,padx=6)
        self.Date_frm.pack(padx=20,anchor=W)

        self.Gender_frm=Frame(self.Form_main,bg="white")
        Label(self.Gender_frm,text="Gender ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Gender_box = LabelFrame(self.Gender_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Gender_entry = ttk.Combobox(self.Gender_box,textvariable = self.Gender,width=25)
        self.Gender_entry["values"]=["Male","Female"]
        self.Gender_entry.pack(fill=BOTH,ipady=8)
        self.Gender_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Gender_frm.pack(padx=20,anchor=W)

        self.Nationality_MT_frm = Frame(self.Form_main,bg="white")
        Label(self.Nationality_MT_frm,text="Nationality ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Nationality_box = LabelFrame(self.Nationality_MT_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Nationality_entry = Entry(self.Nationality_box,textvariable = self.Nationality,bd=0,font=('calibre',10,'normal'))
        self.Nationality_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Nationality_box.grid(row=1,column=0,sticky=N+S+W+E)
        Label(self.Nationality_MT_frm,text="Mother Tongue ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=1,padx=6,pady=3,sticky=W)
        self.MT_box = LabelFrame(self.Nationality_MT_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.MT_entry = Entry(self.MT_box,textvariable = self.MotherTongue,bd=0,font=('calibre',10,'normal'))
        self.MT_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.MT_box.grid(row=1,column=1,padx=6,sticky=N+S+W+E)
        self.Nationality_MT_frm.pack(padx=20,anchor=W)

        self.Course_frm = Frame(self.Form_main,bg="white")
        Label(self.Course_frm,text="2nd Language ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.lang2_box = LabelFrame(self.Course_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.lang2_entry = ttk.Combobox(self.lang2_box,textvariable = self.lang2,width=25)
        self.lang2_entry["values"]=["Tamil","Telugu","Hindi"]
        self.lang2_entry.pack(fill=BOTH,ipady=8)
        self.lang2_box.grid(row=1,column=0,sticky=N+S+W+E)
        Label(self.Course_frm,text="3rd Language ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=1,padx=6,pady=3,sticky=W)
        self.lang3_box = LabelFrame(self.Course_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.lang3_entry = ttk.Combobox(self.lang3_box,textvariable = self.lang3,width=25)
        self.lang3_entry["values"]=["Tamil","Telugu","Hindi"]
        self.lang3_entry.pack(fill=BOTH,ipady=8)
        self.lang3_box.grid(row=1,column=1,padx=6,sticky=N+S+W+E)
        Label(self.Course_frm,text="Stream ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=2,padx=6,pady=3,sticky=W)
        self.Course_box = LabelFrame(self.Course_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Course_entry = ttk.Combobox(self.Course_box,textvariable = self.Course,width=25)
        self.Course_entry["values"]=["Science","Commerce","Humanities"]
        self.Course_entry.pack(fill=BOTH,ipady=8)
        self.Course_box.grid(row=1,column=2,padx=6,sticky=N+S+W+E)
        self.Course_frm.pack(padx=20,anchor=W)

        Label(self.Form_main,text="Parents' Information ",bg="white",font=('Segoe UI Light',20,'normal')).pack(padx=5,pady=15)

        self.father_details = Frame(self.Form_main,bg="white")
        Label(self.father_details,text="Father's Name ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.fathername_box = LabelFrame(self.father_details,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.fathername_entry = Entry(self.fathername_box,bd=0,textvariable = self.fathername ,font=('calibre',10,'normal'))
        self.fathername_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.fathername_box.grid(row=1,column=0,sticky=N+S+W+E)
        Label(self.father_details,text="Father's Mobile Number ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=1,padx=6,pady=3,sticky=W)
        self.fatherno_box = LabelFrame(self.father_details,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.fatherno_entry = Entry(self.fatherno_box,bd=0,textvariable = self.fatherno,font=('calibre',10,'normal'))
        self.fatherno_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.fatherno_box.grid(row=1,column=1,padx=6,sticky=N+S+W+E)
        self.father_details.pack(padx=20,anchor=W)

        self.mother_details = Frame(self.Form_main,bg="white")
        Label(self.mother_details,text="Mother's Name ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.mothername_box = LabelFrame(self.mother_details,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.mothername_entry = Entry(self.mothername_box,bd=0,textvariable = self.mothername ,font=('calibre',10,'normal'))
        self.mothername_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.mothername_box.grid(row=1,column=0,sticky=N+S+W+E)
        Label(self.mother_details,text="Mother's Mobile Number",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=1,padx=6,pady=3,sticky=W)
        self.motherno_box = LabelFrame(self.mother_details,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.motherno_entry = Entry(self.motherno_box,bd=0,textvariable = self.motherno,font=('calibre',10,'normal'))
        self.motherno_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.motherno_box.grid(row=1,column=1,padx=6,sticky=N+S+W+E)
        self.mother_details.pack(padx=20,anchor=W)
        
        self.EMAIL_frm = Frame(self.Form_main,bg="white")
        Label(self.EMAIL_frm,text="Email Address",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Email_box = LabelFrame(self.EMAIL_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Email_Address_entry = Entry(self.Email_box,bd=0,width=60,textvariable = self.Email_Address,font=('calibre',10,'normal'))
        self.Email_Address_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Email_box.grid(row=1,column=0,columnspan=2,sticky=N+S+W+E)
        self.EMAIL_frm.pack(padx=20,anchor=W)

        Label(self.Form_main,text="Residential Information",bg="white",font=('Segoe UI Light',20,'normal')).pack(padx=5,pady=15)

        self.Address_frm = Frame(self.Form_main,bg="white")
        Label(self.Address_frm,text="Residence Address",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.House_box = LabelFrame(self.Address_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.House_Address_text = Text(self.House_box,bd=0,width=40,height=5)
        self.House_Address_text.pack(fill=BOTH,padx=10,ipady=8)
        self.House_box.grid(row=1,column=0,columnspan=2,sticky=N+S+W+E)
        self.Address_frm.pack(padx=20,anchor=W)

        self.button_frm = Frame(self.Form_main,bg="white")
        self.clear = Button(self.button_frm,text="Clear",font=('Segoe UI',11,'normal'),width=12,height=2,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.clear_all())
        self.clear.grid(row=0,column=0,sticky=N+S+W+E)
        self.submit = Button(self.button_frm,text="Submit",font=('Segoe UI',11,'normal'),width=15,height=2,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.Submit())
        self.submit.grid(row=0,column=1,padx=6,sticky=N+S+W+E)
        self.button_frm.pack(padx=20,pady=10,anchor=E)

        Canvas(self.Form_main,height=80,bg="#ecf0f5",borderwidth=0).pack(fill=X,ipadx=150)
        self.Form_canvas.pack(fill=Y,side=LEFT,expand=True,anchor="center",ipadx=150)
        self.scroll.pack( side = RIGHT, fill = Y )

        self.clear_all()
        self.Class_DD.bind("<<ComboboxSelected>>", lambda event: self.EnableDisableFields())

    def clear_all(self):
        self.Adm_entry.delete(0,END)
        self.F_Name_entry.delete(0,END)
        self.L_Name_entry.delete(0,END)
        self.EMIS_entry.delete(0,END)
        self.Class_DD.delete(0,END)
        self.Section_DD.delete(0,END)
        self.DOB_entry.delete(0,END)
        self.DOJ_entry.delete(0,END)
        self.Nationality_entry.delete(0,END)
        self.MT_entry.delete(0,END)
        self.lang2_entry.delete(0,END)
        self.lang3_entry.delete(0,END)
        self.Course_entry.delete(0,END)
        self.fathername_entry.delete(0,END)
        self.fatherno_entry.delete(0,END)
        self.mothername_entry.delete(0,END)
        self.motherno_entry.delete(0,END)
        self.Email_Address_entry.delete(0,END)
        self.House_Address_text.delete("1.0",END)
        self.lang2_entry.config(state="normal")
        self.lang3_entry.config(state="normal")
        self.Course_entry.config(state='normal')

    def EnableDisableFields(self):
        if self.Class.get() in ["I","II","III","IV","V","VI","VII","VIII"]:
            self.lang2_entry.config(state="normal")
            self.lang3_entry.config(state="normal")
            self.Course_entry.config(state='disabled')

        elif self.Class.get() in ["X","IX"]:
            self.lang2_entry.config(state="normal")
            self.lang3_entry.config(state="disabled")
            self.Course_entry.config(state='disabled')

        elif self.Class.get() in ["XI","XII"]:
            self.lang2_entry.config(state="disabled")
            self.lang3_entry.config(state="disabled")
            self.Course_entry.config(state='normal')

        elif self.Class.get() in ["LKG","UKG"]:
            self.lang2_entry.config(state="disabled")
            self.lang3_entry.config(state="disabled")
            self.Course_entry.config(state='disabled')

    def Submit(self):
        for i in student_data():
            if int(self.Admno.get()) == i[0]:
                messagebox.showerror("DATAHIVE","Student with this Admission Number is Already Available")
                break
        else:
            if self.Admno.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Admission Number")
            elif self.F_Name.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter First Name")
            elif self.L_Name.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Last Name")
            elif self.EMIS.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter EMIS Number")
            elif len(self.EMIS.get()) != 16:
                messagebox.showerror("DATAHIVE","Please Enter a 12 digit EMIS Number")
            elif not self.EMIS.get().isdigit():
                messagebox.showerror("DATAHIVE","Enter a Valid EMIS Number")
            elif self.Class.get() == "":
                messagebox.showerror("DATAHIVE","Please Select the Class")
            elif self.Section.get() == "":
                messagebox.showerror("DATAHIVE","Please Select the Section")
            elif self.DOB.get() == "":
                messagebox.showerror("DATAHIVE","Please Select Date of Birth")
            elif self.DOJ.get() == "":
                messagebox.showerror("DATAHIVE","Please Select Date of Joining")
            elif self.Nationality.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Nationality")
            elif self.MotherTongue.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Mother Tongue")
            elif self.fathername.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Father's Name")
            elif self.fatherno.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Father's Mobile Number")
            elif not self.fatherno.get().isdigit() and len(self.fatherno.get())==10:
                messagebox.showerror("DATAHIVE","Father's Mobile Number is InValid")
            elif self.mothername.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Mother's Name")
            elif self.motherno.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Mother's Mobile Number")
            elif not self.motherno.get().isdigit() and len(self.motherno.get())==10:
                messagebox.showerror("DATAHIVE","Mother's Mobile Number is InValid")
            elif self.Email_Address.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Email Address")
            elif ".com" not in self.Email_Address.get() or "@" not in self.Email_Address.get():
                messagebox.showerror("DATAHIVE","Enter a Valid Email Address")
            elif self.House_Address_text.get("1.0",END) == "":
                messagebox.showerror("DATAHIVE","Please Enter Residential Address")
            elif self.Class.get() in ["I","II","III","IV","V","VI","VII","VIII"]:
                if self.lang2.get() == "":
                    messagebox.showerror("DATAHIVE","Please Choose 2nd Language")
                elif self.lang3.get() == "":
                    messagebox.showerror("DATAHIVE","Please Choose 3nd Language")
                else:
                    l=[self.Admno.get(), self.F_Name.get(), self.L_Name.get(), self.EMIS.get(), self.Class.get(), self.Section.get(), self.DOB.get(), self.DOJ.get(),self.Gender.get() , self.Nationality.get(), self.MotherTongue.get(), self.lang2.get(), self.lang3.get(), self.fathername.get(), self.fatherno.get(), self.mothername.get(), self.motherno.get(), self.Email_Address.get(), self.House_Address_text.get("1.0",END)]
                mycur.execute("INSERT INTO i_viii VALUES({},'{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{},'{}',{},'{}','{}')".format(*l))
                mydb.commit()
                messagebox.showinfo("DATAHIVE","Student Added")
                update_dash()
                self.clear_all()
            elif self.Class.get() in ["IX","X"]:
                if self.lang2.get() == "":
                    messagebox.showerror("DATAHIVE","Please Choose 2nd Language")
                else:
                    l=[self.Admno.get(), self.F_Name.get(), self.L_Name.get(), self.EMIS.get(), self.Class.get(), self.Section.get(), self.DOB.get(), self.DOJ.get(),self.Gender.get() , self.Nationality.get(), self.MotherTongue.get(), self.lang2.get(), self.fathername.get(), self.fatherno.get(), self.mothername.get(), self.motherno.get(), self.Email_Address.get(), self.House_Address_text.get("1.0",END)]
                mycur.execute("INSERT INTO ix_x VALUES({},'{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}',{},'{}',{},'{}','{}')".format(*l))
                mydb.commit()
                messagebox.showinfo("DATAHIVE","Student Added")
                update_dash()
                self.clear_all()
            elif self.Class.get() in ["XI","XII"]:
                if self.Course.get() == "":
                    messagebox.showerror("DATAHIVE","Please Choose Stream")
                else:
                    l=[self.Admno.get(), self.F_Name.get(), self.L_Name.get(), self.EMIS.get(), self.Class.get(), self.Section.get(), self.DOB.get(), self.DOJ.get(),self.Gender.get() , self.Nationality.get(), self.MotherTongue.get(), self.Course.get(), self.fathername.get(), self.fatherno.get(), self.mothername.get(), self.motherno.get(), self.Email_Address.get(), self.House_Address_text.get("1.0",END)]
                mycur.execute("INSERT INTO xi_xii VALUES({},'{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}',{},'{}',{},'{}','{}')".format(*l))
                mydb.commit()
                messagebox.showinfo("DATAHIVE","Student Added")
                update_dash()
                self.clear_all()
            elif self.Class.get() in ["LKG","UKG"]:
                l=[self.Admno.get(), self.F_Name.get(), self.L_Name.get(), self.EMIS.get(), self.Class.get(), self.Section.get(), self.DOB.get(), self.DOJ.get(),self.Gender.get() , self.Nationality.get(), self.MotherTongue.get(), self.fathername.get(), self.fatherno.get(), self.mothername.get(), self.motherno.get(), self.Email_Address.get(), self.House_Address_text.get("1.0",END)]
                mycur.execute("INSERT INTO LKG_UKG VALUES({},'{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}',{},'{}',{},'{}','{}')".format(*l))
                mydb.commit()
                messagebox.showinfo("DATAHIVE","Student Added")
                update_dash()
                self.clear_all()

class modify_student_details(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(background="#ecf0f5")

        
        self.s=ttk.Style()
        self.s.theme_use("vista")

        self.Admno=StringVar()
        self.F_Name=StringVar()
        self.L_Name=StringVar()
        self.EMIS=StringVar()
        self.Class=StringVar()
        self.Section=StringVar()
        self.DOB=StringVar()
        self.DOJ=StringVar()
        self.Gender=StringVar()
        self.Nationality=StringVar()
        self.MotherTongue=StringVar()
        self.lang2=StringVar()
        self.lang3=StringVar() 
        self.Course=StringVar()
        self.fathername=StringVar()
        self.fatherno=StringVar()
        self.mothername=StringVar()
        self.motherno=StringVar()
        self.Email_Address=StringVar()
        
        self.Form_canvas=Canvas(self,background="#ecf0f5")
        self.scroll=ttk.Scrollbar(self,command = self.Form_canvas.yview)
        self.Form_main=Frame(self.Form_canvas,bg="white",bd=0)
        self.Form_main.bind("<Configure>",lambda e: self.Form_canvas.configure(scrollregion=self.Form_canvas.bbox("all")))
        self.Scroll_Form = self.Form_canvas.create_window(0,0, window=self.Form_main,anchor="nw")
        self.Form_canvas.config(yscrollcommand = self.scroll.set)

        Canvas(self.Form_main,height=80,bg="#ecf0f5",borderwidth=0).pack(fill=X,ipadx=150)

        Label(self.Form_main,text="Student Information",bg="white",font=('Segoe UI Light',20,'normal')).pack(padx=5,pady=15)

        self.Adm_frm=Frame(self.Form_main,bg="white")
        Label(self.Adm_frm,text="Admission Number",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Adm_entry_box = LabelFrame(self.Adm_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Adm_entry = Entry(self.Adm_entry_box,textvariable = self.Admno,bd=0,font=('Segoe UI', 11))
        self.Adm_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Adm_entry_box.grid(row=1,column=0,sticky=N+S+W+E)
        Button(self.Adm_frm,text="Check",font=('Segoe UI',11,'normal'),width=12,height=2,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.check_adm()).grid(row=1,column=1,padx=8)
        self.Adm_frm.pack(padx=20,anchor=W)
        
        self.Name_frm = Frame(self.Form_main,bg="white")
        Label(self.Name_frm,text="Name",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.F_Name_entry_box = LabelFrame(self.Name_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.F_Name_entry = Entry(self.F_Name_entry_box,textvariable = self.F_Name,bd=0,font=('Segoe UI', 11))
        self.F_Name_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.F_Name_entry_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.L_Name_entry_box = LabelFrame(self.Name_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.L_Name_entry = Entry(self.L_Name_entry_box,textvariable = self.L_Name,bd=0,font=('Segoe UI', 11))
        self.L_Name_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.L_Name_entry_box.grid(row=1,column=1,padx=6,sticky=N+S+W+E)
        Label(self.Name_frm,text="First Name ",bg="white",font=('Segoe UI',10,'normal')).grid(row=2,column=0,sticky=W)
        Label(self.Name_frm,text="Last Name ",bg="white",font=('Segoe UI',10,'normal')).grid(row=2,column=1,sticky=W,padx=6)
        self.Name_frm.pack(padx=20,anchor=W)

        self.EMIS_frm = Frame(self.Form_main,bg="white")
        Label(self.EMIS_frm,text="EMIS Number ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.EMIS_entry_box = LabelFrame(self.EMIS_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.EMIS_entry = Entry(self.EMIS_entry_box,textvariable = self.EMIS,bd=0,font=('calibre',10,'normal'))
        self.EMIS_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.EMIS_entry_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.EMIS_frm.pack(padx=20,anchor=W)

        self.Class_Section_frm = Frame(self.Form_main,bg="white")
        Label(self.Class_Section_frm,text="Class ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Class_DD_box = LabelFrame(self.Class_Section_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Class_DD = ttk.Combobox(self.Class_DD_box,textvariable = self.Class)
        self.Class_DD["values"]=["LKG","UKG","I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"]
        self.Class_DD.pack(fill=BOTH,ipady=8)
        self.Class_DD_box.grid(row=1,column=0,sticky=N+S+W+E)
        Label(self.Class_Section_frm,text="Section ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=1,padx=6,pady=3,sticky=W)
        self.Section_DD_box = LabelFrame(self.Class_Section_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Section_DD = ttk.Combobox(self.Section_DD_box,textvariable = self.Section)
        self.Section_DD["values"]=["A","B","C","D","E"]
        self.Section_DD.pack(fill=BOTH,ipady=8)
        self.Section_DD_box.grid(row=1,column=1,sticky=N+S+W+E,padx=6)
        self.Class_Section_frm.pack(padx=20,anchor=W)

        self.Date_frm = Frame(self.Form_main,bg="white")
        Label(self.Date_frm,text="Date of Birth",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.DOB_box = LabelFrame(self.Date_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.DOB_entry = DateEntry(self.DOB_box,textvariable=self.DOB,width=20,background='#00264d',foreground='#ecf0f5',date_pattern="yyyy-mm-dd")
        self.DOB_entry.pack(fill=BOTH,ipady=8)
        self.DOB_box.grid(row=1,column=0,sticky=N+S+W+E)
        Label(self.Date_frm,text="Date of Join",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=1,padx=6,pady=3,sticky=W)
        self.DOJ_box = LabelFrame(self.Date_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.DOJ_entry = DateEntry(self.DOJ_box,textvariable=self.DOJ,width=20,background='#00264d',foreground='#ecf0f5',date_pattern="yyyy-mm-dd")
        self.DOJ_entry.pack(fill=BOTH,ipady=8)
        self.DOJ_box.grid(row=1,column=1,sticky=N+S+W+E,padx=6)
        self.Date_frm.pack(padx=20,anchor=W)

        self.Gender_frm=Frame(self.Form_main,bg="white")
        Label(self.Gender_frm,text="Gender ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Gender_box = LabelFrame(self.Gender_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Gender_entry = ttk.Combobox(self.Gender_box,textvariable = self.Gender,width=25)
        self.Gender_entry["values"]=["Male","Female"]
        self.Gender_entry.pack(fill=BOTH,ipady=8)
        self.Gender_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Gender_frm.pack(padx=20,anchor=W)

        self.Nationality_MT_frm = Frame(self.Form_main,bg="white")
        Label(self.Nationality_MT_frm,text="Nationality ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Nationality_box = LabelFrame(self.Nationality_MT_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Nationality_entry = Entry(self.Nationality_box,textvariable = self.Nationality,bd=0,font=('calibre',10,'normal'))
        self.Nationality_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Nationality_box.grid(row=1,column=0,sticky=N+S+W+E)
        Label(self.Nationality_MT_frm,text="Mother Tongue ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=1,padx=6,pady=3,sticky=W)
        self.MT_box = LabelFrame(self.Nationality_MT_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.MT_entry = Entry(self.MT_box,textvariable = self.MotherTongue,bd=0,font=('calibre',10,'normal'))
        self.MT_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.MT_box.grid(row=1,column=1,padx=6,sticky=N+S+W+E)
        self.Nationality_MT_frm.pack(padx=20,anchor=W)

        self.Course_frm = Frame(self.Form_main,bg="white")
        Label(self.Course_frm,text="2nd Language ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.lang2_box = LabelFrame(self.Course_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.lang2_entry = ttk.Combobox(self.lang2_box,textvariable = self.lang2,width=25)
        self.lang2_entry["values"]=["Tamil","Telugu","Hindi"]
        self.lang2_entry.pack(fill=BOTH,ipady=8)
        self.lang2_box.grid(row=1,column=0,sticky=N+S+W+E)
        Label(self.Course_frm,text="3rd Language ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=1,padx=6,pady=3,sticky=W)
        self.lang3_box = LabelFrame(self.Course_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.lang3_entry = ttk.Combobox(self.lang3_box,textvariable = self.lang3,width=25)
        self.lang3_entry["values"]=["Tamil","Telugu","Hindi"]
        self.lang3_entry.pack(fill=BOTH,ipady=8)
        self.lang3_box.grid(row=1,column=1,padx=6,sticky=N+S+W+E)
        Label(self.Course_frm,text="Stream ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=2,padx=6,pady=3,sticky=W)
        self.Course_box = LabelFrame(self.Course_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Course_entry = ttk.Combobox(self.Course_box,textvariable = self.Course,width=25)
        self.Course_entry["values"]=["Science","Commerce","Humanities"]
        self.Course_entry.pack(fill=BOTH,ipady=8)
        self.Course_box.grid(row=1,column=2,padx=6,sticky=N+S+W+E)
        self.Course_frm.pack(padx=20,anchor=W)

        Label(self.Form_main,text="Parents' Information ",bg="white",font=('Segoe UI Light',20,'normal')).pack(padx=5,pady=15)

        self.father_details = Frame(self.Form_main,bg="white")
        Label(self.father_details,text="Father's Name ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.fathername_box = LabelFrame(self.father_details,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.fathername_entry = Entry(self.fathername_box,bd=0,textvariable = self.fathername ,font=('calibre',10,'normal'))
        self.fathername_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.fathername_box.grid(row=1,column=0,sticky=N+S+W+E)
        Label(self.father_details,text="Father's Mobile Number ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=1,padx=6,pady=3,sticky=W)
        self.fatherno_box = LabelFrame(self.father_details,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.fatherno_entry = Entry(self.fatherno_box,bd=0,textvariable = self.fatherno,font=('calibre',10,'normal'))
        self.fatherno_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.fatherno_box.grid(row=1,column=1,padx=6,sticky=N+S+W+E)
        self.father_details.pack(padx=20,anchor=W)

        self.mother_details = Frame(self.Form_main,bg="white")
        Label(self.mother_details,text="Mother's Name ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.mothername_box = LabelFrame(self.mother_details,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.mothername_entry = Entry(self.mothername_box,bd=0,textvariable = self.mothername ,font=('calibre',10,'normal'))
        self.mothername_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.mothername_box.grid(row=1,column=0,sticky=N+S+W+E)
        Label(self.mother_details,text="Mother's Mobile Number",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=1,padx=6,pady=3,sticky=W)
        self.motherno_box = LabelFrame(self.mother_details,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.motherno_entry = Entry(self.motherno_box,bd=0,textvariable = self.motherno,font=('calibre',10,'normal'))
        self.motherno_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.motherno_box.grid(row=1,column=1,padx=6,sticky=N+S+W+E)
        self.mother_details.pack(padx=20,anchor=W)
        
        self.EMAIL_frm = Frame(self.Form_main,bg="white")
        Label(self.EMAIL_frm,text="Email Address",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Email_box = LabelFrame(self.EMAIL_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Email_Address_entry = Entry(self.Email_box,bd=0,width=60,textvariable = self.Email_Address,font=('calibre',10,'normal'))
        self.Email_Address_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Email_box.grid(row=1,column=0,columnspan=2,sticky=N+S+W+E)
        self.EMAIL_frm.pack(padx=20,anchor=W)

        Label(self.Form_main,text="Residential Information",bg="white",font=('Segoe UI Light',20,'normal')).pack(padx=5,pady=15)

        self.Address_frm = Frame(self.Form_main,bg="white")
        Label(self.Address_frm,text="Residence Address",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.House_box = LabelFrame(self.Address_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.House_Address_text = Text(self.House_box,bd=0,width=40,height=5)
        self.House_Address_text.pack(fill=BOTH,padx=10,ipady=8)
        self.House_box.grid(row=1,column=0,columnspan=2,sticky=N+S+W+E)
        self.Address_frm.pack(padx=20,anchor=W)

        self.button_frm = Frame(self.Form_main,bg="white")
        self.clear = Button(self.button_frm,text="Reset",font=('Segoe UI',11,'normal'),width=12,height=2,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.reset())
        self.clear.grid(row=0,column=0,padx=6,sticky=N+S+W+E)
        self.cancel_btn = Button(self.button_frm,text="Cancel",font=('Segoe UI',11,'normal'),width=12,height=2,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.clear_all())
        self.cancel_btn.grid(row=0,column=0,sticky=N+S+W+E)
        self.submit = Button(self.button_frm,text="Save",font=('Segoe UI',11,'normal'),width=15,height=2,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.Submit())
        self.submit.grid(row=0,column=1,padx=6,sticky=N+S+W+E)
        self.button_frm.pack(padx=20,pady=10,anchor=E)

        Canvas(self.Form_main,height=80,bg="#ecf0f5",borderwidth=0).pack(fill=X,ipadx=150)
        self.Form_canvas.pack(fill=Y,side=LEFT,expand=True,anchor="center",ipadx=150)
        self.scroll.pack( side = RIGHT, fill = Y )

        self.Class_DD.bind("<<ComboboxSelected>>", lambda event: self.EnableDisableFields())

    def clear_all(self):
        self.Adm_entry.delete(0,END)
        self.F_Name_entry.delete(0,END)
        self.L_Name_entry.delete(0,END)
        self.EMIS_entry.delete(0,END)
        self.Class_DD.delete(0,END)
        self.Section_DD.delete(0,END)
        self.DOB_entry.delete(0,END)
        self.DOJ_entry.delete(0,END)
        self.Nationality_entry.delete(0,END)
        self.MT_entry.delete(0,END)
        self.lang2_entry.delete(0,END)
        self.lang3_entry.delete(0,END)
        self.Course_entry.delete(0,END)
        self.fathername_entry.delete(0,END)
        self.fatherno_entry.delete(0,END)
        self.mothername_entry.delete(0,END)
        self.motherno_entry.delete(0,END)
        self.Email_Address_entry.delete(0,END)
        self.Adm_entry.configure(state="normal")
        self.House_Address_text.delete("1.0",END)
        self.lang2_entry.config(state="normal")
        self.lang3_entry.config(state="normal")
        self.Course_entry.config(state='normal')

    def check_adm(self):
        self.Adm_entry.configure(state="disabled")
        self.result=[]
        mycur.execute("SELECT * FROM LKG_UKG WHERE ADMNO = {}".format(self.Admno.get()))
        self.result.extend(mycur.fetchall())
        mycur.execute("SELECT * FROM I_VIII WHERE ADMNO = {}".format(self.Admno.get()))
        self.result.extend(mycur.fetchall())
        mycur.execute("SELECT * FROM IX_X WHERE ADMNO = {}".format(self.Admno.get()))
        self.result.extend(mycur.fetchall())
        mycur.execute("SELECT * FROM XI_XII WHERE ADMNO = {}".format(self.Admno.get()))
        self.result.extend(mycur.fetchall())

        if self.result == []:
            messagebox.showerror("DataHive","Admission Number does not exist")
        else:
            self.reset()
    
    def reset(self):
        
        self.F_Name.set(self.result[0][1])
        self.L_Name.set(self.result[0][2])
        self.EMIS.set(self.result[0][3])
        self.Class.set(self.result[0][4])
        self.Section.set(self.result[0][5])
        self.DOB.set(self.result[0][6])
        self.DOJ.set(self.result[0][7])
        self.Gender.set(self.result[0][8])
        self.Nationality.set(self.result[0][9])
        self.MotherTongue.set(self.result[0][10])

        if self.result[0][4] in ["I","II","III","IV","V","VI","VII","VIII"]:
            self.lang2_entry.config(state="normal")
            self.lang2.set(self.result[0][11])
            self.lang3_entry.config(state="normal")
            self.lang3.set(self.result[0][12])
            self.Course_entry.config(state='disabled')
            self.fathername.set(self.result[0][13])
            self.fatherno.set(self.result[0][14])
            self.mothername.set(self.result[0][15])
            self.motherno.set(self.result[0][16])
            self.Email_Address.set(self.result[0][17])
            self.House_Address_text.delete("1.0",END)
            self.House_Address_text.insert("1.0",self.result[0][18])

        elif self.result[0][4] in ["X","IX"]:
            self.lang2_entry.config(state="normal")
            self.lang2.set(self.result[0][11])
            self.lang3_entry.config(state="disabled")
            self.Course_entry.config(state='disabled')
            self.fathername.set(self.result[0][12])
            self.fatherno.set(self.result[0][13])
            self.mothername.set(self.result[0][14])
            self.motherno.set(self.result[0][15])
            self.Email_Address.set(self.result[0][16])
            self.House_Address_text.delete("1.0",END)
            self.House_Address_text.insert("1.0",self.result[0][17])

        elif self.result[0][4] in ["XI","XII"]:
            self.lang2_entry.config(state="disabled")
            self.lang3_entry.config(state="disabled")
            self.Course_entry.config(state='normal')
            self.Course.set(self.result[0][11])
            self.fathername.set(self.result[0][12])
            self.fatherno.set(self.result[0][13])
            self.mothername.set(self.result[0][14])
            self.motherno.set(self.result[0][15])
            self.Email_Address.set(self.result[0][16])
            self.House_Address_text.delete("1.0",END)
            self.House_Address_text.insert("1.0",self.result[0][17])

        elif self.result[0][4] in ["LKG","UKG"]:
            self.lang2_entry.config(state="disabled")
            self.lang3_entry.config(state="disabled")
            self.Course_entry.config(state='disabled')
            self.fathername.set(self.result[0][11])
            self.fatherno.set(self.result[0][12])
            self.mothername.set(self.result[0][13])
            self.motherno.set(self.result[0][14])
            self.Email_Address.set(self.result[0][15])
            self.House_Address_text.delete("1.0",END)
            self.House_Address_text.insert("1.0",self.result[0][16])

    def EnableDisableFields(self):
        if self.Class.get() in ["I","II","III","IV","V","VI","VII","VIII"]:
            self.lang2_entry.config(state="normal")
            self.lang3_entry.config(state="normal")
            self.Course_entry.config(state='disabled')

        elif self.Class.get() in ["X","IX"]:
            self.lang2_entry.config(state="normal")
            self.lang3_entry.config(state="disabled")
            self.Course_entry.config(state='disabled')

        elif self.Class.get() in ["XI","XII"]:
            self.lang2_entry.config(state="disabled")
            self.lang3_entry.config(state="disabled")
            self.Course_entry.config(state='normal')

        elif self.Class.get() in ["LKG","UKG"]:
            self.lang2_entry.config(state="disabled")
            self.lang3_entry.config(state="disabled")
            self.Course_entry.config(state='disabled')
    
    def Submit(self):
        if self.Admno.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Admission Number")
        elif self.F_Name.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter First Name")
        elif self.L_Name.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Last Name")
        elif self.EMIS.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter EMIS Number")
        elif len(self.EMIS.get()) != 16:
            messagebox.showerror("DATAHIVE","Please Enter a 12 digit EMIS Number")
        elif not self.EMIS.get().isdigit():
            messagebox.showerror("DATAHIVE","Enter a Valid EMIS Number")
        elif self.Class.get() == "":
            messagebox.showerror("DATAHIVE","Please Select the Class")
        elif self.Section.get() == "":
            messagebox.showerror("DATAHIVE","Please Select the Section")
        elif self.DOB.get() == "":
            messagebox.showerror("DATAHIVE","Please Select Date of Birth")
        elif self.DOJ.get() == "":
            messagebox.showerror("DATAHIVE","Please Select Date of Joining")
        elif self.Nationality.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Nationality")
        elif self.MotherTongue.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Mother Tongue")
        elif self.fathername.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Father's Name")
        elif self.fatherno.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Father's Mobile Number")
        elif not self.fatherno.get().isdigit() and len(self.fatherno.get())==10:
            messagebox.showerror("DATAHIVE","Father's Mobile Number is InValid")
        elif self.mothername.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Mother's Name")
        elif self.motherno.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Mother's Mobile Number")
        elif not self.motherno.get().isdigit() and len(self.motherno.get())==10:
            messagebox.showerror("DATAHIVE","Mother's Mobile Number is InValid")
        elif self.Email_Address.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Email Address")
        elif ".com" not in self.Email_Address.get() or "@" not in self.Email_Address.get():
            messagebox.showerror("DATAHIVE","Enter a Valid Email Address")
        elif self.House_Address_text.get("1.0",END) == "":
            messagebox.showerror("DATAHIVE","Please Enter Residential Address")
        elif self.Class.get() in ["I","II","III","IV","V","VI","VII","VIII"]:
            if self.lang2.get() == "":
                messagebox.showerror("DATAHIVE","Please Choose 2nd Language")
            elif self.lang3.get() == "":
                messagebox.showerror("DATAHIVE","Please Choose 3nd Language")
            else:
                l=[self.Admno.get(), self.F_Name.get(), self.L_Name.get(), self.EMIS.get(), self.Class.get(), self.Section.get(), self.DOB.get(), self.DOJ.get(),self.Gender.get() , self.Nationality.get(), self.MotherTongue.get(), self.lang2.get(), self.lang3.get(), self.fathername.get(), self.fatherno.get(), self.mothername.get(), self.motherno.get(), self.Email_Address.get(), self.House_Address_text.get("1.0",END)]
            print(l)
            mycur.execute('DELETE FROM LKG_UKG WHERE ADMNO = {}'.format(self.Admno.get()))
            mycur.execute('DELETE FROM I_VIII WHERE ADMNO = {}'.format(self.Admno.get()))
            mycur.execute('DELETE FROM IX_X WHERE ADMNO = {}'.format(self.Admno.get()))
            mycur.execute('DELETE FROM XI_XII WHERE ADMNO = {}'.format(self.Admno.get()))
            mycur.execute("INSERT INTO i_viii VALUES({},'{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{},'{}',{},'{}','{}')".format(*l))
            mydb.commit()
        elif self.Class.get() in ["IX","X"]:
            if self.lang2.get() == "":
                messagebox.showerror("DATAHIVE","Please Choose 2nd Language")
            else:
                l=[self.Admno.get(), self.F_Name.get(), self.L_Name.get(), self.EMIS.get(), self.Class.get(), self.Section.get(), self.DOB.get(), self.DOJ.get(),self.Gender.get() , self.Nationality.get(), self.MotherTongue.get(), self.lang2.get(), self.fathername.get(), self.fatherno.get(), self.mothername.get(), self.motherno.get(), self.Email_Address.get(), self.House_Address_text.get("1.0",END)]
            mycur.execute('DELETE FROM LKG_UKG WHERE ADMNO = {}'.format(self.Admno.get()))
            mycur.execute('DELETE FROM I_VIII WHERE ADMNO = {}'.format(self.Admno.get()))
            mycur.execute('DELETE FROM IX_X WHERE ADMNO = {}'.format(self.Admno.get()))
            mycur.execute('DELETE FROM XI_XII WHERE ADMNO = {}'.format(self.Admno.get()))
            mycur.execute("INSERT INTO ix_x VALUES({},'{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}',{},'{}',{},'{}','{}')".format(*l))
            mydb.commit()
        elif self.Class.get() in ["XI","XII"]:
            if self.Course.get() == "":
                messagebox.showerror("DATAHIVE","Please Choose Stream")
            else:
                l=[self.Admno.get(), self.F_Name.get(), self.L_Name.get(), self.EMIS.get(), self.Class.get(), self.Section.get(), self.DOB.get(), self.DOJ.get(),self.Gender.get() , self.Nationality.get(), self.MotherTongue.get(), self.Course.get(), self.fathername.get(), self.fatherno.get(), self.mothername.get(), self.motherno.get(), self.Email_Address.get(), self.House_Address_text.get("1.0",END)]
            mycur.execute('DELETE FROM LKG_UKG WHERE ADMNO = {}'.format(self.Admno.get()))
            mycur.execute('DELETE FROM I_VIII WHERE ADMNO = {}'.format(self.Admno.get()))
            mycur.execute('DELETE FROM IX_X WHERE ADMNO = {}'.format(self.Admno.get()))
            mycur.execute('DELETE FROM XI_XII WHERE ADMNO = {}'.format(self.Admno.get()))
            mycur.execute("INSERT INTO xi_xii VALUES({},'{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}',{},'{}',{},'{}','{}')".format(*l))
            mydb.commit()
        elif self.Class.get() in ["LKG","UKG"]:
            l=[self.Admno.get(), self.F_Name.get(), self.L_Name.get(), self.EMIS.get(), self.Class.get(), self.Section.get(), self.DOB.get(), self.DOJ.get(),self.Gender.get() , self.Nationality.get(), self.MotherTongue.get(), self.fathername.get(), self.fatherno.get(), self.mothername.get(), self.motherno.get(), self.Email_Address.get(), self.House_Address_text.get("1.0",END)]
            mycur.execute('DELETE FROM LKG_UKG WHERE ADMNO = {}'.format(self.Admno.get()))
            mycur.execute('DELETE FROM I_VIII WHERE ADMNO = {}'.format(self.Admno.get()))
            mycur.execute('DELETE FROM IX_X WHERE ADMNO = {}'.format(self.Admno.get()))
            mycur.execute('DELETE FROM XI_XII WHERE ADMNO = {}'.format(self.Admno.get()))
            mycur.execute("INSERT INTO LKG_UKG VALUES({},'{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}',{},'{}',{},'{}','{}')".format(*l))
            mydb.commit()
        messagebox.showinfo("DATAHIVE","Student details Modified")
        self.clear_all()

class delete_student(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(background="#ecf0f5")

        self.checked = PhotoImage(file="icons\\checked.png")
        self.unchecked = PhotoImage(file="icons\\unchecked.png")

        self.filter_value = StringVar() 

        self.search_box=Frame(self)
        
        self.search_bar=Frame(self.search_box,background="#ecf0f5")
        self.searchbox = Entry(self.search_bar,bd=0,highlightthickness=1,highlightbackground="#4da6ff")
        self.searchbox.pack(side=LEFT,fill=BOTH,expand=True)
        self.search_ico = PhotoImage(file = "icons\\search.png")
        self.search_btn=Button(self.search_bar,image=self.search_ico,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white")
        self.search_btn.img = self.search_ico
        self.search_btn.pack(side=RIGHT)
        self.search_bar.pack(fill=X)

        Button(self.search_box,text="Refresh",bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: update_table_with_checks(self.table,"student")).pack(pady=5,anchor=E)

        self.search_box.pack(fill=X,padx=8,pady=4)

        self.search_table = Frame(self)

        self.y_scroll = Scrollbar(self.search_table)
        self.y_scroll.pack( side = RIGHT, fill = BOTH )
        self.x_scroll = Scrollbar(self.search_table,orient="horizontal")
        self.x_scroll.pack( side = BOTTOM, fill = BOTH )

        self.table = ttk.Treeview(self.search_table, yscrollcommand = self.y_scroll.set, xscrollcommand = self.x_scroll.set)
        self.style = ttk.Style(self.table)
        self.style.configure("Treeview",rowheight=30)
        self.table["columns"]=("Admno","FName","LName","EMIS","Class","Section","DOB","DOJ","Gender","Nationality","MT","lang2","lang3","Course","fathername","fatherno","mothername","motherno","email","address")
        self.table.pack(side=LEFT,fill=BOTH)
        self.table.heading("Admno", text="Admission Number")
        self.table.heading("FName", text="First Name")
        self.table.heading("LName", text="Last Name")
        self.table.heading("EMIS", text="EMIS")
        self.table.heading("Class", text="Class")
        self.table.heading("Section", text="Section")
        self.table.heading("DOB", text="Date of Birth")
        self.table.heading("DOJ", text="Date of Joining")
        self.table.heading("Gender", text="Gender")
        self.table.heading("Nationality", text="Nationality")
        self.table.heading("MT", text="Mother Tongue")
        self.table.heading("lang2", text="2nd Language")
        self.table.heading("lang3", text="3rd Language")
        self.table.heading("Course", text="Course")
        self.table.heading("fathername", text="Father's Name")
        self.table.heading("fatherno", text="Father's Mobile Number")
        self.table.heading("mothername", text="Mother's Name")
        self.table.heading("motherno", text="Mother's Mobile Number")
        self.table.heading("email", text="EMail Address")
        self.table.heading("address", text="Residential Address")
        
        self.table.tag_configure("checked",image=self.checked)
        self.table.tag_configure("unchecked",image=self.unchecked)
        self.table.bind("<Button 1>",lambda event: self.toggleCheck(event))

        self.y_scroll.config( command = self.table.yview )
        self.x_scroll.config( command = self.table.xview )
        self.y_scroll.set(0,1)
        self.x_scroll.set(0,1)

        self.search_table.pack(anchor="center",fill=BOTH,padx=8,pady=4,expand=True)

        self.delete_btn = Button(self,text="Delete",font=('Segoe UI',11,'normal'),width=10,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=self.delete_rows)
        self.delete_btn.pack(anchor='e',padx=8,pady=4)

        update_table_with_checks(self.table,"student")

    def toggleCheck(self,event):
        rowid = self.table.identify_row(event.y)
        try:
            tag = self.table.item(rowid, "tags")[0]
            tags = list(self.table.item(rowid,"tags"))
            tags.remove(tag)
            self.table.item(rowid, tags=tags)
            if tag == "checked":
                self.table.item(rowid, tags="unchecked")
            else:
                self.table.item(rowid, tags="checked")
        except:
            pass
        
    def delete_rows(self):
        for i in self.table.get_children():
            if self.table.item(i,"tags")[0] == "checked":
                print(self.table.item(i,"values")[0],self.table.item(i,"values")[4])
                if self.table.item(i,"values")[4] in ["I","II","III","IV","V","VI","VII","VIII"]:
                    mycur.execute('DELETE FROM I_VIII WHERE ADMNO = {}'.format(self.table.item(i,"values")[0]))
                elif self.table.item(i,"values")[4] in ["X","IX"]:
                    mycur.execute('DELETE FROM IX_X WHERE ADMNO = {}'.format(self.table.item(i,"values")[0]))
                elif self.table.item(i,"values")[4] in ["XI","XII"]:
                    mycur.execute('DELETE FROM XI_XII WHERE ADMNO = {}'.format(self.table.item(i,"values")[0]))
                elif self.table.item(i,"values")[4] in ["LKG","UKG"]:
                    mycur.execute('DELETE FROM LKG_UKG WHERE ADMNO = {}'.format(self.table.item(i,"values")[0]))
        mydb.commit()
        update_table_with_checks(self.table,"student")
        update_dash()
        messagebox.showinfo("DATAHIVE","Deleted Successfully")

class search_student(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(background="#ecf0f5")

        self.SEARCH = StringVar()
        self.search_box=Frame(self)
        
        self.search_bar=Frame(self.search_box,background="#ecf0f5")
        self.searchbox = Entry(self.search_bar,bd=0,highlightthickness=1,highlightbackground="#4da6ff",textvariable=self.SEARCH)
        self.searchbox.pack(side=LEFT,fill=BOTH,expand=True)
        self.search_ico = PhotoImage(file = "icons\\search.png")
        self.search_btn=Button(self.search_bar,image=self.search_ico,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.search_tbl())
        self.search_btn.img = self.search_ico
        self.search_btn.pack(side=RIGHT)
        self.search_bar.pack(fill=X)

        Button(self.search_box,text="Refresh",bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.update_table()).pack(pady=5,anchor=E)

        self.search_box.pack(fill=X,padx=8,pady=4)

        self.search_table = Frame(self)

        self.y_scroll = Scrollbar(self.search_table)
        self.y_scroll.pack( side = RIGHT, fill = BOTH )
        self.x_scroll = Scrollbar(self.search_table,orient="horizontal")
        self.x_scroll.pack( side = BOTTOM, fill = BOTH )

        self.table = ttk.Treeview(self.search_table, show="headings", yscrollcommand = self.y_scroll.set, xscrollcommand = self.x_scroll.set)
        self.table["columns"]=("Admno","FName","LName","EMIS","Class","Section","DOB","DOJ","Gender","Nationality","MT","lang2","lang3","Course","fathername","fatherno","mothername","motherno","email","address")
        self.table.pack(side=LEFT,fill=BOTH)
        self.table.heading("Admno", text="Admission Number")
        self.table.heading("FName", text="First Name")
        self.table.heading("LName", text="Last Name")
        self.table.heading("EMIS", text="EMIS")
        self.table.heading("Class", text="Class")
        self.table.heading("Section", text="Section")
        self.table.heading("DOB", text="Date of Birth")
        self.table.heading("DOJ", text="Date of Joining")
        self.table.heading("Gender", text="Gender")
        self.table.heading("Nationality", text="Nationality")
        self.table.heading("MT", text="Mother Tongue")
        self.table.heading("lang2", text="2nd Language")
        self.table.heading("lang3", text="3rd Language")
        self.table.heading("Course", text="Course")
        self.table.heading("fathername", text="Father's Name")
        self.table.heading("fatherno", text="Father's Mobile Number")
        self.table.heading("mothername", text="Mother's Name")
        self.table.heading("motherno", text="Mother's Mobile Number")
        self.table.heading("email", text="EMail Address")
        self.table.heading("address", text="Residential Address")

        self.y_scroll.config( command = self.table.yview )
        self.x_scroll.config( command = self.table.xview )
        self.y_scroll.set(0,1)
        self.x_scroll.set(0,1)

        self.search_table.pack(anchor="center",fill=BOTH,padx=8,pady=4,expand=True)
        self.update_table()

    def search_tbl(self):
        sdata=[]
        mycur.execute("SELECT * FROM lkg_ukg where (admno like '%{}%') or (fname like '%{}%') or (lname like '%{}%')".format(self.SEARCH.get(),self.SEARCH.get(),self.SEARCH.get()))
        for i in mycur.fetchall():
            i=i[0:len(i)-6]+("-","-","-")+i[len(i)-6:]
            sdata.append(i)
        mycur.execute("SELECT * FROM i_viii where (admno like '%{}%') or (fname like '%{}%') or (lname like '%{}%')".format(self.SEARCH.get(),self.SEARCH.get(),self.SEARCH.get()))
        for i in mycur.fetchall():
            i=i[0:len(i)-6]+("-",)+i[len(i)-6:]
            sdata.append(i)
        mycur.execute("SELECT * FROM ix_x where (admno like '%{}%') or (fname like '%{}%') or (lname like '%{}%')".format(self.SEARCH.get(),self.SEARCH.get(),self.SEARCH.get()))
        for i in mycur.fetchall():
            i=i[0:len(i)-6]+("-","-")+i[len(i)-6:]
            sdata.append(i)
        mycur.execute("SELECT * FROM xi_xii where (admno like '%{}%') or (fname like '%{}%') or (lname like '%{}%')".format(self.SEARCH.get(),self.SEARCH.get(),self.SEARCH.get()))
        for i in mycur.fetchall():
            i=i[0:len(i)-7]+("-","-")+i[len(i)-7:]
            sdata.append(i)
        sdata.sort()
        try:
            self.table.delete(*self.table.get_children())
        except:
            pass
        for i in sdata:
            self.table.insert('','end',values=i)

    def update_table(self):
        try:
            self.table.delete(*self.table.get_children())
        except:
            pass
        for i in student_data():
            self.table.insert('','end',values=i)

#teachers
class teachers(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(background="#ecf0f5")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        tea_add=PhotoImage(file = "icons\\teacher-add-100.png")
        add=Button(self,image=tea_add,width=400,height=200,text="                 ADD",font=('Segoe UI', 30),bg="#443085",bd=0,activebackground="#000817",compound ='left',command=lambda: controller.show_frame(add_new_teacher))
        add.image=tea_add
        add.grid(row=0,column=0,sticky=N+S+E+W,padx=10,pady=10)

        tea_modify=PhotoImage(file = "icons\\teacher-modify-100.png")
        modify=Button(self,image=tea_modify,width=400,height=200,text="           MODIFY",font=('Segoe UI', 30),bg="#f39c12",bd=0,activebackground="#000817",compound ='left',command=lambda: controller.show_frame(modify_teacher_details))
        modify.image=tea_modify
        modify.grid(row=0,column=1,sticky=N+S+E+W,padx=10,pady=10)

        tea_search=PhotoImage(file = "icons\\teacher-search-100.png")
        search=Button(self,image=tea_search,width=400,height=200,text="           SEARCH",font=('Segoe UI', 30),bg="#00a65a",bd=0,activebackground="#000817",compound ='left',command=lambda: controller.show_frame(search_teacher))
        search.image=tea_search
        search.grid(row=1,column=0,sticky=N+S+E+W,padx=10,pady=10)

        tea_delete=PhotoImage(file = "icons\\teacher-delete-100.png")
        delete=Button(self,image=tea_delete,width=400,height=200,text="             DELETE",font=('Segoe UI', 30),bg="#f56954",bd=0,activebackground="#000817",compound ='left',command=lambda: controller.show_frame(delete_teacher))
        delete.image=tea_delete
        delete.grid(row=1,column=1,sticky=N+S+E+W,padx=10,pady=10)        

class add_new_teacher(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(background="#ecf0f5")

        self.s=ttk.Style()
        self.s.theme_use("vista")

        self.Empno=StringVar()
        self.F_Name=StringVar()
        self.L_Name=StringVar()
        self.Qualification=StringVar()
        self.Designation=StringVar()
        self.Subject=StringVar()
        self.Class=StringVar()
        self.Section=StringVar()
        self.DOB=StringVar()
        self.DOJ=StringVar()
        self.Gender=StringVar()
        self.Aadhar=StringVar()
        self.PAN=StringVar()
        self.mobile=StringVar()
        self.Email_Address=StringVar()
        
        self.Form_canvas=Canvas(self,background="#ecf0f5")
        self.scroll=ttk.Scrollbar(self,command = self.Form_canvas.yview)
        self.Form_main=Frame(self.Form_canvas,bg="white",bd=0)
        self.Form_main.bind("<Configure>",lambda e: self.Form_canvas.configure(scrollregion=self.Form_canvas.bbox("all")))
        self.Scroll_Form = self.Form_canvas.create_window(0,0, window=self.Form_main,anchor="nw")
        self.Form_canvas.config(yscrollcommand = self.scroll.set)

        Canvas(self.Form_main,height=80,bg="#ecf0f5",borderwidth=0).pack(fill=X,ipadx=150)

        Label(self.Form_main,text="Teacher's Information",bg="white",font=('Segoe UI Light',20,'normal')).pack(padx=5,pady=15)

        self.Empno_frm=Frame(self.Form_main,bg="white")
        Label(self.Empno_frm,text="Employee Number",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Empno_entry_box = LabelFrame(self.Empno_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Empno_entry = Entry(self.Empno_entry_box,textvariable = self.Empno,bd=0,font=('Segoe UI', 11))
        self.Empno_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Empno_entry_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Empno_frm.pack(padx=20,anchor=W)
        
        self.Name_frm = Frame(self.Form_main,bg="white")
        Label(self.Name_frm,text="Name",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.F_Name_entry_box = LabelFrame(self.Name_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.F_Name_entry = Entry(self.F_Name_entry_box,textvariable = self.F_Name,bd=0,font=('Segoe UI', 11))
        self.F_Name_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.F_Name_entry_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.L_Name_entry_box = LabelFrame(self.Name_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.L_Name_entry = Entry(self.L_Name_entry_box,textvariable = self.L_Name,bd=0,font=('Segoe UI', 11))
        self.L_Name_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.L_Name_entry_box.grid(row=1,column=1,padx=6,sticky=N+S+W+E)
        Label(self.Name_frm,text="First Name ",bg="white",font=('Segoe UI',10,'normal')).grid(row=2,column=0,sticky=W)
        Label(self.Name_frm,text="Last Name ",bg="white",font=('Segoe UI',10,'normal')).grid(row=2,column=1,sticky=W,padx=6)
        self.Name_frm.pack(padx=20,anchor=W)

        self.Qualification_frm = Frame(self.Form_main,bg="white")
        Label(self.Qualification_frm,text="Qualification ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Qualification_entry_box = LabelFrame(self.Qualification_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Qualification_entry = Entry(self.Qualification_entry_box,textvariable = self.Qualification,bd=0,font=('calibre',10,'normal'))
        self.Qualification_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Qualification_entry_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Qualification_frm.pack(padx=20,anchor=W)

        self.Desig_frm = Frame(self.Form_main,bg="white")
        Label(self.Desig_frm,text="Designation ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Desig_box = LabelFrame(self.Desig_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Desig_entry = ttk.Combobox(self.Desig_box,textvariable = self.Designation,width=25)
        self.Desig_entry["values"]=["PGT - Post Graduate Teacher","TGT - Trained Graduate Teacher","PRT - Primary Teacher","PET - Physical Education Teacher"]
        self.Desig_entry.pack(fill=BOTH,ipady=8)
        self.Desig_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Desig_frm.pack(padx=20,anchor=W)

        self.Subject_frm=Frame(self.Form_main,bg="white")
        Label(self.Subject_frm,text="Subject ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Subject_box = LabelFrame(self.Subject_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Subject_entry = ttk.Combobox(self.Subject_box,textvariable = self.Subject,width=25)
        self.Subject_entry["values"]=["English","Tamil","Hindi","Social Science","Science", "Physics","Biology", "Chemistry","Maths",
                                      "Sanskrit", "Computer Science", "Commerce", "Accounts", "Buisness Studies", "Engineering Graphics",
                                      "Physical Education", "Art"]
        self.Subject_entry.pack(fill=BOTH,ipady=8)
        self.Subject_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Subject_frm.pack(padx=20,anchor=W)

        self.CT_frm = Frame(self.Form_main,bg="white")
        Label(self.CT_frm,text="Whether Class Teacher ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.CT_box = LabelFrame(self.CT_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.CT_entry = ttk.Combobox(self.CT_box,width=25)
        self.CT_entry["values"]=["Yes","No"]
        self.CT_entry.pack(fill=BOTH,ipady=8)
        self.CT_box.grid(row=1,column=0,sticky=N+S+W+E)
        Label(self.CT_frm,text="Class ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=1,pady=3,padx=6,sticky=W)
        self.Class_DD_box = LabelFrame(self.CT_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Class_DD = ttk.Combobox(self.Class_DD_box,textvariable = self.Class)
        
        self.Class_DD.pack(fill=BOTH,ipady=8)
        self.Class_DD_box.grid(row=1,column=1,padx=6,sticky=N+S+W+E)
        Label(self.CT_frm,text="Section ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=2,pady=3,sticky=W)
        self.Section_DD_box = LabelFrame(self.CT_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Section_DD = ttk.Combobox(self.Section_DD_box,textvariable = self.Section)
        
        self.Section_DD.pack(fill=BOTH,ipady=8)
        self.Section_DD_box.grid(row=1,column=2,sticky=N+S+W+E)
        self.CT_frm.pack(padx=20,anchor=W)

        self.Date_frm = Frame(self.Form_main,bg="white")
        Label(self.Date_frm,text="Date of Birth",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.DOB_box = LabelFrame(self.Date_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.DOB_entry = DateEntry(self.DOB_box,textvariable=self.DOB,width=20,background='#00264d',foreground='#ecf0f5',date_pattern="yyyy-mm-dd")
        self.DOB_entry.pack(fill=BOTH,ipady=8)
        self.DOB_box.grid(row=1,column=0,sticky=N+S+W+E)
        Label(self.Date_frm,text="Date of Join",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=1,padx=6,pady=3,sticky=W)
        self.DOJ_box = LabelFrame(self.Date_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.DOJ_entry = DateEntry(self.DOJ_box,textvariable=self.DOJ,width=20,background='#00264d',foreground='#ecf0f5',date_pattern="yyyy-mm-dd")
        self.DOJ_entry.pack(fill=BOTH,ipady=8)
        self.DOJ_box.grid(row=1,column=1,sticky=N+S+W+E,padx=6)
        self.Date_frm.pack(padx=20,anchor=W)

        self.Gender_frm=Frame(self.Form_main,bg="white")
        Label(self.Gender_frm,text="Gender ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Gender_box = LabelFrame(self.Gender_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Gender_entry = ttk.Combobox(self.Gender_box,textvariable = self.Gender,width=25)
        self.Gender_entry["values"]=["Male","Female"]
        self.Gender_entry.pack(fill=BOTH,ipady=8)
        self.Gender_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Gender_frm.pack(padx=20,anchor=W)

        self.Aadhar_frm = Frame(self.Form_main,bg="white")
        Label(self.Aadhar_frm,text="Aadhar Number ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Aadhar_box = LabelFrame(self.Aadhar_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Aadhar_entry = Entry(self.Aadhar_box,textvariable = self.Aadhar,bd=0,font=('calibre',10,'normal'))
        self.Aadhar_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Aadhar.trace("w", lambda name, index, mode, sv=self.Aadhar, entry=self.Aadhar_entry: self.aadhar_entry_ch(sv,entry))
        self.Aadhar_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Aadhar_frm.pack(padx=20,anchor=W)

        self.PAN_frm = Frame(self.Form_main,bg="white")
        Label(self.PAN_frm,text="PAN",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.PAN_box = LabelFrame(self.PAN_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.PAN_entry = Entry(self.PAN_box,textvariable = self.PAN,bd=0,font=('calibre',10,'normal'))
        self.PAN_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.PAN_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.PAN_frm.pack(padx=20,anchor=W)
        self.PAN_frm.pack(padx=20,anchor=W)

        Label(self.Form_main,text="Contact Information ",bg="white",font=('Segoe UI Light',20,'normal')).pack(padx=5,pady=15)

        self.Mobile_details = Frame(self.Form_main,bg="white")
        Label(self.Mobile_details,text="Mobile Number",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,padx=6,pady=3,sticky=W)
        self.Mobileno_box = LabelFrame(self.Mobile_details,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Mobileno_entry = Entry(self.Mobileno_box,bd=0,textvariable = self.mobile,font=('calibre',10,'normal'))
        self.Mobileno_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Mobileno_box.grid(row=1,column=0,padx=6,sticky=N+S+W+E)
        self.Mobile_details.pack(padx=20,anchor=W)
        
        self.EMAIL_frm = Frame(self.Form_main,bg="white")
        Label(self.EMAIL_frm,text="Email Address",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Email_box = LabelFrame(self.EMAIL_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Email_Address_entry = Entry(self.Email_box,bd=0,width=60,textvariable = self.Email_Address,font=('calibre',10,'normal'))
        self.Email_Address_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Email_box.grid(row=1,column=0,columnspan=2,sticky=N+S+W+E)
        self.EMAIL_frm.pack(padx=20,anchor=W)

        self.Address_frm = Frame(self.Form_main,bg="white")
        Label(self.Address_frm,text="Residence Address",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.House_box = LabelFrame(self.Address_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.House_Address_text = Text(self.House_box,bd=0,width=40,height=5)
        self.House_Address_text.pack(fill=BOTH,padx=10,ipady=8)
        self.House_box.grid(row=1,column=0,columnspan=2,sticky=N+S+W+E)
        self.Address_frm.pack(padx=20,anchor=W)

        self.button_frm = Frame(self.Form_main,bg="white")
        self.clear = Button(self.button_frm,text="Clear",font=('Segoe UI',11,'normal'),width=12,height=2,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.clear_all())
        self.clear.grid(row=0,column=0,sticky=N+S+W+E)
        self.submit = Button(self.button_frm,text="Submit",font=('Segoe UI',11,'normal'),width=15,height=2,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.Submit())
        self.submit.grid(row=0,column=1,padx=6,sticky=N+S+W+E)
        self.button_frm.pack(padx=20,pady=10,anchor=E)

        Canvas(self.Form_main,height=80,bg="#ecf0f5",borderwidth=0).pack(fill=X,ipadx=150)
        self.Form_canvas.pack(fill=Y,side=LEFT,expand=True,anchor="center",ipadx=150)
        self.scroll.pack( side = RIGHT, fill = Y )

        self.clear_all()
        self.CT_entry.bind("<<ComboboxSelected>>", lambda event: self.EnableDisableFields())

    def aadhar_entry_ch(self,sv,entry):
        i=entry.index(END)
        if sv.get() == "":
            pass
        elif sv.get()[-1] == "-":
            pass
        elif i in [5,10]:
            entry.insert(i-1,"-")
        elif i >= 14:
            entry.delete(14,END)

    def clear_all(self):
        self.Empno_entry.delete(0,END)
        self.F_Name_entry.delete(0,END)
        self.L_Name_entry.delete(0,END)
        self.Qualification_entry.delete(0,END)
        self.Class_DD.delete(0,END)
        self.Section_DD.delete(0,END)
        self.DOB_entry.delete(0,END)
        self.DOJ_entry.delete(0,END)
        self.Desig_entry.delete(0,END)
        self.Subject_entry.delete(0,END)
        self.CT_entry.delete(0,END)
        self.Gender_entry.delete(0,END)
        self.Aadhar_entry.delete(0,END)
        self.PAN_entry.delete(0,END)
        self.Mobileno_entry.delete(0,END)
        self.Email_Address_entry.delete(0,END)
        self.House_Address_text.delete("1.0",END)
        self.Class_DD.config(state="normal")
        self.Class_DD["values"]=[]
        self.Section_DD.config(state="normal")
        self.Section_DD["values"]=[]

    def EnableDisableFields(self):
        if self.CT_entry.get() == "Yes":
            self.Class_DD.config(state="normal")
            self.Class_DD["values"]=["LKG","UKG","I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"]
            self.Section_DD.config(state="normal")
            self.Section_DD["values"]=["A","B","C","D","E"]
        else:
            self.Class_DD.config(state="disabled")
            self.Section_DD.config(state='disabled')

    def Submit(self):
        for i in teacher_data():
            if int(self.Empno.get()) == i[0]:
                messagebox.showerror("DATAHIVE","Employee with this Employee Number is Already Available")
                break
        else:
            if self.Empno.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Employee Number")
            elif self.F_Name.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter First Name")
            elif self.L_Name.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Last Name")
            elif self.Qualification.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Qualification")
            elif self.Designation.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Designation")
            elif self.Subject.get() == "":
                messagebox.showerror("DATAHIVE","Please Select Subject")
            elif self.CT_entry.get() == "":
                messagebox.showerror("DATAHIVE","Please Select Whether Class Teacher")
            elif self.CT_entry.get() == "Yes" and self.Class.get() == "":
                messagebox.showerror("DATAHIVE","Please Select the Class")
            elif self.CT_entry.get() == "Yes" and self.Section.get() == "":
                messagebox.showerror("DATAHIVE","Please Select the Section")
            elif self.DOB.get() == "":
                messagebox.showerror("DATAHIVE","Please Select Date of Birth")
            elif self.DOJ.get() == "":
                messagebox.showerror("DATAHIVE","Please Select Date of Joining")
            elif self.Gender.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Gender")
            elif self.Aadhar.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Aadhar Number")
            elif len(self.Aadhar.get().replace("-","")) != 12:
                messagebox.showerror("DATAHIVE","Please Enter a 12 digit Aadhar Number")
            elif not self.Aadhar.get().replace("-","").isdigit():
                messagebox.showerror("DATAHIVE","Enter a Valid Aadhar Number")
            elif self.PAN.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter PAN")
            elif self.mobile.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Mobile Number")
            elif not self.mobile.get().isdigit() and len(self.mobile.get())==10:
                messagebox.showerror("DATAHIVE","Enter a Valid Mobile Number")
            elif self.Email_Address.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Email Address")
            elif ".com" not in self.Email_Address.get() or "@" not in self.Email_Address.get():
                messagebox.showerror("DATAHIVE","Enter a Valid Email Address")
            elif self.House_Address_text.get("1.0",END) == "":
                messagebox.showerror("DATAHIVE","Please Enter Residential Address")
            else:
                if self.CT_entry.get() == "Yes":
                    l=[self.Empno.get(),self.F_Name.get(),self.L_Name.get(),self.Qualification.get(),self.Designation.get(),self.Subject.get(),self.CT_entry.get(),self.Class.get(),self.Section.get(),self.DOB.get(),self.DOJ.get(), self.Gender.get(),self.Aadhar.get(),self.PAN.get(),self.mobile.get(),self.Email_Address.get(),self.House_Address_text.get("1.0",END)]
                elif self.CT_entry.get() == "No":
                    l=[self.Empno.get(),self.F_Name.get(),self.L_Name.get(),self.Qualification.get(),self.Designation.get(),self.Subject.get(),self.CT_entry.get(),"","",self.DOB.get(),self.DOJ.get(), self.Gender.get(),self.Aadhar.get(),self.PAN.get(),self.mobile.get(),self.Email_Address.get(),self.House_Address_text.get("1.0",END)]
                print(l)
                mycur.execute("INSERT INTO TEACHERS VALUES({},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{},'{}','{}')".format(*l))
                mydb.commit()
                messagebox.showinfo("DATAHIVE","Teacher Added")
                self.clear_all()
                update_dash()

class modify_teacher_details(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(background="#ecf0f5")
        
        self.s=ttk.Style()
        self.s.theme_use("vista")

        self.Empno=StringVar()
        self.F_Name=StringVar()
        self.L_Name=StringVar()
        self.Qualification=StringVar()
        self.Designation=StringVar()
        self.Subject=StringVar()
        self.CT=StringVar()
        self.Class=StringVar()
        self.Section=StringVar()
        self.DOB=StringVar()
        self.DOJ=StringVar()
        self.Gender=StringVar()
        self.Aadhar=StringVar()
        self.PAN=StringVar()
        self.mobile=StringVar()
        self.Email_Address=StringVar()
        
        self.Form_canvas=Canvas(self,background="#ecf0f5")
        self.scroll=ttk.Scrollbar(self,command = self.Form_canvas.yview)
        self.Form_main=Frame(self.Form_canvas,bg="white",bd=0)
        self.Form_main.bind("<Configure>",lambda e: self.Form_canvas.configure(scrollregion=self.Form_canvas.bbox("all")))
        self.Scroll_Form = self.Form_canvas.create_window(0,0, window=self.Form_main,anchor="nw")
        self.Form_canvas.config(yscrollcommand = self.scroll.set)

        Canvas(self.Form_main,height=80,bg="#ecf0f5",borderwidth=0).pack(fill=X,ipadx=150)

        Label(self.Form_main,text="Teacher's Information",bg="white",font=('Segoe UI Light',20,'normal')).pack(padx=5,pady=15)

        self.Empno_frm=Frame(self.Form_main,bg="white")
        Label(self.Empno_frm,text="Employee Number",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Empno_entry_box = LabelFrame(self.Empno_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Empno_entry = Entry(self.Empno_entry_box,textvariable = self.Empno,bd=0,font=('Segoe UI', 11))
        self.Empno_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Empno_entry_box.grid(row=1,column=0,sticky=N+S+W+E)
        Button(self.Empno_frm,text="Check",font=('Segoe UI',11,'normal'),width=12,height=2,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.check_emp()).grid(row=1,column=1,padx=8)
        self.Empno_frm.pack(padx=20,anchor=W)
        
        self.Name_frm = Frame(self.Form_main,bg="white")
        Label(self.Name_frm,text="Name",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.F_Name_entry_box = LabelFrame(self.Name_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.F_Name_entry = Entry(self.F_Name_entry_box,textvariable = self.F_Name,bd=0,font=('Segoe UI', 11))
        self.F_Name_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.F_Name_entry_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.L_Name_entry_box = LabelFrame(self.Name_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.L_Name_entry = Entry(self.L_Name_entry_box,textvariable = self.L_Name,bd=0,font=('Segoe UI', 11))
        self.L_Name_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.L_Name_entry_box.grid(row=1,column=1,padx=6,sticky=N+S+W+E)
        Label(self.Name_frm,text="First Name ",bg="white",font=('Segoe UI',10,'normal')).grid(row=2,column=0,sticky=W)
        Label(self.Name_frm,text="Last Name ",bg="white",font=('Segoe UI',10,'normal')).grid(row=2,column=1,sticky=W,padx=6)
        self.Name_frm.pack(padx=20,anchor=W)

        self.Qualification_frm = Frame(self.Form_main,bg="white")
        Label(self.Qualification_frm,text="Qualification ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Qualification_entry_box = LabelFrame(self.Qualification_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Qualification_entry = Entry(self.Qualification_entry_box,textvariable = self.Qualification,bd=0,font=('calibre',10,'normal'))
        self.Qualification_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Qualification_entry_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Qualification_frm.pack(padx=20,anchor=W)

        self.Desig_frm = Frame(self.Form_main,bg="white")
        Label(self.Desig_frm,text="Designation ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Desig_box = LabelFrame(self.Desig_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Desig_entry = ttk.Combobox(self.Desig_box,textvariable = self.Designation,width=25)
        self.Desig_entry["values"]=["PGT - Post Graduate Teacher","TGT - Trained Graduate Teacher","PRT - Primary Teacher","PET - Physical Education Teacher"]
        self.Desig_entry.pack(fill=BOTH,ipady=8)
        self.Desig_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Desig_frm.pack(padx=20,anchor=W)

        self.Subject_frm=Frame(self.Form_main,bg="white")
        Label(self.Subject_frm,text="Subject ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Subject_box = LabelFrame(self.Subject_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Subject_entry = ttk.Combobox(self.Subject_box,textvariable = self.Subject,width=25)
        self.Subject_entry["values"]=["English","Tamil","Hindi","Social Science","Science", "Physics","Biology", "Chemistry","Maths",
                                      "Sanskrit", "Computer Science", "Commerce", "Accounts", "Buisness Studies", "Engineering Graphics",
                                      "Physical Education", "Art"]
        self.Subject_entry.pack(fill=BOTH,ipady=8)
        self.Subject_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Subject_frm.pack(padx=20,anchor=W)

        self.CT_frm = Frame(self.Form_main,bg="white")
        Label(self.CT_frm,text="Whether Class Teacher ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.CT_box = LabelFrame(self.CT_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.CT_entry = ttk.Combobox(self.CT_box,width=25,textvariable = self.CT)
        self.CT_entry["values"]=["Yes","No"]
        self.CT_entry.pack(fill=BOTH,ipady=8)
        self.CT_box.grid(row=1,column=0,sticky=N+S+W+E)
        Label(self.CT_frm,text="Class ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=1,pady=3,padx=6,sticky=W)
        self.Class_DD_box = LabelFrame(self.CT_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Class_DD = ttk.Combobox(self.Class_DD_box,textvariable = self.Class)
        
        self.Class_DD.pack(fill=BOTH,ipady=8)
        self.Class_DD_box.grid(row=1,column=1,padx=6,sticky=N+S+W+E)
        Label(self.CT_frm,text="Section ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=2,pady=3,sticky=W)
        self.Section_DD_box = LabelFrame(self.CT_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Section_DD = ttk.Combobox(self.Section_DD_box,textvariable = self.Section)
        
        self.Section_DD.pack(fill=BOTH,ipady=8)
        self.Section_DD_box.grid(row=1,column=2,sticky=N+S+W+E)
        self.CT_frm.pack(padx=20,anchor=W)

        self.Date_frm = Frame(self.Form_main,bg="white")
        Label(self.Date_frm,text="Date of Birth",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.DOB_box = LabelFrame(self.Date_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.DOB_entry = DateEntry(self.DOB_box,textvariable=self.DOB,width=20,background='#00264d',foreground='#ecf0f5',date_pattern="yyyy-mm-dd")
        self.DOB_entry.pack(fill=BOTH,ipady=8)
        self.DOB_box.grid(row=1,column=0,sticky=N+S+W+E)
        Label(self.Date_frm,text="Date of Join",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=1,padx=6,pady=3,sticky=W)
        self.DOJ_box = LabelFrame(self.Date_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.DOJ_entry = DateEntry(self.DOJ_box,textvariable=self.DOJ,width=20,background='#00264d',foreground='#ecf0f5',date_pattern="yyyy-mm-dd")
        self.DOJ_entry.pack(fill=BOTH,ipady=8)
        self.DOJ_box.grid(row=1,column=1,sticky=N+S+W+E,padx=6)
        self.Date_frm.pack(padx=20,anchor=W)

        self.Gender_frm=Frame(self.Form_main,bg="white")
        Label(self.Gender_frm,text="Gender ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Gender_box = LabelFrame(self.Gender_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Gender_entry = ttk.Combobox(self.Gender_box,textvariable = self.Gender,width=25)
        self.Gender_entry["values"]=["Male","Female"]
        self.Gender_entry.pack(fill=BOTH,ipady=8)
        self.Gender_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Gender_frm.pack(padx=20,anchor=W)

        self.Aadhar_frm = Frame(self.Form_main,bg="white")
        Label(self.Aadhar_frm,text="Aadhar Number ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Aadhar_box = LabelFrame(self.Aadhar_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Aadhar_entry = Entry(self.Aadhar_box,textvariable = self.Aadhar,bd=0,font=('calibre',10,'normal'))
        self.Aadhar_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Aadhar.trace("w", lambda name, index, mode, sv=self.Aadhar, entry=self.Aadhar_entry: self.aadhar_entry_ch(sv,entry))
        self.Aadhar_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Aadhar_frm.pack(padx=20,anchor=W)

        self.PAN_frm = Frame(self.Form_main,bg="white")
        Label(self.PAN_frm,text="PAN",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.PAN_box = LabelFrame(self.PAN_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.PAN_entry = Entry(self.PAN_box,textvariable = self.PAN,bd=0,font=('calibre',10,'normal'))
        self.PAN_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.PAN_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.PAN_frm.pack(padx=20,anchor=W)
        self.PAN_frm.pack(padx=20,anchor=W)

        Label(self.Form_main,text="Contact Information ",bg="white",font=('Segoe UI Light',20,'normal')).pack(padx=5,pady=15)

        self.Mobile_details = Frame(self.Form_main,bg="white")
        Label(self.Mobile_details,text="Mobile Number",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,padx=6,pady=3,sticky=W)
        self.Mobileno_box = LabelFrame(self.Mobile_details,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Mobileno_entry = Entry(self.Mobileno_box,bd=0,textvariable = self.mobile,font=('calibre',10,'normal'))
        self.Mobileno_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Mobileno_box.grid(row=1,column=0,padx=6,sticky=N+S+W+E)
        self.Mobile_details.pack(padx=20,anchor=W)
        
        self.EMAIL_frm = Frame(self.Form_main,bg="white")
        Label(self.EMAIL_frm,text="Email Address",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Email_box = LabelFrame(self.EMAIL_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Email_Address_entry = Entry(self.Email_box,bd=0,width=60,textvariable = self.Email_Address,font=('calibre',10,'normal'))
        self.Email_Address_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Email_box.grid(row=1,column=0,columnspan=2,sticky=N+S+W+E)
        self.EMAIL_frm.pack(padx=20,anchor=W)

        self.Address_frm = Frame(self.Form_main,bg="white")
        Label(self.Address_frm,text="Residence Address",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.House_box = LabelFrame(self.Address_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.House_Address_text = Text(self.House_box,bd=0,width=40,height=5)
        self.House_Address_text.pack(fill=BOTH,padx=10,ipady=8)
        self.House_box.grid(row=1,column=0,columnspan=2,sticky=N+S+W+E)
        self.Address_frm.pack(padx=20,anchor=W)

        self.button_frm = Frame(self.Form_main,bg="white")
        self.reset_btn = Button(self.button_frm,text="Reset",font=('Segoe UI',11,'normal'),width=12,height=2,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.reset())
        self.reset_btn.grid(row=0,column=0,padx=6,sticky=N+S+W+E)
        self.cancel_btn = Button(self.button_frm,text="Cancel",font=('Segoe UI',11,'normal'),width=12,height=2,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.clear_all())
        self.cancel_btn.grid(row=0,column=1,sticky=N+S+W+E)
        self.submit_btn = Button(self.button_frm,text="Save",font=('Segoe UI',11,'normal'),width=15,height=2,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.Submit())
        self.submit_btn.grid(row=0,column=2,padx=6,sticky=N+S+W+E)
        self.button_frm.pack(padx=20,pady=10,anchor=E)

        Canvas(self.Form_main,height=80,bg="#ecf0f5",borderwidth=0).pack(fill=X,ipadx=150)
        self.Form_canvas.pack(fill=Y,side=LEFT,expand=True,anchor="center",ipadx=150)
        self.scroll.pack( side = RIGHT, fill = Y )

        self.clear_all()
        self.CT_entry.bind("<<ComboboxSelected>>", lambda event: self.EnableDisableFields())

    def aadhar_entry_ch(self,sv,entry):
        i=entry.index(END)
        if sv.get() == "":
            pass
        elif sv.get()[-1] == "-":
            pass
        elif i in [5,10]:
            entry.insert(i-1,"-")
        elif i >= 14:
            entry.delete(14,END)

    def clear_all(self):
        self.Empno_entry.configure(state="normal")
        self.Empno_entry.delete(0,END)
        self.F_Name_entry.delete(0,END)
        self.L_Name_entry.delete(0,END)
        self.Qualification_entry.delete(0,END)
        self.Class_DD.delete(0,END)
        self.Section_DD.delete(0,END)
        self.DOB_entry.delete(0,END)
        self.DOJ_entry.delete(0,END)
        self.Desig_entry.delete(0,END)
        self.Subject_entry.delete(0,END)
        self.CT_entry.delete(0,END)
        self.Gender_entry.delete(0,END)
        self.Aadhar_entry.delete(0,END)
        self.PAN_entry.delete(0,END)
        self.Mobileno_entry.delete(0,END)
        self.Email_Address_entry.delete(0,END)
        self.House_Address_text.delete("1.0",END)
        self.Class_DD.config(state="normal")
        self.Class_DD["values"]=[]
        self.Section_DD.config(state="normal")
        self.Section_DD["values"]=[]
        
    def check_emp(self):
        self.Empno_entry.configure(state="disabled")
        self.result=[]
        mycur.execute("SELECT * FROM TEACHERS WHERE EMPNO = {}".format(self.Empno.get()))
        self.result.extend(mycur.fetchall())

        if self.result == []:
            messagebox.showerror("DataHive","Teacher with this Employee Number does not exist")
            self.Empno_entry.configure(state="normal")
        else:
            self.reset()

    def reset(self):
        try:
            self.F_Name.set(self.result[0][1])
            self.L_Name.set(self.result[0][2])
            self.Qualification.set(self.result[0][3])
            self.Designation.set(self.result[0][4])
            self.Subject.set(self.result[0][5])
            self.CT_entry.set(self.result[0][6])
            self.Class.set(self.result[0][7])
            self.Section.set(self.result[0][8])
            self.DOB.set(self.result[0][9])
            self.DOJ.set(self.result[0][10])
            self.Gender.set(self.result[0][11])
            self.Aadhar.set(self.result[0][12])
            self.PAN.set(self.result[0][13])
            self.mobile.set(self.result[0][14])
            self.Email_Address.set(self.result[0][15])
            self.House_Address_text.delete("1.0",END)
            self.House_Address_text.insert("1.0",self.result[0][16])
        except:
            pass

    def EnableDisableFields(self):
        if self.CT_entry.get() == "Yes":
            self.Class_DD.config(state="normal")
            self.Class_DD["values"]=["LKG","UKG","I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"]
            self.Section_DD.config(state="normal")
            self.Section_DD["values"]=["A","B","C","D","E"]
        else:
            self.Class_DD.delete(0,END)
            self.Section_DD.delete(0,END)
            self.Class_DD.config(state="disabled")
            self.Section_DD.config(state='disabled')

    def Submit(self):
        if self.Empno.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Employee Number")
        elif self.F_Name.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter First Name")
        elif self.L_Name.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Last Name")
        elif self.Qualification.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Qualification")
        elif self.Designation.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Designation")
        elif self.Subject.get() == "":
            messagebox.showerror("DATAHIVE","Please Select Subject")
        elif self.CT_entry.get() == "":
            messagebox.showerror("DATAHIVE","Please Select Whether Class Teacher")
        elif self.CT_entry.get() == "Yes" and self.Class.get() == "":
            messagebox.showerror("DATAHIVE","Please Select the Class")
        elif self.CT_entry.get() == "Yes" and self.Section.get() == "":
            messagebox.showerror("DATAHIVE","Please Select the Section")
        elif self.DOB.get() == "":
            messagebox.showerror("DATAHIVE","Please Select Date of Birth")
        elif self.DOJ.get() == "":
            messagebox.showerror("DATAHIVE","Please Select Date of Joining")
        elif self.Gender.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Gender")
        elif self.Aadhar.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Aadhar Number")
        elif len(self.Aadhar.get().replace("-","")) != 12:
            messagebox.showerror("DATAHIVE","Please Enter a 12 digit Aadhar Number")
        elif not self.Aadhar.get().replace("-","").isdigit():
            messagebox.showerror("DATAHIVE","Enter a Valid Aadhar Number")
        elif self.PAN.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter PAN")
        elif self.mobile.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Mobile Number")
        elif not self.mobile.get().isdigit() and len(self.mobile.get())==10:
            messagebox.showerror("DATAHIVE","Enter a Valid Mobile Number")
        elif self.Email_Address.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Email Address")
        elif ".com" not in self.Email_Address.get() or "@" not in self.Email_Address.get():
            messagebox.showerror("DATAHIVE","Enter a Valid Email Address")
        elif self.House_Address_text.get("1.0",END) == "":
            messagebox.showerror("DATAHIVE","Please Enter Residential Address")
        else:
            l=[self.Empno.get(),self.F_Name.get(),self.L_Name.get(),self.Qualification.get(),self.Designation.get(),self.Subject.get(),self.CT_entry.get(),self.Class.get(),self.Section.get(),self.DOB.get(),self.DOJ.get(), self.Gender.get(),self.Aadhar.get(),self.PAN.get(),self.mobile.get(),self.Email_Address.get(),self.House_Address_text.get("1.0",END)]
            mycur.execute('DELETE FROM TEACHERS WHERE EMPNO = {}'.format(self.Empno.get()))
            mycur.execute("INSERT INTO TEACHERS VALUES({},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{},'{}','{}')".format(*l))
            mydb.commit()
            messagebox.showinfo("DATAHIVE","Modified Successfully")
            update_dash()
            self.clear_all()

class delete_teacher(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(background="#ecf0f5")

        self.checked = PhotoImage(file="icons\\checked.png")
        self.unchecked = PhotoImage(file="icons\\unchecked.png")

        self.search_box=Frame(self)
        
        self.search_bar=Frame(self.search_box,bg="#ecf0f5")
        self.searchbox = Entry(self.search_bar,bd=0,highlightthickness=1,highlightbackground="#4da6ff")
        self.searchbox.pack(side=LEFT,fill=BOTH,expand=True)
        self.search_ico = PhotoImage(file = "icons\\search.png")
        self.search_btn=Button(self.search_bar,image=self.search_ico,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white")
        self.search_btn.img = self.search_ico
        self.search_btn.pack(side=RIGHT)
        self.search_bar.pack(fill=X)

        Button(self.search_box,text="Refresh",bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: update_table_with_checks(self.table,"teacher")).pack(pady=5,anchor=E)

        self.search_box.pack(fill=X,padx=8,pady=4)

        self.search_table = Frame(self)

        self.y_scroll = Scrollbar(self.search_table)
        self.y_scroll.pack( side = RIGHT, fill = BOTH )
        self.x_scroll = Scrollbar(self.search_table,orient="horizontal")
        self.x_scroll.pack( side = BOTTOM, fill = BOTH )

        self.table = ttk.Treeview(self.search_table, yscrollcommand = self.y_scroll.set, xscrollcommand = self.x_scroll.set)
        self.style = ttk.Style(self.table)
        self.style.configure("Treeview",rowheight=30)
        self.table["columns"]=("Empno","FName","LName","Qualification","Designation","Subject","CT","Class","Section","DOB","DOJ","Gender","Aadhar","PAN","mobileno","email","address")
        self.table.pack(side=LEFT,fill=BOTH)
        self.table.heading("Empno", text="Employee Number")
        self.table.heading("FName", text="First Name")
        self.table.heading("LName", text="Last Name")
        self.table.heading("Qualification", text="Qualification")
        self.table.heading("Designation", text="Designation")
        self.table.heading("Subject", text="Subject")
        self.table.heading("CT", text="Class Teacher")
        self.table.heading("Class", text="Class")
        self.table.heading("Section", text="Section")
        self.table.heading("DOB", text="Date of Birth")
        self.table.heading("DOJ", text="Date of Joining")
        self.table.heading("Gender", text="Gender")
        self.table.heading("Aadhar", text="Aadhar Number")
        self.table.heading("PAN", text="PAN")
        self.table.heading("mobileno", text="Mobile Number")
        self.table.heading("email", text="EMail Address")
        self.table.heading("address", text="Residential Address")
        
        self.table.tag_configure("checked",image=self.checked)
        self.table.tag_configure("unchecked",image=self.unchecked)
        self.table.bind("<Button 1>",lambda event: self.toggleCheck(event))

        self.y_scroll.config( command = self.table.yview )
        self.x_scroll.config( command = self.table.xview )
        self.y_scroll.set(0,1)
        self.x_scroll.set(0,1)

        self.search_table.pack(anchor="center",fill=BOTH,padx=8,pady=4,expand=True)

        self.delete_btn = Button(self,text="Delete",font=('Segoe UI',11,'normal'),width=10,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=self.delete_rows)
        self.delete_btn.pack(anchor='e',padx=8,pady=4)

        update_table_with_checks(self.table,"teacher")

    def toggleCheck(self,event):
        rowid = self.table.identify_row(event.y)
        try:
            tag = self.table.item(rowid, "tags")[0]
            tags = list(self.table.item(rowid,"tags"))
            tags.remove(tag)
            self.table.item(rowid, tags=tags)
            if tag == "checked":
                self.table.item(rowid, tags="unchecked")
            else:
                self.table.item(rowid, tags="checked")
        except:
            pass
        
    def delete_rows(self):
        for i in self.table.get_children():
            try:
                if self.table.item(i,"tags")[0] == "checked":
                    print(self.table.item(i,"values")[0])
                    mycur.execute('DELETE FROM TEACHERS WHERE EMPNO = {}'.format(self.table.item(i,"values")[0]))
                    mydb.commit()
                    update_table_with_checks(self.table,"teacher")
                    messagebox.showinfo("DATAHIVE","Deleted Successfully")
            except:
                continue

class search_teacher(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(background="#ecf0f5")

        self.SEARCH = StringVar()
        self.search_box=Frame(self)
        
        self.search_bar=Frame(self.search_box,bg="#ecf0f5")
        self.searchbox = Entry(self.search_bar,bd=0,highlightthickness=1,highlightbackground="#4da6ff",textvariable=self.SEARCH)
        self.searchbox.pack(side=LEFT,fill=BOTH,expand=True)
        self.search_ico = PhotoImage(file = "icons\\search.png")
        self.search_btn=Button(self.search_bar,image=self.search_ico,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.search_tbl())
        self.search_btn.img = self.search_ico
        self.search_btn.pack(side=RIGHT)
        self.search_bar.pack(fill=X)

        Button(self.search_box,text="Refresh",bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.update_table()).pack(pady=5,anchor=E)

        self.search_box.pack(fill=X,padx=8,pady=4)

        self.search_table = Frame(self)

        self.y_scroll = Scrollbar(self.search_table)
        self.y_scroll.pack( side = RIGHT, fill = BOTH )
        self.x_scroll = Scrollbar(self.search_table,orient="horizontal")
        self.x_scroll.pack( side = BOTTOM, fill = BOTH )

        self.table = ttk.Treeview(self.search_table, show="headings", yscrollcommand = self.y_scroll.set, xscrollcommand = self.x_scroll.set)
        self.style = ttk.Style(self.table)
        self.style.configure("Treeview",rowheight=30)
        self.table["columns"]=("Empno","FName","LName","Qualification","Designation","Subject","CT","Class","Section","DOB","DOJ","Gender","Aadhar","PAN","mobileno","email","address")
        self.table.pack(side=LEFT,fill=BOTH)
        self.table.heading("Empno", text="Employee Number")
        self.table.heading("FName", text="First Name")
        self.table.heading("LName", text="Last Name")
        self.table.heading("Qualification", text="Qualification")
        self.table.heading("Designation", text="Designation")
        self.table.heading("Subject", text="Subject")
        self.table.heading("CT", text="Class Teacher")
        self.table.heading("Class", text="Class")
        self.table.heading("Section", text="Section")
        self.table.heading("DOB", text="Date of Birth")
        self.table.heading("DOJ", text="Date of Joining")
        self.table.heading("Gender", text="Gender")
        self.table.heading("Aadhar", text="Aadhar Number")
        self.table.heading("PAN", text="PAN")
        self.table.heading("mobileno", text="Mobile Number")
        self.table.heading("email", text="EMail Address")
        self.table.heading("address", text="Residential Address")

        self.y_scroll.config( command = self.table.yview )
        self.x_scroll.config( command = self.table.xview )
        self.y_scroll.set(0,1)
        self.x_scroll.set(0,1)

        self.search_table.pack(anchor="center",fill=BOTH,padx=8,pady=4,expand=True)
        self.update_table()

    def search_tbl(self):
        mycur.execute("SELECT * FROM TEACHERS WHERE (EMPNO LIKE '%{}%') OR (FNAME LIKE '%{}%') OR (LNAME LIKE '%{}%');".format(self.SEARCH.get(),self.SEARCH.get(),self.SEARCH.get()))
        try:
            self.table.delete(*self.table.get_children())
        except:
            pass
        for i in mycur.fetchall():
            self.table.insert('','end',values=i)

    def update_table(self):
        try:
            self.table.delete(*self.table.get_children())
        except:
            pass
        for i in teacher_data():
            self.table.insert('','end',values=i)

#staffs
class staffs(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(background="#ecf0f5")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        staf_add=PhotoImage(file = "icons\\staffs-add-100.png")
        add=Button(self,image=staf_add,width=400,height=200,text="                 ADD",font=('Segoe UI', 30),bg="#443085",bd=0,activebackground="#000817",compound ='left',command=lambda: controller.show_frame(add_new_staff))
        add.image=staf_add
        add.grid(row=0,column=0,sticky=N+S+E+W,padx=10,pady=10)

        staf_modify=PhotoImage(file = "icons\\staffs-modify-100.png")
        modify=Button(self,image=staf_modify,width=400,height=200,text="           MODIFY",font=('Segoe UI', 30),bg="#f39c12",bd=0,activebackground="#000817",compound ='left',command=lambda: controller.show_frame(modify_staff_details))
        modify.image=staf_modify
        modify.grid(row=0,column=1,sticky=N+S+E+W,padx=10,pady=10)

        staf_search=PhotoImage(file = "icons\\staffs-search-100.png")
        search=Button(self,image=staf_search,width=400,height=200,text="           SEARCH",font=('Segoe UI', 30),bg="#00a65a",bd=0,activebackground="#000817",compound ='left',command=lambda: controller.show_frame(search_staff))
        search.image=staf_search
        search.grid(row=1,column=0,sticky=N+S+E+W,padx=10,pady=10)

        staf_delete=PhotoImage(file = "icons\\staffs-delete-100.png")
        delete=Button(self,image=staf_delete,width=400,height=200,text="             DELETE",font=('Segoe UI', 30),bg="#f56954",bd=0,activebackground="#000817",compound ='left',command=lambda: controller.show_frame(delete_staff))
        delete.image=staf_delete
        delete.grid(row=1,column=1,sticky=N+S+E+W,padx=10,pady=10)        

class add_new_staff(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(background="#ecf0f5")
        self.configure(background="#ecf0f5")
        self.s=ttk.Style()
        self.s.theme_use("vista")

        self.Empno=StringVar()
        self.F_Name=StringVar()
        self.L_Name=StringVar()
        self.Designation=StringVar()
        self.DOB=StringVar()
        self.DOJ=StringVar()
        self.Gender=StringVar()
        self.Aadhar=StringVar()
        self.PAN=StringVar()
        self.mobile=StringVar()
        self.Email_Address=StringVar()
        
        self.Form_canvas=Canvas(self,background="#ecf0f5")
        self.scroll=ttk.Scrollbar(self,command = self.Form_canvas.yview)
        self.Form_main=Frame(self.Form_canvas,bg="white",bd=0)
        self.Form_main.bind("<Configure>",lambda e: self.Form_canvas.configure(scrollregion=self.Form_canvas.bbox("all")))
        self.Scroll_Form = self.Form_canvas.create_window(0,0, window=self.Form_main,anchor="nw")
        self.Form_canvas.config(yscrollcommand = self.scroll.set)

        Canvas(self.Form_main,height=80,bg="#ecf0f5",borderwidth=0).pack(fill=X,ipadx=150)

        Label(self.Form_main,text="Staff's Information",bg="white",font=('Segoe UI Light',20,'normal')).pack(padx=5,pady=15)

        self.Empno_frm=Frame(self.Form_main,bg="white")
        Label(self.Empno_frm,text="Employee Number",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Empno_entry_box = LabelFrame(self.Empno_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Empno_entry = Entry(self.Empno_entry_box,textvariable = self.Empno,bd=0,font=('Segoe UI', 11))
        self.Empno_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Empno_entry_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Empno_frm.pack(padx=20,anchor=W)
        
        self.Name_frm = Frame(self.Form_main,bg="white")
        Label(self.Name_frm,text="Name",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.F_Name_entry_box = LabelFrame(self.Name_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.F_Name_entry = Entry(self.F_Name_entry_box,textvariable = self.F_Name,bd=0,font=('Segoe UI', 11))
        self.F_Name_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.F_Name_entry_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.L_Name_entry_box = LabelFrame(self.Name_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.L_Name_entry = Entry(self.L_Name_entry_box,textvariable = self.L_Name,bd=0,font=('Segoe UI', 11))
        self.L_Name_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.L_Name_entry_box.grid(row=1,column=1,padx=6,sticky=N+S+W+E)
        Label(self.Name_frm,text="First Name ",bg="white",font=('Segoe UI',10,'normal')).grid(row=2,column=0,sticky=W)
        Label(self.Name_frm,text="Last Name ",bg="white",font=('Segoe UI',10,'normal')).grid(row=2,column=1,sticky=W,padx=6)
        self.Name_frm.pack(padx=20,anchor=W)

        self.Desig_frm = Frame(self.Form_main,bg="white")
        Label(self.Desig_frm,text="Designation ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Desig_box = LabelFrame(self.Desig_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Desig_entry = ttk.Combobox(self.Desig_box,textvariable = self.Designation,width=25)
        self.Desig_entry["values"]=["Superindentent","Junior Assistant","Record Clerk","Office Assistant","Sweeper","Security"]
        self.Desig_entry.pack(fill=BOTH,ipady=8)
        self.Desig_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Desig_frm.pack(padx=20,anchor=W)

        self.Date_frm = Frame(self.Form_main,bg="white")
        Label(self.Date_frm,text="Date of Birth",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.DOB_box = LabelFrame(self.Date_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.DOB_entry = DateEntry(self.DOB_box,textvariable=self.DOB,width=20,background='#00264d',foreground='#ecf0f5',date_pattern="yyyy-mm-dd")
        self.DOB_entry.pack(fill=BOTH,ipady=8)
        self.DOB_box.grid(row=1,column=0,sticky=N+S+W+E)
        Label(self.Date_frm,text="Date of Join",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=1,padx=6,pady=3,sticky=W)
        self.DOJ_box = LabelFrame(self.Date_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.DOJ_entry = DateEntry(self.DOJ_box,textvariable=self.DOJ,width=20,background='#00264d',foreground='#ecf0f5',date_pattern="yyyy-mm-dd")
        self.DOJ_entry.pack(fill=BOTH,ipady=8)
        self.DOJ_box.grid(row=1,column=1,sticky=N+S+W+E,padx=6)
        self.Date_frm.pack(padx=20,anchor=W)

        self.Gender_frm=Frame(self.Form_main,bg="white")
        Label(self.Gender_frm,text="Gender ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Gender_box = LabelFrame(self.Gender_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Gender_entry = ttk.Combobox(self.Gender_box,textvariable = self.Gender,width=25)
        self.Gender_entry["values"]=["Male","Female"]
        self.Gender_entry.pack(fill=BOTH,ipady=8)
        self.Gender_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Gender_frm.pack(padx=20,anchor=W)

        self.Aadhar_frm = Frame(self.Form_main,bg="white")
        Label(self.Aadhar_frm,text="Aadhar Number ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Aadhar_box = LabelFrame(self.Aadhar_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Aadhar_entry = Entry(self.Aadhar_box,textvariable = self.Aadhar,bd=0,font=('calibre',10,'normal'))
        self.Aadhar_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Aadhar.trace("w", lambda name, index, mode, sv=self.Aadhar, entry=self.Aadhar_entry: self.aadhar_entry_ch(sv,entry))
        self.Aadhar_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Aadhar_frm.pack(padx=20,anchor=W)

        self.PAN_frm = Frame(self.Form_main,bg="white")
        Label(self.PAN_frm,text="PAN",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.PAN_box = LabelFrame(self.PAN_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.PAN_entry = Entry(self.PAN_box,textvariable = self.PAN,bd=0,font=('calibre',10,'normal'))
        self.PAN_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.PAN_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.PAN_frm.pack(padx=20,anchor=W)
        self.PAN_frm.pack(padx=20,anchor=W)

        Label(self.Form_main,text="Contact Information ",bg="white",font=('Segoe UI Light',20,'normal')).pack(padx=5,pady=15)

        self.Mobile_details = Frame(self.Form_main,bg="white")
        Label(self.Mobile_details,text="Mobile Number",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,padx=6,pady=3,sticky=W)
        self.Mobileno_box = LabelFrame(self.Mobile_details,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Mobileno_entry = Entry(self.Mobileno_box,bd=0,textvariable = self.mobile,font=('calibre',10,'normal'))
        self.Mobileno_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Mobileno_box.grid(row=1,column=0,padx=6,sticky=N+S+W+E)
        self.Mobile_details.pack(padx=20,anchor=W)
        
        self.EMAIL_frm = Frame(self.Form_main,bg="white")
        Label(self.EMAIL_frm,text="Email Address",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Email_box = LabelFrame(self.EMAIL_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Email_Address_entry = Entry(self.Email_box,bd=0,width=60,textvariable = self.Email_Address,font=('calibre',10,'normal'))
        self.Email_Address_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Email_box.grid(row=1,column=0,columnspan=2,sticky=N+S+W+E)
        self.EMAIL_frm.pack(padx=20,anchor=W)

        self.Address_frm = Frame(self.Form_main,bg="white")
        Label(self.Address_frm,text="Residence Address",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.House_box = LabelFrame(self.Address_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.House_Address_text = Text(self.House_box,bd=0,width=40,height=5)
        self.House_Address_text.pack(fill=BOTH,padx=10,ipady=8)
        self.House_box.grid(row=1,column=0,columnspan=2,sticky=N+S+W+E)
        self.Address_frm.pack(padx=20,anchor=W)

        self.button_frm = Frame(self.Form_main,bg="white")
        self.clear = Button(self.button_frm,text="Clear",font=('Segoe UI',11,'normal'),width=12,height=2,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.clear_all())
        self.clear.grid(row=0,column=0,sticky=N+S+W+E)
        self.submit = Button(self.button_frm,text="Submit",font=('Segoe UI',11,'normal'),width=15,height=2,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.Submit())
        self.submit.grid(row=0,column=1,padx=6,sticky=N+S+W+E)
        self.button_frm.pack(padx=20,pady=10,anchor=E)

        Canvas(self.Form_main,height=80,bg="#ecf0f5",borderwidth=0).pack(fill=X,ipadx=150)
        self.Form_canvas.pack(fill=Y,side=LEFT,expand=True,anchor="center",ipadx=150)
        self.scroll.pack( side = RIGHT, fill = Y )

        self.clear_all()

    def aadhar_entry_ch(self,sv,entry):
        i=entry.index(END)
        if sv.get() == "":
            pass
        elif sv.get()[-1] == "-":
            pass
        elif i in [5,10]:
            entry.insert(i-1,"-")
        elif i >= 14:
            entry.delete(14,END)

    def clear_all(self):
        self.Empno_entry.delete(0,END)
        self.F_Name_entry.delete(0,END)
        self.L_Name_entry.delete(0,END)
        self.DOB_entry.delete(0,END)
        self.DOJ_entry.delete(0,END)
        self.Desig_entry.delete(0,END)
        self.Gender_entry.delete(0,END)
        self.Aadhar_entry.delete(0,END)
        self.PAN_entry.delete(0,END)
        self.Mobileno_entry.delete(0,END)
        self.Email_Address_entry.delete(0,END)
        self.House_Address_text.delete("1.0",END)

    def Submit(self):
        for i in teacher_data():
            if int(self.Empno.get()) == i[0]:
                messagebox.showerror("DATAHIVE","Employee with this Employee Number is Already Available")
                break
        else:
            if self.Empno.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Employee Number")
            elif self.F_Name.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter First Name")
            elif self.L_Name.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Last Name")
            elif self.Designation.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Designation")
            elif self.DOB.get() == "":
                messagebox.showerror("DATAHIVE","Please Select Date of Birth")
            elif self.DOJ.get() == "":
                messagebox.showerror("DATAHIVE","Please Select Date of Joining")
            elif self.Gender.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Gender")
            elif self.Aadhar.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Aadhar Number")
            elif len(self.Aadhar.get().replace("-","")) != 12:
                messagebox.showerror("DATAHIVE","Please Enter a 12 digit Aadhar Number")
            elif not self.Aadhar.get().replace("-","").isdigit():
                messagebox.showerror("DATAHIVE","Enter a Valid Aadhar Number")
            elif self.PAN.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter PAN")
            elif self.mobile.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Mobile Number")
            elif not self.mobile.get().isdigit() and len(self.mobile.get())==10:
                messagebox.showerror("DATAHIVE","Enter a Valid Mobile Number")
            elif self.Email_Address.get() == "":
                messagebox.showerror("DATAHIVE","Please Enter Email Address")
            elif ".com" not in self.Email_Address.get() or "@" not in self.Email_Address.get():
                messagebox.showerror("DATAHIVE","Enter a Valid Email Address")
            elif self.House_Address_text.get("1.0",END) == "":
                messagebox.showerror("DATAHIVE","Please Enter Residential Address")
            else:
                l=[self.Empno.get(),self.F_Name.get(),self.L_Name.get(),self.Designation.get(),self.DOB.get(),self.DOJ.get(), self.Gender.get(),self.Aadhar.get(),self.PAN.get(),self.mobile.get(),self.Email_Address.get(),self.House_Address_text.get("1.0",END)]
                mycur.execute("INSERT INTO STAFFS VALUES({},'{}','{}','{}','{}','{}','{}','{}','{}',{},'{}','{}')".format(*l))
                mydb.commit()
                messagebox.showinfo("DATAHIVE","Staff Added")
                update_dash()
                self.clear_all()

class modify_staff_details(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(background="#ecf0f5")
        self.configure(background="#ecf0f5")
        self.s=ttk.Style()
        self.s.theme_use("vista")

        self.Empno=StringVar()
        self.F_Name=StringVar()
        self.L_Name=StringVar()
        self.Designation=StringVar()
        self.DOB=StringVar()
        self.DOJ=StringVar()
        self.Gender=StringVar()
        self.Aadhar=StringVar()
        self.PAN=StringVar()
        self.mobile=StringVar()
        self.Email_Address=StringVar()
        
        self.Form_canvas=Canvas(self,background="#ecf0f5")
        self.scroll=ttk.Scrollbar(self,command = self.Form_canvas.yview)
        self.Form_main=Frame(self.Form_canvas,bg="white",bd=0)
        self.Form_main.bind("<Configure>",lambda e: self.Form_canvas.configure(scrollregion=self.Form_canvas.bbox("all")))
        self.Scroll_Form = self.Form_canvas.create_window(0,0, window=self.Form_main,anchor="nw")
        self.Form_canvas.config(yscrollcommand = self.scroll.set)

        Canvas(self.Form_main,height=80,bg="#ecf0f5",borderwidth=0).pack(fill=X,ipadx=150)

        Label(self.Form_main,text="Staff's Information",bg="white",font=('Segoe UI Light',20,'normal')).pack(padx=5,pady=15)

        self.Empno_frm=Frame(self.Form_main,bg="white")
        Label(self.Empno_frm,text="Employee Number",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Empno_entry_box = LabelFrame(self.Empno_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Empno_entry = Entry(self.Empno_entry_box,textvariable = self.Empno,bd=0,font=('Segoe UI', 11))
        self.Empno_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Empno_entry_box.grid(row=1,column=0,sticky=N+S+W+E)
        Button(self.Empno_frm,text="Check",font=('Segoe UI',11,'normal'),width=12,height=2,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.check_emp()).grid(row=1,column=1,padx=8)
        self.Empno_frm.pack(padx=20,anchor=W)
        
        self.Name_frm = Frame(self.Form_main,bg="white")
        Label(self.Name_frm,text="Name",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.F_Name_entry_box = LabelFrame(self.Name_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.F_Name_entry = Entry(self.F_Name_entry_box,textvariable = self.F_Name,bd=0,font=('Segoe UI', 11))
        self.F_Name_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.F_Name_entry_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.L_Name_entry_box = LabelFrame(self.Name_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.L_Name_entry = Entry(self.L_Name_entry_box,textvariable = self.L_Name,bd=0,font=('Segoe UI', 11))
        self.L_Name_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.L_Name_entry_box.grid(row=1,column=1,padx=6,sticky=N+S+W+E)
        Label(self.Name_frm,text="First Name ",bg="white",font=('Segoe UI',10,'normal')).grid(row=2,column=0,sticky=W)
        Label(self.Name_frm,text="Last Name ",bg="white",font=('Segoe UI',10,'normal')).grid(row=2,column=1,sticky=W,padx=6)
        self.Name_frm.pack(padx=20,anchor=W)

        self.Desig_frm = Frame(self.Form_main,bg="white")
        Label(self.Desig_frm,text="Designation ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Desig_box = LabelFrame(self.Desig_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Desig_entry = ttk.Combobox(self.Desig_box,textvariable = self.Designation,width=25)
        self.Desig_entry["values"]=["PGT - Post Graduate Teacher","TGT - Trained Graduate Teacher","PRT - Primary Teacher","PET - Physical Education Teacher"]
        self.Desig_entry.pack(fill=BOTH,ipady=8)
        self.Desig_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Desig_frm.pack(padx=20,anchor=W)

        self.Date_frm = Frame(self.Form_main,bg="white")
        Label(self.Date_frm,text="Date of Birth",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.DOB_box = LabelFrame(self.Date_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.DOB_entry = DateEntry(self.DOB_box,textvariable=self.DOB,width=20,background='#00264d',foreground='#ecf0f5',date_pattern="yyyy-mm-dd")
        self.DOB_entry.pack(fill=BOTH,ipady=8)
        self.DOB_box.grid(row=1,column=0,sticky=N+S+W+E)
        Label(self.Date_frm,text="Date of Join",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=1,padx=6,pady=3,sticky=W)
        self.DOJ_box = LabelFrame(self.Date_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.DOJ_entry = DateEntry(self.DOJ_box,textvariable=self.DOJ,width=20,background='#00264d',foreground='#ecf0f5',date_pattern="yyyy-mm-dd")
        self.DOJ_entry.pack(fill=BOTH,ipady=8)
        self.DOJ_box.grid(row=1,column=1,sticky=N+S+W+E,padx=6)
        self.Date_frm.pack(padx=20,anchor=W)

        self.Gender_frm=Frame(self.Form_main,bg="white")
        Label(self.Gender_frm,text="Gender ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Gender_box = LabelFrame(self.Gender_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Gender_entry = ttk.Combobox(self.Gender_box,textvariable = self.Gender,width=25)
        self.Gender_entry["values"]=["Male","Female"]
        self.Gender_entry.pack(fill=BOTH,ipady=8)
        self.Gender_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Gender_frm.pack(padx=20,anchor=W)

        self.Aadhar_frm = Frame(self.Form_main,bg="white")
        Label(self.Aadhar_frm,text="Aadhar Number ",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Aadhar_box = LabelFrame(self.Aadhar_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Aadhar_entry = Entry(self.Aadhar_box,textvariable = self.Aadhar,bd=0,font=('calibre',10,'normal'))
        self.Aadhar_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Aadhar.trace("w", lambda name, index, mode, sv=self.Aadhar, entry=self.Aadhar_entry: self.aadhar_entry_ch(sv,entry))
        self.Aadhar_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Aadhar_frm.pack(padx=20,anchor=W)

        self.PAN_frm = Frame(self.Form_main,bg="white")
        Label(self.PAN_frm,text="PAN",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.PAN_box = LabelFrame(self.PAN_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.PAN_entry = Entry(self.PAN_box,textvariable = self.PAN,bd=0,font=('calibre',10,'normal'))
        self.PAN_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.PAN_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.PAN_frm.pack(padx=20,anchor=W)
        self.PAN_frm.pack(padx=20,anchor=W)

        Label(self.Form_main,text="Contact Information ",bg="white",font=('Segoe UI Light',20,'normal')).pack(padx=5,pady=15)

        self.Mobile_details = Frame(self.Form_main,bg="white")
        Label(self.Mobile_details,text="Mobile Number",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,padx=6,pady=3,sticky=W)
        self.Mobileno_box = LabelFrame(self.Mobile_details,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Mobileno_entry = Entry(self.Mobileno_box,bd=0,textvariable = self.mobile,font=('calibre',10,'normal'))
        self.Mobileno_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Mobileno_box.grid(row=1,column=0,padx=6,sticky=N+S+W+E)
        self.Mobile_details.pack(padx=20,anchor=W)
        
        self.EMAIL_frm = Frame(self.Form_main,bg="white")
        Label(self.EMAIL_frm,text="Email Address",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.Email_box = LabelFrame(self.EMAIL_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Email_Address_entry = Entry(self.Email_box,bd=0,width=60,textvariable = self.Email_Address,font=('calibre',10,'normal'))
        self.Email_Address_entry.pack(fill=BOTH,padx=10,ipady=8)
        self.Email_box.grid(row=1,column=0,columnspan=2,sticky=N+S+W+E)
        self.EMAIL_frm.pack(padx=20,anchor=W)

        self.Address_frm = Frame(self.Form_main,bg="white")
        Label(self.Address_frm,text="Residence Address",bg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=3,sticky=W)
        self.House_box = LabelFrame(self.Address_frm,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.House_Address_text = Text(self.House_box,bd=0,width=40,height=5)
        self.House_Address_text.pack(fill=BOTH,padx=10,ipady=8)
        self.House_box.grid(row=1,column=0,columnspan=2,sticky=N+S+W+E)
        self.Address_frm.pack(padx=20,anchor=W)

        self.button_frm = Frame(self.Form_main,bg="white")
        self.reset_btn = Button(self.button_frm,text="Reset",font=('Segoe UI',11,'normal'),width=12,height=2,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.reset())
        self.reset_btn.grid(row=0,column=0,padx=6,sticky=N+S+W+E)
        self.cancel_btn = Button(self.button_frm,text="Cancel",font=('Segoe UI',11,'normal'),width=12,height=2,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.clear_all())
        self.cancel_btn.grid(row=0,column=1,sticky=N+S+W+E)
        self.submit_btn = Button(self.button_frm,text="Save",font=('Segoe UI',11,'normal'),width=15,height=2,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.Submit())
        self.submit_btn.grid(row=0,column=2,padx=6,sticky=N+S+W+E)
        self.button_frm.pack(padx=20,pady=10,anchor=E)

        Canvas(self.Form_main,height=80,bg="#ecf0f5",borderwidth=0).pack(fill=X,ipadx=150)
        self.Form_canvas.pack(fill=Y,side=LEFT,expand=True,anchor="center",ipadx=150)
        self.scroll.pack( side = RIGHT, fill = Y )

        self.clear_all()

    def aadhar_entry_ch(self,sv,entry):
        i=entry.index(END)
        if sv.get() == "":
            pass
        elif sv.get()[-1] == "-":
            pass
        elif i in [5,10]:
            entry.insert(i-1,"-")
        elif i >= 14:
            entry.delete(14,END)

    def check_emp(self):
        self.Empno_entry.configure(state="disabled")
        self.result=[]
        mycur.execute("SELECT * FROM STAFFS WHERE EMPNO = {}".format(self.Empno.get()))
        self.result.extend(mycur.fetchall())

        if self.result == []:
            messagebox.showerror("DataHive","Staff with this Employee Number does not exist")
            self.Empno_entry.configure(state="normal")
        else:
            self.reset()

    def clear_all(self):
        self.Empno_entry.configure(state="normal")
        self.Empno_entry.delete(0,END)
        self.F_Name_entry.delete(0,END)
        self.L_Name_entry.delete(0,END)
        self.DOB_entry.delete(0,END)
        self.DOJ_entry.delete(0,END)
        self.Desig_entry.delete(0,END)
        self.Gender_entry.delete(0,END)
        self.Aadhar_entry.delete(0,END)
        self.PAN_entry.delete(0,END)
        self.Mobileno_entry.delete(0,END)
        self.Email_Address_entry.delete(0,END)
        self.House_Address_text.delete("1.0",END)

    def reset(self):
        try:
            self.F_Name.set(self.result[0][1])
            self.L_Name.set(self.result[0][2])
            self.Designation.set(self.result[0][3])
            self.DOB.set(self.result[0][4])
            self.DOJ.set(self.result[0][5])
            self.Gender.set(self.result[0][6])
            self.Aadhar.set(self.result[0][7])
            self.PAN.set(self.result[0][8])
            self.mobile.set(self.result[0][9])
            self.Email_Address.set(self.result[0][10])
            self.House_Address_text.delete("1.0",END)
            self.House_Address_text.insert("1.0",self.result[0][11])
        except:
            pass

    def Submit(self):
        if self.Empno.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Employee Number")
        elif self.F_Name.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter First Name")
        elif self.L_Name.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Last Name")
        elif self.Designation.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Designation")
        elif self.DOB.get() == "":
            messagebox.showerror("DATAHIVE","Please Select Date of Birth")
        elif self.DOJ.get() == "":
            messagebox.showerror("DATAHIVE","Please Select Date of Joining")
        elif self.Gender.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Gender")
        elif self.Aadhar.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Aadhar Number")
        elif len(self.Aadhar.get().replace("-","")) != 12:
            messagebox.showerror("DATAHIVE","Please Enter a 12 digit Aadhar Number")
        elif not self.Aadhar.get().replace("-","").isdigit():
            messagebox.showerror("DATAHIVE","Enter a Valid Aadhar Number")
        elif self.PAN.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter PAN")
        elif self.mobile.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Mobile Number")
        elif not self.mobile.get().isdigit() and len(self.mobile.get())==10:
            messagebox.showerror("DATAHIVE","Enter a Valid Mobile Number")
        elif self.Email_Address.get() == "":
            messagebox.showerror("DATAHIVE","Please Enter Email Address")
        elif ".com" not in self.Email_Address.get() or "@" not in self.Email_Address.get():
            messagebox.showerror("DATAHIVE","Enter a Valid Email Address")
        elif self.House_Address_text.get("1.0",END) == "":
            messagebox.showerror("DATAHIVE","Please Enter Residential Address")
        else:
            l=[self.Empno.get(),self.F_Name.get(),self.L_Name.get(),self.Designation.get(),self.DOB.get(),self.DOJ.get(), self.Gender.get(),self.Aadhar.get(),self.PAN.get(),self.mobile.get(),self.Email_Address.get(),self.House_Address_text.get("1.0",END)]
            mycur.execute('DELETE FROM STAFFS WHERE EMPNO = {}'.format(self.Empno.get()))
            mycur.execute("INSERT INTO STAFFS VALUES({},'{}','{}','{}','{}','{}','{}','{}','{}',{},'{}','{}')".format(*l))
            mydb.commit()
            messagebox.showinfo("DATAHIVE","Modified Successfully")
            self.clear_all()

class delete_staff(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(background="#ecf0f5")

        self.checked = PhotoImage(file="icons\\checked.png")
        self.unchecked = PhotoImage(file="icons\\unchecked.png")

        self.search_box=Frame(self)

        self.search_bar=Frame(self.search_box)
        self.searchbox = Entry(self.search_bar,bd=0,highlightthickness=1,highlightbackground="#4da6ff")
        self.searchbox.pack(side=LEFT,fill=BOTH,expand=True)
        self.search_ico = PhotoImage(file = "icons\\search.png")
        self.search_btn=Button(self.search_bar,image=self.search_ico,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white")
        self.search_btn.img = self.search_ico
        self.search_btn.pack(side=RIGHT)
        self.search_bar.pack(fill=X)

        Button(self.search_box,text="Refresh",bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: update_table_with_checks(self.table,"staff")).pack(pady=5,anchor=E)

        self.search_box.pack(fill=X,padx=8,pady=4)

        self.search_table = Frame(self)

        self.y_scroll = Scrollbar(self.search_table)
        self.y_scroll.pack( side = RIGHT, fill = BOTH )
        self.x_scroll = Scrollbar(self.search_table,orient="horizontal")
        self.x_scroll.pack( side = BOTTOM, fill = BOTH )

        self.table = ttk.Treeview(self.search_table, yscrollcommand = self.y_scroll.set, xscrollcommand = self.x_scroll.set)
        self.style = ttk.Style(self.table)
        self.style.configure("Treeview",rowheight=30)
        self.table["columns"]=("Empno","FName","LName","Designation","DOB","DOJ","Gender","Aadhar","PAN","mobileno","email","address")
        self.table.pack(side=LEFT,fill=BOTH)
        self.table.heading("Empno", text="Employee Number")
        self.table.heading("FName", text="First Name")
        self.table.heading("LName", text="Last Name")
        self.table.heading("Designation", text="Designation")
        self.table.heading("DOB", text="Date of Birth")
        self.table.heading("DOJ", text="Date of Joining")
        self.table.heading("Gender", text="Gender")
        self.table.heading("Aadhar", text="Aadhar Number")
        self.table.heading("PAN", text="PAN")
        self.table.heading("mobileno", text="Mobile Number")
        self.table.heading("email", text="EMail Address")
        self.table.heading("address", text="Residential Address")

        self.table.tag_configure("checked",image=self.checked)
        self.table.tag_configure("unchecked",image=self.unchecked)
        self.table.bind("<Button 1>",lambda event: self.toggleCheck(event))

        self.y_scroll.config( command = self.table.yview )
        self.x_scroll.config( command = self.table.xview )
        self.y_scroll.set(0,1)
        self.x_scroll.set(0,1)

        self.search_table.pack(anchor="center",fill=BOTH,padx=8,pady=4,expand=True)

        self.delete_btn = Button(self,text="Delete",font=('Segoe UI',11,'normal'),width=10,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=self.delete_rows)
        self.delete_btn.pack(anchor='e',padx=8,pady=4)

        update_table_with_checks(self.table,"staff")

    def toggleCheck(self,event):
        rowid = self.table.identify_row(event.y)
        try:
            tag = self.table.item(rowid, "tags")[0]
            tags = list(self.table.item(rowid,"tags"))
            tags.remove(tag)
            self.table.item(rowid, tags=tags)
            if tag == "checked":
                self.table.item(rowid, tags="unchecked")
            else:
                self.table.item(rowid, tags="checked")
        except:
            pass
    
    def delete_rows(self):
        for i in self.table.get_children():
            try:
                if self.table.item(i,"tags")[0] == "checked":
                    print(self.table.item(i,"values")[0])
                    mycur.execute('DELETE FROM STAFFS WHERE EMPNO = {}'.format(self.table.item(i,"values")[0]))
                    mydb.commit()
                    update_table_with_checks(self.table,"staff")
                    messagebox.showinfo("DATAHIVE","Deleted Successfully")
            except:
                continue

class search_staff(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(background="#ecf0f5")

        self.SEARCH = StringVar()
        self.search_box=Frame(self)
        
        self.search_bar=Frame(self.search_box)
        self.searchbox = Entry(self.search_bar,bd=0,highlightthickness=1,highlightbackground="#4da6ff",textvariable=self.SEARCH)
        self.searchbox.pack(side=LEFT,fill=BOTH,expand=True)
        self.search_ico = PhotoImage(file = "icons\\search.png")
        self.search_btn=Button(self.search_bar,image=self.search_ico,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.search_tbl())
        self.search_btn.img = self.search_ico
        self.search_btn.pack(side=RIGHT)
        self.search_bar.pack(fill=X)

        Button(self.search_box,text="Refresh",bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.update_table()).pack(pady=5,anchor=E)

        self.search_box.pack(fill=X,padx=8,pady=4)

        self.search_table = Frame(self)

        self.y_scroll = Scrollbar(self.search_table)
        self.y_scroll.pack( side = RIGHT, fill = BOTH )
        self.x_scroll = Scrollbar(self.search_table,orient="horizontal")
        self.x_scroll.pack( side = BOTTOM, fill = BOTH )

        self.table = ttk.Treeview(self.search_table, show="headings", yscrollcommand = self.y_scroll.set, xscrollcommand = self.x_scroll.set)
        self.table["columns"]=("Empno","FName","LName","Designation","DOB","DOJ","Gender","Aadhar","PAN","mobileno","email","address")
        self.table.pack(side=LEFT,fill=BOTH)
        self.table.heading("Empno", text="Employee Number")
        self.table.heading("FName", text="First Name")
        self.table.heading("LName", text="Last Name")
        self.table.heading("Designation", text="Designation")
        self.table.heading("DOB", text="Date of Birth")
        self.table.heading("DOJ", text="Date of Joining")
        self.table.heading("Gender", text="Gender")
        self.table.heading("Aadhar", text="Aadhar Number")
        self.table.heading("PAN", text="PAN")
        self.table.heading("mobileno", text="Mobile Number")
        self.table.heading("email", text="EMail Address")
        self.table.heading("address", text="Residential Address")

        self.y_scroll.config( command = self.table.yview )
        self.x_scroll.config( command = self.table.xview )
        self.y_scroll.set(0,1)
        self.x_scroll.set(0,1)

        self.search_table.pack(anchor="center",fill=BOTH,padx=8,pady=4,expand=True)
        self.update_table()

    def search_tbl(self):
        mycur.execute("SELECT * FROM STAFFS WHERE (EMPNO LIKE '%{}%') OR (FNAME LIKE '%{}%') OR (LNAME LIKE '%{}%');".format(self.SEARCH.get(),self.SEARCH.get(),self.SEARCH.get()))
        try:
            self.table.delete(*self.table.get_children())
        except:
            pass
        for i in mycur.fetchall():
            self.table.insert('','end',values=i)

    def update_table(self):
        try:
            self.table.delete(*self.table.get_children())
        except:
            pass
        for i in staff_data():
            self.table.insert('','end',values=i)

class dashboard(Frame):

    def __init__(self, parent, controller):
        global no_of_students, no_of_teachers, no_of_staffs
        Frame.__init__(self,parent)
        self.configure(background="#ecf0f5")
        self.frm0 = Frame(self,background="#ecf0f5")

        self.Msg_Frame=Frame(self.frm0,background="#ecf0f5")
        self.Msg_Frame.pack(side=LEFT,fill=BOTH,padx=10,pady=10)
        self.Msg_Frame.pack_propagate(1)

        # logo name address
        self.lna=Frame(self.Msg_Frame,background="#ecf0f5",width=500,height=135)
        self.schlogo=Canvas(self.lna,width = 100,height = 100,highlightthickness=True,bg="#ecf0f5")
        img = PhotoImage(file='icons/School.png')
        self.schlogo.img=img
        self.schlogo.create_image(50,50,anchor=CENTER,image = img)
        self.schlogo.pack(side=LEFT)
        self.schtext=Frame(self.lna,background="#ecf0f5")
        file = open("School_details.txt","r")
        school_details=file.readlines()
        file.close()
        words=school_details[0].split()
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
        Label(self.schtext, text=school_details[1][:len(school_details[1])-1],font=(('Segoe UI Light'), 9 ),justify=LEFT,bg="#ecf0f5").pack(anchor=W)
        Label(self.schtext, text=school_details[2][:len(school_details[2])-1]+" - "+school_details[3],font=(('Segoe UI Light'), 9 ),justify=LEFT,bg="#ecf0f5").pack(anchor=W)
        self.schtext.pack(side=LEFT,padx=10)
        self.lna.pack(fill=BOTH,side=TOP,anchor=W,pady=5,padx=10)
        self.lna.pack_propagate(0)

        self.Announcement = Frame(self.Msg_Frame,background="#ecf0f5")
        self.scrollbar_y = Scrollbar(self.Announcement)
        self.scrollbar_x = Scrollbar(self.Announcement,orient=HORIZONTAL)
        self.scrollbar_y.pack(side = RIGHT, fill = BOTH)
        self.scrollbar_x.pack(side = BOTTOM, fill = BOTH)
        self.Announcement_listbox = ttk.Treeview(self.Announcement, show="headings",yscrollcommand = self.scrollbar_y.set,xscrollcommand = self.scrollbar_x.set)
        self.Announcement_listbox.pack(side = LEFT, fill = BOTH,expand=True)
        self.Announcement_listbox['columns']=("Announcements")
        self.Announcement_listbox.heading("Announcements",text="Announcements")
        self.Announcement_listbox.column("Announcements",minwidth=0)
        self.scrollbar_y.config(command = self.Announcement_listbox.yview)
        self.scrollbar_x.config(command = self.Announcement_listbox.xview)
        self.Announcement.pack(side=BOTTOM,fill=BOTH)

        try:
            announcement_file = open("announcement.csv","r")
            r=csv.reader(announcement_file)
            for i in r:
                self.Announcement_listbox.insert('','end',values=[i[0].replace(u'\u00AF','\n')]+i[1:])
            announcement_file.close()
        except:
            pass

        self.Msg_Frame1=Frame(self.frm0,background="#ecf0f5")
        self.Msg_Frame1.pack(side=RIGHT,fill=BOTH,padx=10,pady=10,expand=True)
        self.Msg_Frame1.pack_propagate(1)

        self.Event = Frame(self.Msg_Frame1,background="#ecf0f5",width=40)
        self.scrollbar_y = Scrollbar(self.Event)
        self.scrollbar_x = Scrollbar(self.Event,orient=HORIZONTAL)
        self.scrollbar_y.pack(side = RIGHT, fill = BOTH)
        self.scrollbar_x.pack(side = BOTTOM, fill = BOTH)
        self.Event_listbox = ttk.Treeview(self.Event, show="headings",yscrollcommand = self.scrollbar_y.set,xscrollcommand = self.scrollbar_x.set)
        self.Event_listbox.pack(side = LEFT, fill = BOTH,expand=True)
        self.Event_listbox['columns']=("Date","Events")
        self.Event_listbox.heading("Date",text="Date")
        self.Event_listbox.column("Date",minwidth=0, width=150, stretch=NO)
        self.Event_listbox.heading("Events",text="Events")
        self.Event_listbox.column("Events",minwidth=0, stretch=YES)
        self.scrollbar_y.config(command = self.Event_listbox.yview)
        self.scrollbar_x.config(command = self.Event_listbox.xview)
        self.Event.pack(fill=BOTH,expand=True)

        try:
            event_file = open("events.csv","r")
            r=csv.reader(event_file)
            for i in r:
                self.Event_listbox.insert('','end',values=i[:1]+[i[1].replace(u'\u00AF','\n')])
            event_file.close()
        except:
            pass

        self.frm0.pack(side=TOP,fill=BOTH,expand=True)
        self.frm0.pack_propagate(0)

        # side frame
        self.frm=Frame(self,height=200,background="#ecf0f5")
        no_of_students=StringVar(self.frm)
        no_of_teachers=StringVar(self.frm)
        no_of_staffs=StringVar(self.frm)
        update_dash()

        # frm1
        c1="#f56954"
        self.frm1=Frame(self.frm,width=300,height=150,background=c1)
        self.spic = PhotoImage(file="icons\\student-100.png")
        self.stu=Label(self.frm1,background=c1,image=self.spic)
        self.stu.image=self.spic
        self.stu.pack(side=RIGHT,anchor=S,ipadx=10,ipady=20)
        self.nost=Label(self.frm1,textvariable=no_of_students,font=(('Segoe UI'), 40 ),fg='#d9d9d9',background=c1)
        self.nost.place(x=30,y=15)
        self.stlbl=Label(self.frm1,text="Students",font=(('Segoe UI'), 20 ),fg='#d9d9d9',background=c1)
        self.stlbl.place(x=30,y=80)
        self.frm1.pack(side=LEFT,fill=BOTH,pady=10,expand=True)
        self.frm1.pack_propagate(0)

        # frm2
        c2="#f39c12"
        self.frm2=Frame(self.frm,width=300,height=150,background=c2)
        self.notea=Label(self.frm2,textvariable=no_of_teachers,font=(('Segoe UI'), 40 ),fg='#d9d9d9',background=c2)
        self.notea.place(x=30,y=15)
        self.tlbl=Label(self.frm2,text="Teachers",font=(('Segoe UI'), 20 ),fg='#d9d9d9',background=c2)
        self.tlbl.place(x=30,y=80)
        self.tpic = PhotoImage(file="icons\\teacher-100.png")
        self.teac=Label(self.frm2,background=c2,image=self.tpic)
        self.teac.image=self.tpic
        self.teac.pack(side=RIGHT,anchor=S,ipadx=10,ipady=20)
        self.frm2.pack(side=LEFT,fill=BOTH,pady=10,expand=True,padx=10)
        self.frm2.pack_propagate(0)

        # frm3
        c3="#00a65a"
        self.frm3=Frame(self.frm,width=300,height=150,background=c3)
        self.stpic = PhotoImage(file="icons\\staffs-100.png")
        self.staf=Label(self.frm3,background=c3,image=self.stpic)
        self.staf.image=self.stpic
        self.staf.pack(side=RIGHT,anchor=S,ipadx=10,ipady=20)
        self.nostaf=Label(self.frm3,textvariable=no_of_staffs,font=(('Segoe UI'), 40 ),fg='#d9d9d9',background=c3)
        self.nostaf.place(x=30,y=15)
        self.slbl=Label(self.frm3,text="Staffs",font=(('Segoe UI'), 20 ),fg='#d9d9d9',background=c3)
        self.slbl.place(x=30,y=80)
        self.frm3.pack(side=LEFT,fill=BOTH,pady=10,expand=True)
        self.frm3.pack_propagate(0)

        self.frm.pack(side=BOTTOM,fill=X,padx=10)
        self.frm.pack_propagate(0)

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
                self.Announcement_listbox.insert('','end',values=[i[0].replace(u'\u00AF','\n')])
            announcement_file.close()
        except:
            pass
        self.Announcement_listbox.after(400,self.update_Announcement)

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
        self.Frame1 = self
        self.Frame2 = Frame(self.Frame1)
        self.Frame2.pack(fill=X,anchor=N,padx=5,pady=10)

        Label(self.Frame2,text="CLASS").pack(side=LEFT)

        self.Class = ttk.Combobox(self.Frame2)
        self.Class["values"]=["LKG","UKG","I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"]
        self.Class.pack(side=LEFT)

        Label(self.Frame2,text="SECTION").pack(side=LEFT)

        self.Section = ttk.Combobox(self.Frame2)
        self.Section["values"]=["A","B","C","D","E"]
        self.Section.pack(side=LEFT)

        Button(self.Frame2,text="ADD COLUMN",font=('Segoe UI',11,'normal'),width=13,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda:self.Add_Column()).pack(side=RIGHT)

        Button(self.Frame2,text="SAVE",font=('Segoe UI',11,'normal'),width=10,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda:self.save_file()).pack(side=RIGHT,padx=10)

        Button(self.Frame2,text="OPEN",font=('Segoe UI',11,'normal'),width=10,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda:self.open_file()).pack(side=RIGHT)

        self.Form_canvas=Canvas(self.Frame1,background="#ecf0f5",bd=0)
        self.scroll=ttk.Scrollbar(self.Frame1,orient=HORIZONTAL,command = self.Form_canvas.xview)
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

    def Add_Column(self):
        global Entry_L
        self.column+=1
        for i in range(self.row+1):
            if i==0:
                Label(self.table_frm,text="Period"+str(self.column-2),bg="white",font=('Segoe UI',11,'normal')).grid(row=i,column=self.column,pady=1,padx=1,sticky=NSEW)
            else:
                e=Entry(self.table_frm)
                e.grid(row=i,column=self.column,pady=1,padx=1,sticky=NSEW)
                Entry_L[i].append(e)

    def save_file(self):
        with open("Time Table//"+self.Class.get()+self.Section.get()+".csv","w",newline="") as timetable:
            w = csv.writer(timetable)
            w.writerow(["Period "+str(i+1) for i in range(self.column-2)])
            for i in Entry_L:
                l=[]
                for j in i:
                    l.append(j.get())
                w.writerow(l)
        messagebox.showinfo("DataHIVE","File has been saved successfully.")

    def open_file(self):
        global Entry_L
        try:
            timetable = open("Time Table//"+self.Class.get()+self.Section.get()+".csv","r",newline="")
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
            messagebox.showerror("DataHIVE","File not found")

class report_card(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.configure(background="#ecf0f5")

        self.row=12
        self.column=5

        self.Frame1 = self

        self.Frame2 = Frame(self.Frame1)
        self.Frame2.pack(fill=X,anchor=N,padx=5,pady=8)

        Label(self.Frame2,text="Admission Number").pack(side=LEFT)

        self.Admno = Entry(self.Frame2)
        self.Admno.pack(side=LEFT)

        Button(self.Frame2,text="EXPORT",font=('Segoe UI',11,'normal'),width=10,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda:self.print_file()).pack(side=RIGHT)
        
        Button(self.Frame2,text="SAVE",font=('Segoe UI',11,'normal'),width=10,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda:self.save_file()).pack(side=RIGHT,padx=10)

        Button(self.Frame2,text="CALCULATE TOTAL",font=('Segoe UI',11,'normal'),width=17,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda:self.calculate()).pack(side=RIGHT)
        
        Button(self.Frame2,text="OPEN",font=('Segoe UI',11,'normal'),width=10,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda:self.open_file()).pack(side=RIGHT,padx=10)

        self.ncs_frm = Frame(self)
        self.ncs_frm.pack(fill=X,anchor=NW,padx=5,pady=8)
        self.Name=StringVar()
        self.Class=StringVar()
        self.Section=StringVar()
        Label(self.ncs_frm,text="Name",font=(('Segoe UI'), 12 )).grid(row=0,column=0,sticky=W)
        Label(self.ncs_frm,text="Class",font=(('Segoe UI'), 12 )).grid(row=1,column=0,sticky=W)
        Label(self.ncs_frm,text="Section",font=(('Segoe UI'), 12 )).grid(row=2,column=0,sticky=W)
        Label(self.ncs_frm,textvariable=self.Name,font=(('Segoe UI'), 12 )).grid(row=0,column=1,sticky=W)
        Label(self.ncs_frm,textvariable=self.Class,font=(('Segoe UI'), 12 )).grid(row=1,column=1,sticky=W)
        Label(self.ncs_frm,textvariable=self.Section,font=(('Segoe UI'), 12 )).grid(row=2,column=1,sticky=W)

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

    def calculate(self):
        midterm=0
        quaterly=0
        halfyearly=0
        annual=0
        for i,j in self.report_l.items():
            if i == "Total":
                j[0].delete(0,END)
                j[1].delete(0,END)
                j[2].delete(0,END)
                j[3].delete(0,END)
                j[0].insert(0,str(midterm))
                j[1].insert(0,str(quaterly))
                j[2].insert(0,str(halfyearly))
                j[3].insert(0,str(annual))
                
            else:
                temp=[]
                for theory, internal, total in zip(j["Theory"],j["Internal"],j["Total"]):
                    if theory.get() == "":
                        theory.insert(0,"0")
                    if internal.get() == "":
                        internal.insert(0,"0")
                    total.delete(0,END)
                    total.insert(0,str(int(theory.get())+int(internal.get())))
                    temp.append(int(theory.get())+int(internal.get()))
                midterm+=temp[0]
                quaterly+=temp[1]
                halfyearly+=temp[2]
                annual+=temp[3]

    def save_file(self):
        try :
            for i in student_data():
                if self.Admno.get() == str(i[0]):
                    self.name_class_section=[i[1]+" "+i[2],i[4],i[5]]
                    break
            else:
                self.name_class_section=[]
                
            self.marks_l=[]
            for i,j in self.report_l.items():
                if i == "Total":
                    for m in j:
                        mark=m.get()
                        if mark == "":
                            self.marks_l.append("0")
                        else:
                            self.marks_l.append(mark)
                else:
                    for k,l in j.items():
                        for m in l:
                            mark=m.get()
                            if mark == "":
                                self.marks_l.append("0")
                            else:
                                self.marks_l.append(mark)
            print("VALUES("+self.Admno.get()+","+",".join(map(str, self.marks_l))+")")

            if self.name_class_section[1] in ["I","II","III","IV","V","VI","VII","VIII"]:
                try:
                    mycur.execute("DELETE FROM MARKS_I_VIII WHERE ADMNO = {};".format(self.Admno.get()))
                    mydb.commit()
                except:
                    pass
                mycur.execute("INSERT INTO MARKS_I_VIII VALUES("+self.Admno.get()+","+",".join(map(str, self.marks_l))+")")
                mydb.commit()
                
            elif self.name_class_section[1] in ["X","IX"]:
                try:
                    mycur.execute("DELETE FROM MARKS_IX_X WHERE ADMNO = {};".format(self.Admno.get()))
                    mydb.commit()
                except:
                    pass
                mycur.execute("INSERT INTO MARKS_IX_X VALUES("+self.Admno.get()+","+",".join(map(str, self.marks_l))+")")
                mydb.commit()
                
            elif self.name_class_section[1] in ["XI","XII"]:
                try:
                    mycur.execute("DELETE FROM MARKS_XI_XII WHERE ADMNO = {};".format(self.Admno.get()))
                    mydb.commit()
                except:
                    pass
                mycur.execute("INSERT INTO MARKS_XI_XII VALUES("+self.Admno.get()+","+",".join(map(str, self.marks_l))+")")
                mydb.commit()
                
            elif self.name_class_section[1] in ["LKG","UKG"]:
                try:
                    mycur.execute("DELETE FROM MARKS_LKG_UKG WHERE ADMNO = {};".format(self.Admno.get()))
                    mydb.commit()
                except:
                    pass
                mycur.execute("INSERT INTO MARKS_LKG_UKG VALUES("+self.Admno.get()+","+",".join(map(str, self.marks_l))+")")
                mydb.commit()
            else:
                messagebox.showerror("DataHIVE","Enter a Valid Admission Number and click OPEN")
        except:
            messagebox.showerror("DataHIVE","Enter Admission Number and click OPEN to save")

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
            if self.Admno.get() == str(i[0]):
                self.name_class_section=[i[1]+" "+i[2],i[4],i[5]]
                break
            
        if self.name_class_section == []:
            messagebox.showerror("DataHIVE","Admission Number not Found.")
            self.subjects=["Subject 1","Subject 2","Subject 3","Subject 4","Subject 5"]
            self.marks = []
            self.Name.set("")
            self.Class.set("")
            self.Section.set("")

        else:
            self.Name.set(self.name_class_section[0])
            self.Class.set(self.name_class_section[1])
            self.Section.set(self.name_class_section[2])

            if self.name_class_section[1] in ["I","II","III","IV","V","VI","VII","VIII"]:
                mycur.execute('SELECT * FROM MARKS_I_VIII WHERE ADMNO = {}'.format(self.Admno.get()))
            elif self.name_class_section[1] in ["X","IX"]:
                mycur.execute('SELECT * FROM MARKS_IX_X WHERE ADMNO = {}'.format(self.Admno.get()))
            elif self.name_class_section[1] in ["XI","XII"]:
                mycur.execute('SELECT * FROM MARKS_XI_XII WHERE ADMNO = {}'.format(self.Admno.get()))
            elif self.name_class_section[1] in ["LKG","UKG"]:
                mycur.execute('SELECT * FROM MARKS_LKG_UKG WHERE ADMNO = {}'.format(self.Admno.get()))

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
        school_details=file.readlines()
        file.close()

        for i in student_data():
            if self.Admno.get() == str(i[0]):
                self.name_class_section=[i[1]+" "+i[2],i[4],i[5]]
                break
            else:
                self.name_class_section=[]
                        
        if self.name_class_section != []:
            data_dict = {
                "info":{
                        "admno":self.Admno.get(),
                        "name":self.name_class_section[0],
                        "class":self.name_class_section[1],
                        "sec":self.name_class_section[2],
                        "school name": school_details[0]
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

class loading(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.configure(background="#ecf0f5")
        self.logo = Canvas(self,width = 500, height = 500,highlightthickness=False,background="#ecf0f5")
        img = PhotoImage(file="icons\\DATAHIVE-logo.png")
        self.logo.img=img
        self.logo.create_image(250,250,anchor=CENTER,image = img)
        self.logo.pack(expand=True)

class announcements(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.configure(background="#ecf0f5")
        self.Announcement = Frame(self ,background="#ecf0f5",height=200)
        self.scrollbar = Scrollbar(self.Announcement)
        self.scrollbar.pack(side = RIGHT, fill = BOTH)
        self.Announcement_listbox = ttk.Treeview(self.Announcement, show="headings",yscrollcommand = self.scrollbar.set)
        self.Announcement_listbox.pack(side = LEFT, fill = BOTH,expand=True)
        self.Announcement_listbox['columns']=("Announcements")
        self.Announcement_listbox.heading("Announcements",text="Announcements")
        self.Announcement_listbox.column("Announcements",minwidth=0)
        self.scrollbar.config(command = self.Announcement_listbox.yview)
        self.Announcement.pack(fill=BOTH,expand=True,pady=15,padx=10)
        self.Announcement.pack_propagate(0)

        self.Frame3 =  Frame(self ,background="#ecf0f5")
        self.Frame3.pack(fill=BOTH,padx=10)

        self.teacher_ =  IntVar()
        Checkbutton(self.Frame3,text="Teachers",activebackground="#ececec",activeforeground="#000000",background="#ecf0f5",foreground="#000000",onvalue=1, offvalue=0,variable=self.teacher_).pack(side=LEFT,anchor=W)

        self.student_ =  IntVar()
        Checkbutton(self.Frame3,text="Students",activebackground="#ececec",activeforeground="#000000",background="#ecf0f5",foreground="#000000",onvalue=1, offvalue=0,variable=self.student_).pack(side=LEFT,padx=4,anchor=W)

        self.specific_class_ = IntVar()
        self.specific_class =  Checkbutton(self.Frame3,text="Specific Class",activebackground="#ececec",activeforeground="#000000",background="#ecf0f5",foreground="#000000",onvalue=1, offvalue=0,variable=self.specific_class_)
        self.specific_class.pack(side=LEFT,anchor=W)

        self.Class=StringVar()
        self.Section=StringVar()
        self.Class_Section_frm = Frame(self.Frame3,bg="#ecf0f5")
        self.Class_DD_box = LabelFrame(self.Class_Section_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Class_DD = ttk.Combobox(self.Class_DD_box,textvariable = self.Class)
        self.Class_DD["values"]=["LKG","UKG","I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"]
        self.Class_DD.pack(fill=BOTH)
        self.Class_DD_box.grid(row=1,column=0,sticky=N+S+W+E)
        self.Section_DD_box = LabelFrame(self.Class_Section_frm,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.Section_DD = ttk.Combobox(self.Section_DD_box,textvariable = self.Section)
        self.Section_DD["values"]=["A","B","C","D","E"]
        self.Section_DD.pack(fill=BOTH)
        self.Section_DD_box.grid(row=1,column=1,sticky=N+S+W+E,padx=6)
        self.Class_Section_frm.pack(side=LEFT,padx=20,anchor=W)

        self.Frame2 =  Frame(self ,background="#ecf0f5")
        self.Frame2.pack(fill=BOTH,expand=True,padx=10,pady=10)

        self.message =  scrolledtext.ScrolledText(self.Frame2,wrap = WORD,width = 10,height = 10)
        self.message.pack(fill=BOTH,pady=15,expand=True)

        self.Button1 =  Button(self.Frame2,text='''Announce''',font=('Segoe UI',11,'normal'),width=10,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.save_announcements())
        self.Button1.pack(side=RIGHT)

        self.Button2 =  Button(self.Frame2,text='''New''',font=('Segoe UI',11,'normal'),width=10,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.new_announcements())
        self.Button2.pack(side=RIGHT,padx=10)

        self.Button3 =  Button(self.Frame2,text='''Delete''',font=('Segoe UI',11,'normal'),width=10,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.delete_announcements())
        self.Button3.pack(side=RIGHT)

        self.Announcement_listbox.bind("<Button 1>",lambda event: self.select_row(event))
        self.load_announcements()

    def delete_announcements(self):
        announcements_file = open("announcement.csv","r")
        r=list(csv.reader(announcements_file))
        i=self.Announcement_listbox.item(self.rowid)["values"]
        r.remove([i[0].replace('\n',u'\u00AF')]+[str(i[1])]+[str(i[2])]+[str(i[3])]+[str(i[4])]+[str(i[5])])
        announcements_file.close()
        print(r)
        temp = open("temp","w",newline="")
        w=csv.writer(temp)
        w.writerows(r)
        temp.close()
        os.remove("announcement.csv")
        os.rename("temp","announcement.csv")
        self.load_announcements()
        self.new_announcements()

    def new_announcements(self):
        self.Button1.configure(text="Announce",command=lambda: self.save_announcements())
        self.message.delete("1.0",END)
        self.teacher_.set(0)
        self.student_.set(0)
        self.specific_class_.set(0)
        self.Class_DD.delete(0,END)
        self.Section_DD.delete(0,END)

    def update_announcements(self):
        announcement_file = open("announcement.csv","r")
        r=list(csv.reader(announcement_file))
        print(self.Announcement_listbox.item(self.rowid))
        i=self.Announcement_listbox.item(self.rowid)["values"]
        print(r)
        print([i[0].replace('\n',u'\u00AF')]+[str(i[1])]+[str(i[2])]+[str(i[3])]+[str(i[4])]+[str(i[5])])
        r.remove([i[0].replace('\n',u'\u00AF')]+[str(i[1])]+[str(i[2])]+[str(i[3])]+[str(i[4])]+[str(i[5])])
        r+=[[self.message.get("1.0",END).replace('\n',u'\u00AF'),str(self.teacher_.get()),str(self.student_.get()),str(self.specific_class_.get()),self.Class.get(),self.Section.get()]]
        announcement_file.close()
        print(r)
        temp = open("temp","w",newline="")
        w=csv.writer(temp)
        w.writerows(r)
        temp.close()
        os.remove("announcement.csv")
        os.rename("temp","announcement.csv")
        self.load_announcements()
        self.new_announcements()

    def select_row(self,event):
        try:
            self.rowid = self.Announcement_listbox.identify_row(event.y)
            item = self.Announcement_listbox.item(self.rowid)
            self.message.delete("1.0",END)
            self.message.insert("1.0",item["values"][0])
            self.teacher_.set(item["values"][1])
            self.student_.set(item["values"][2])
            self.specific_class_.set(item["values"][3])
            self.Class.set(item["values"][4])
            self.Section.set(item["values"][5])
            self.Button1.configure(text="Update",command=lambda: self.update_announcements())
        except:
            pass

    def save_announcements(self):
        announcement_file = open("announcement.csv","a",newline="")
        w=csv.writer(announcement_file)
        print([self.message.get("1.0",END).replace('\n',u'\u00AF'),str(self.teacher_.get()),str(self.student_.get()),str(self.specific_class_.get()),self.Class.get(),self.Section.get()])
        w.writerow([self.message.get("1.0",END).replace('\n',u'\u00AF'),str(self.teacher_.get()),str(self.student_.get()),str(self.specific_class_.get()),self.Class.get(),self.Section.get()])
        announcement_file.close()
        self.load_announcements()
        self.new_announcements()
        
    def load_announcements(self):
        try:
            self.Announcement_listbox.delete(*self.Announcement_listbox.get_children())
        except:
            pass
        try:
            announcement_file = open("announcement.csv","r")
            r=csv.reader(announcement_file)
            for i in r:
                self.Announcement_listbox.insert('','end',values=[i[0].replace(u'\u00AF','\n')]+i[1:])
            announcement_file.close()
        except:
            with open("announcement.csv","w") as announcement_file:
                pass

class events(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.configure(background="#ecf0f5")
        self.Event = Frame(self,background="#ecf0f5",height=200)
        self.scrollbar = Scrollbar(self.Event)
        self.scrollbar.pack(side = RIGHT, fill = BOTH)
        self.Event_listbox = ttk.Treeview(self.Event, show="headings",yscrollcommand = self.scrollbar.set)
        self.Event_listbox.pack(side = LEFT, fill = BOTH,expand=True)
        self.Event_listbox['columns']=("Date","Events")
        self.Event_listbox.heading("Date",text="Date")
        self.Event_listbox.column("Date",minwidth=0, width=150, stretch=NO)
        self.Event_listbox.heading("Events",text="Event")
        self.Event_listbox.column("Events",minwidth=0, stretch=YES)
        self.scrollbar.config(command = self.Event_listbox.yview)
        self.Event.pack(fill=BOTH,expand=True,pady=10,padx=10)
        self.Event.pack_propagate(0)

        self.date = StringVar()
        self.date_box = LabelFrame(self,bd=0,highlightthickness=2,highlightcolor="light blue",bg="white")
        self.date_entry = DateEntry(self.date_box,width=20,background='#00264d',foreground='#ecf0f5',date_pattern="yyyy-mm-dd",variable=self.date)
        self.date_entry.pack(fill=BOTH,ipady=2)
        self.date_box.pack(anchor=W,pady=10,padx=10)

        self.Frame2 = Frame(self ,background="#ecf0f5")
        self.Frame2.pack(side=LEFT,fill=BOTH,expand=True,padx=10,pady=0)

        self.message = scrolledtext.ScrolledText(self.Frame2,wrap="word",width=10,height=10)
        self.message.pack(fill=BOTH,pady=0)

        self.Button1 =  Button(self.Frame2,text='''Create Event''',font=('Segoe UI',11,'normal'),width=14,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.save_event())
        self.Button1.pack(side=RIGHT,pady=8)

        self.Button2 =  Button(self.Frame2,text='''New Event''',font=('Segoe UI',11,'normal'),width=11,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.new_event())
        self.Button2.pack(side=RIGHT,padx=10,pady=8)

        self.Button3 =  Button(self.Frame2,text='''Delete''',font=('Segoe UI',11,'normal'),width=10,bd=0,bg="#4da6ff",activebackground="#00264d",fg="white",activeforeground="white",command=lambda: self.delete_event())
        self.Button3.pack(side=RIGHT,pady=8)

        self.Frame3 =  Frame(self ,background="#ecf0f5")
        self.Frame3.pack(side=RIGHT,fill=BOTH,padx=20,pady=40)

        self.teacher_ =  IntVar()
        Checkbutton(self.Frame3,text="Teachers",activebackground="#ececec",activeforeground="#000000",background="#ecf0f5",foreground="#000000",onvalue=1, offvalue=0,variable=self.teacher_).pack(anchor=W)

        self.student_ =  IntVar()
        Checkbutton(self.Frame3,text="Students",activebackground="#ececec",activeforeground="#000000",background="#ecf0f5",foreground="#000000",onvalue=1, offvalue=0,variable=self.student_).pack(anchor=W)

        self.Event_listbox.bind("<Button 1>",lambda event: self.select_row(event))
        self.load_event()

    def delete_event(self):
        event_file = open("events.csv","r")
        r=list(csv.reader(event_file))
        i=self.Event_listbox.item(self.rowid)["values"]
        r.remove(i[:1]+[i[1].replace('\n',u'\u00AF')]+[str(i[2])]+[str(i[3])])
        event_file.close()
        print(r)
        temp = open("temp","w",newline="")
        w=csv.writer(temp)
        w.writerows(r)
        temp.close()
        os.remove("events.csv")
        os.rename("temp","events.csv")
        self.load_event()
        self.new_event()

    def new_event(self):
        self.Button1.configure(text="Create Event",command=lambda: self.save_event())
        self.message.delete("1.0",END)
        self.teacher_.set(0)
        self.student_.set(0)

    def update_event(self):
        event_file = open("events.csv","r")
        r=list(csv.reader(event_file))
        print(self.Event_listbox.item(self.rowid))
        i=self.Event_listbox.item(self.rowid)["values"]
        print(r)
        print(i[:1]+[i[1].replace('\n',u'\u00AF')]+[str(i[2])]+[str(i[3])])
        r.remove(i[:1]+[i[1].replace('\n',u'\u00AF')]+[str(i[2])]+[str(i[3])])
        r+=[[self.date_entry.get(),self.message.get("1.0",END).replace('\n',u'\u00AF'),str(self.teacher_.get()),str(self.student_.get())]]
        event_file.close()
        print(r)
        temp = open("temp","w",newline="")
        w=csv.writer(temp)
        w.writerows(r)
        temp.close()
        os.remove("events.csv")
        os.rename("temp","events.csv")
        self.load_event()
        self.new_event()

    def select_row(self,event):
        try:
            self.rowid = self.Event_listbox.identify_row(event.y)
            item = self.Event_listbox.item(self.rowid)
            self.date.set(item["values"][0])
            self.message.delete("1.0",END)
            self.message.insert("1.0",item["values"][1])
            self.teacher_.set(item["values"][2])
            self.student_.set(item["values"][3])
            self.Button1.configure(text="Update Event",command=lambda: self.update_event())
        except:
            pass

    def save_event(self):
        event_file = open("events.csv","a",newline="")
        w=csv.writer(event_file)
        print([self.date_entry.get(),self.message.get("1.0",END),str(self.teacher_.get()),str(self.student_.get())])
        w.writerow([self.date_entry.get(),self.message.get("1.0",END).replace('\n',u'\u00AF'),str(self.teacher_.get()),str(self.student_.get())])
        event_file.close()
        self.load_event()
        self.new_event()
        
    def load_event(self):
        try:
            self.Event_listbox.delete(*self.Event_listbox.get_children())
        except:
            pass
        try:
            event_file = open("events.csv","r")
            r=csv.reader(event_file)
            for i in r:
                self.Event_listbox.insert('','end',values=i[:1]+[i[1].replace(u'\u00AF','\n')]+i[2:])
            event_file.close()
        except:
            with open("events.csv","w") as event_file:
                pass

def close_window():
    if messagebox.askyesno("DATAHIVE","Are you sure? Do you want to exit"):
        root.destroy()
    else:
        pass

if __name__ == "__main__":
    Main=Tk()
    Manager_admin(Main)
    Main.protocol("WM_DELETE_WINDOW",close_window_main)
    Main.mainloop()