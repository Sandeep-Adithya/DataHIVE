from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
import ctypes
import pickle
import base64
import mysql.connector as sql
from tkinter import messagebox
import random
import csv
import datetime
import os

def encrypt(Word) :
    Special = [33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,58,59,60,61,62,63,64,91,92,93,94,95,96]
    Special_List , Encrypted = [] , ''
    for special in Special :
        Special_List.append(chr(special))
    for Letter in Word :
        Encrypted += str(ord(Letter))+random.choice(Special_List)

    return base64.b85encode(Encrypted.encode("utf-8"))

def decrypt(Word) :
    init_ , Initial , Final , Decrypt_List , Special_List , Decrypted = 0 , 0 , 0 , [] , [] , ''
    Special = [33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,58,59,60,61,62,63,64,91,92,93,94,95,96]
    for special in Special :
        Special_List.append(chr(special))
    Word = base64.b85decode(Word).decode("utf-8")
    while init_ < len(Word):
        for special in Special_List:
            if Word[init_] == special and Initial==0 and Final==0:
                Final = init_
                Decrypt_List.append(Word[Initial:Final])
            elif Word[init_] == special and init_>0 :
                Initial = Final+1
                Final = init_
                Decrypt_List.append(Word[Initial:Final])
        init_+=1     
    for Decrypt_Letter in Decrypt_List:
        Decrypted += chr(int(Decrypt_Letter))
    return Decrypted

def Create_Date():
    Date = datetime.date
    Time = datetime.datetime
    TIME = str(Time.now().time())
    TIME = TIME[:TIME.index('.')]
    DATE = str(Date.today())
    return DATE , TIME  

def RECORDS(ID , Username, Name, Designation, Email):
    FIELDS = ['ID','USERNAME','NAME','EMAIL','CREATED DATE','CREATED TIME']
    File_Present_Check,Flag = 'NO',0
    DATE , TIME = Create_Date()
    DATA = {'ID' : ID , 'USERNAME' : Username ,'NAME': Name , 'EMAIL':Email , 'CREATED DATE' : DATE , 'CREATED TIME' : TIME}
    DIR = os.listdir()   
    for File in DIR:              
        if File == 'USER-RECORDS.csv':
            File_Present_Check = 'YES'                
            with open('USER-RECORDS.csv','a',newline = '') as File_Open:                    
                File_Writer = csv.DictWriter(File_Open , fieldnames = FIELDS)
                File_Writer.writerow(DATA)
    if File_Present_Check == 'NO':
        with open('USER-RECORDS.csv','w',newline = '') as File_Open:
            File_Writer = csv.DictWriter(File_Open , fieldnames = FIELDS)
            File_Writer.writeheader()
            File_Writer.writerow(DATA)
    
width, height = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

class School_Setup:

    def __init__(self, root):

        self.root=root
        self.root.geometry("740x490+"+str(int((width/2)-370))+"+"+str(int((height/2)-275)))
        self.root.resizable(width=False, height=False)
        self.root.title("DATAHIVE School Manager - Setup")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.s = ttk.Style()
        self.s.theme_use("default")
        self.s.configure("TProgressbar", foreground='#000000', background='#4da6ff',troughcolor='#004080', thickness=10,borderwidth=0)
        self.setup_welcome()

    def setup_welcome(self):

        self.welcome_frm = Frame(self.root,bg="#00264d")
        Label(self.welcome_frm,background="#00264D",foreground="#D9D9D9",font=(('Segoe UI Light'), 12 ),text="").pack()
        Label(self.welcome_frm,background="#00264D",foreground="#D9D9D9",font=(('Segoe UI Light'), 30 ),text="Welcome to").pack()
        self.logo = Canvas(self.welcome_frm,width = 250, height = 250,highlightthickness=False)
        img = PhotoImage(file="icons\\logo-welcome.png")
        self.logo.img=img
        self.logo.create_image(125,125,anchor=CENTER,image = img)
        self.logo.pack()
        Label(self.welcome_frm,background="#00264D",foreground="#D9D9D9",font=(('Segoe UI Light'), 40 ),text="DATAHIVE").pack()
        Label(self.welcome_frm,background="#00264D",foreground="#D9D9D9",font=(('Segoe UI Light'), 20 ),text="SCHOOL MANAGER").pack()
        Button(self.welcome_frm,bd=0,bg="#4da6ff",activebackground="#000817",fg="white",activeforeground="white",font=(('Segoe UI Light'), 11 ),padx="8",text='Next',command=lambda: self.t_c()).place(x=725,y=475,anchor=S+E)
        self.welcome_frm.grid(row=0,column=0,sticky=N+S+E+W)

    def t_c(self):

        file=open("Info@DataHive.txt","r")
        info=file.read()
        file.close()
        self.t_c_frm = Frame(self.root,bg="#00264d")
        Label(self.t_c_frm,background="#00264D",foreground="white",font=(('Segoe UI Light'), 20 ),text='LICENSE INFORMATION').pack(pady=5)
        self.text_area = scrolledtext.ScrolledText(self.t_c_frm,wrap = WORD,width = 40,height = 21,font = ("Consolas",11))
        self.text_area.insert(INSERT, info)
        self.text_area.configure(state ='disabled')
        self.text_area.pack(fill=BOTH,padx=20)
        Button(self.t_c_frm,bd=0,bg="#4da6ff",activebackground="#000817",fg="white",activeforeground="white",font=(('Segoe UI Light'), 11 ),padx="8",text='Accept',command=lambda: self.setup_start()).place(x=725,y=475,anchor=S+E)
        self.t_c_frm.grid(row=0,column=0,sticky=N+S+E+W)
        self.t_c_frm.tkraise()

    def setup_start(self):
        
        self.setup_frm = Frame(self.root,bg="#00264d")
        Label(self.setup_frm,background="#00264D",foreground="#D9D9D9",font=(('Segoe UI Light'), 40 ),text="SETUP YOUR\nSCHOOL IN\nDATAHIVE").pack(fill=BOTH,expand=True)
        Button(self.setup_frm,bd=0,bg="#4da6ff",activebackground="#000817",fg="white",activeforeground="white",padx="8",font=(('Segoe UI Light'), 11 ),text="Setup",command=lambda: self.setup_form()).pack(side=BOTTOM,pady=15)
        self.setup_frm.grid(row=0,column=0,sticky=N+S+E+W)
        self.setup_frm.tkraise()

    def setup_form(self):

        self.setup_form_frm = Frame(self.root,bg="#00264d")

        Label(self.setup_form_frm,text="School Details",bg="#00264d",fg="white",font=('Segoe UI Light',25,'normal'),anchor=W).pack(pady=20)

        self.form_frm = Frame(self.setup_form_frm,bg = "#00264d")

        Label(self.form_frm,text="School Name",bg="#00264d",fg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,sticky=W,pady=5,padx=5,columnspan=3)
        self.School_Name_box = LabelFrame(self.form_frm,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
        self.School_Name_Entry = Entry(self.School_Name_box,bd=0,font=('Segoe UI', 11),width=60)
        self.School_Name_Entry.pack(fill=BOTH,padx=4,ipady=3)
        self.School_Name_box.grid(row=1,column=0,pady=5,columnspan=4,sticky=NSEW)

        Label(self.form_frm,text="Address",bg="#00264d",fg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=2,column=0,sticky=W,pady=5,padx=5,columnspan=3)
        self.School_Address_box = LabelFrame(self.form_frm,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
        self.School_Address_Entry = Entry(self.School_Address_box,bd=0,font=('Segoe UI', 11),width=60)
        self.School_Address_Entry.pack(fill=BOTH,padx=4,ipady=3)
        self.School_Address_box.grid(row=3,column=0,pady=5,columnspan=4,sticky=NSEW)

        Label(self.form_frm,text="City",bg="#00264d",fg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=4,column=0,sticky=W,pady=15,padx=5)
        self.School_City_box = LabelFrame(self.form_frm,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
        self.School_City_Entry = Entry(self.School_City_box,bd=0,font=('Segoe UI', 11),width=20)
        self.School_City_Entry.pack(fill=BOTH,padx=4,ipady=3)
        self.School_City_box.grid(row=4,column=1,sticky=NSEW,pady=15)

        Label(self.form_frm,text="Pincode",bg="#00264d",fg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=4,column=2,sticky=W,pady=15,padx=5)
        self.School_Pincode_box = LabelFrame(self.form_frm,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
        self.School_Pincode_Entry = Entry(self.School_Pincode_box,bd=0,font=('Segoe UI', 11),width=20)
        self.School_Pincode_Entry.pack(fill=BOTH,padx=4,ipady=3)
        self.School_Pincode_box.grid(row=4,column=3,sticky=NSEW,pady=15)

        self.form_frm.pack(pady=35)
                
        Button(self.setup_form_frm,bd=0,bg="#4da6ff",activebackground="#000817",fg="white",activeforeground="white",font=(('Segoe UI Light'), 11 ),padx="8",text='Next',command=lambda: self.school_field_check()).pack(side=BOTTOM,padx=15,pady=15,anchor=E)
        self.setup_form_frm.grid(row=0,column=0,sticky=N+S+E+W)
        self.setup_form_frm.tkraise()

    def setup_admin(self):

        self.setup_admin_frm = Frame(self.root,bg="#00264d")

        Label(self.setup_admin_frm,text="Administrator",bg="#00264d",fg="white",font=('Segoe UI Light',25,'normal'),anchor=W).pack(pady=15)

        self.adm_form_frm = Frame(self.setup_admin_frm,bg = "#00264d")

        Label(self.adm_form_frm,text="Username",bg="#00264d",fg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,sticky=W,pady=5,padx=5)
        self.Username_box = LabelFrame(self.adm_form_frm,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
        self.Username = Entry(self.Username_box,bd=0,font=('Segoe UI', 11),width=45)
        self.Username.pack(fill=BOTH,padx=4,ipady=3)
        self.Username_box.grid(row=0,column=1,sticky=W,pady=5)

        Label(self.adm_form_frm,text="Password",bg="#00264d",fg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=1,column=0,sticky=W,pady=5,padx=5)
        self.Password_box = LabelFrame(self.adm_form_frm,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
        self.Password = Entry(self.Password_box,bd=0,font=('Segoe UI', 14),width=45,show=u"\u2022")
        self.Password.pack(fill=BOTH,padx=4,ipady=3)
        self.Password_box.grid(row=1,column=1,sticky=W,pady=5)

        Label(self.adm_form_frm,text="Confirm Password",bg="#00264d",fg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=2,column=0,sticky=W,pady=5,padx=5)
        self.CPassword_box = LabelFrame(self.adm_form_frm,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
        self.CPassword = Entry(self.CPassword_box,bd=0,font=('Segoe UI', 14),width=45,show=u"\u2022")
        self.CPassword.pack(fill=BOTH,padx=4,ipady=3)
        self.CPassword_box.grid(row=2,column=1,sticky=W,pady=5)
        
        self.adm_form_frm.pack()

        Label(self.setup_admin_frm,text="MySQL Server",bg="#00264d",fg="white",font=('Segoe UI Light',25,'normal'),anchor=W).pack(pady=15)

        self.sql_form_frm = Frame(self.setup_admin_frm,bg = "#00264d")

        Label(self.sql_form_frm,text="MySQL Username",bg="#00264d",fg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=4,column=0,sticky=W,pady=5,padx=5)
        self.MySQL_Username_box = LabelFrame(self.sql_form_frm,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
        self.MySQL_Username = Entry(self.MySQL_Username_box,bd=0,font=('Segoe UI', 11),width=45)
        self.MySQL_Username.pack(fill=BOTH,padx=4,ipady=3)
        self.MySQL_Username_box.grid(row=4,column=1,sticky=W,pady=5)

        Label(self.sql_form_frm,text="MySQL Password",bg="#00264d",fg="white",font=('Segoe UI',15,'normal'),anchor=W).grid(row=5,column=0,sticky=W,pady=5,padx=5)
        self.MySQL_Password_box = LabelFrame(self.sql_form_frm,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
        self.MySQL_Password = Entry(self.MySQL_Password_box,bd=0,font=('Segoe UI', 14),width=45,show=u"\u2022")
        self.MySQL_Password.pack(fill=BOTH,padx=4,ipady=3)
        self.MySQL_Password_box.grid(row=5,column=1,sticky=W,pady=5)

        self.Test_Button = Button(self.sql_form_frm,bd=0,bg="#4da6ff",activebackground="#000817",fg="white",activeforeground="white",font=(('Segoe UI Light'), 11 ),padx="8",text='Test Connection',command = lambda: self.mysql_test_conn())
        self.Test_Button.grid(row=6,column=1,sticky=E,pady=5)

        self.sql_form_frm.pack()

        self.Admin_next=Button(self.setup_admin_frm,bd=0,bg="#4da6ff",activebackground="#000817",fg="white",activeforeground="white",font=(('Segoe UI Light'), 11 ),padx="8",text='Next',state="disabled",command=lambda: self.Admin_field_check())
        self.Admin_next.pack(side=BOTTOM,padx=15,pady=15,anchor=E)
        self.setup_admin_frm.grid(row=0,column=0,sticky=N+S+E+W)

        self.setup_admin_frm.tkraise()

    def setting_up(self):

        self.settingup_frm = Frame(self.root,bg="#00264d")
        Label(self.settingup_frm,background="#00264D",foreground="#D9D9D9",font=(('Segoe UI Light'), 40 ),text="THANK YOU FOR CHOOSING\nDATAHIVE").pack(pady=80)
        Label(self.settingup_frm,background="#00264D",foreground="#D9D9D9",font=(('Segoe UI Light'), 20 ),text="SETTING UP YOUR SCHOOL").pack(pady=20)
        self.Finish_btn = Button(self.settingup_frm,bd=0,bg="#4da6ff",activebackground="#000817",fg="white",activeforeground="white",font=(('Segoe UI Light'), 11 ),state="disabled",padx="8",text='Finish',command=lambda: self.root.destroy())
        self.Finish_btn.pack(side=BOTTOM,padx=15,pady=15,anchor=E)

        self.bar=DoubleVar()
        self.bar.set(0)
        self.TProgressbar = ttk.Progressbar(self.settingup_frm, variable=self.bar, mode = 'determinate',style="TProgressbar")
        self.TProgressbar.pack(fill=X,expand=True,side=BOTTOM,padx=20)
        self.settingup_frm.grid(row=0,column=0,sticky=N+S+E+W)
        self.Loading = Label(self.settingup_frm,background="#00264D",foreground="#D9D9D9",font=(('Segoe UI Light'), 12 ),text="Loading...")
        self.Loading.pack(side=BOTTOM,anchor=SW,padx=20)
        self.settingup_frm.tkraise()
        self.Progressbar_update()

    def Admin_File(self):
        
        with open('FILE.bin', 'wb' ) as f :
            ID = encrypt(self.Username.get())
            Name = "Admin"
            Pass = encrypt(self.Password.get())
            Mail = encrypt('Encrypt')
            Gmail = encrypt('Datahive')
            d={'USERNAME' : ID , 'NAME' : Name , 'PASSWORD' : Pass}
            pickle.dump(d,f)
            d={'Mail':Mail , 'Gmail':Gmail}
            pickle.dump(d,f)

    def Progressbar_update(self):
        x = self.bar.get()
        self.bar.set(x+2)
        if x>=25:
            self.Admin_File()
        elif x>=50:
            with open("sql.bin","rb") as sql_file:
                d=pickle.load(sql_file)
                mydb = sql.connect(host="localhost",user=d["user"],passwd=d["passwd"],database="School_Manager",auth_plugin="mysql_native_password")
                cursor = mydb.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS School_Manager")
                cursor.execute("USE School_Manager")
                cursor.execute("CREATE TABLE IF NOT EXISTS LKG_UKG(ADMNO BIGINT PRIMARY KEY,FNAME CHAR(25),LNAME CHAR(25),EMIS BIGINT,CLASS CHAR(5),SECTION CHAR(2),DOB DATE,DOJ DATE,GENDER CHAR(7),NATIONALITY CHAR(10),MT CHAR(30),FATHERNAME CHAR(25),FATHERMOBILENO BIGINT,MOTHERNAME CHAR(25),MOTHERMOBILENO BIGINT,EMAILID CHAR(50),ADDRESS CHAR(200));")
                cursor.execute("CREATE TABLE IF NOT EXISTS I_VIII(ADMNO BIGINT PRIMARY KEY,FNAME CHAR(25),LNAME CHAR(25),EMIS BIGINT,CLASS CHAR(5),SECTION CHAR(2),DOB DATE,DOJ DATE,GENDER CHAR(7),NATIONALITY CHAR(10),MT CHAR(30),SECONDLANG CHAR(10),THIRDLANG CHAR(10),FATHERNAME CHAR(25),FATHERMOBILENO BIGINT,MOTHERNAME CHAR(25),MOTHERMOBILENO BIGINT,EMAILID CHAR(50),ADDRESS CHAR(200));")
                cursor.execute("CREATE TABLE IF NOT EXISTS IX_X(ADMNO BIGINT PRIMARY KEY,FNAME CHAR(25),LNAME CHAR(25),EMIS BIGINT,CLASS CHAR(5),SECTION CHAR(2),DOB DATE,DOJ DATE,GENDER CHAR(7),NATIONALITY CHAR(10),MT CHAR(30),SECONDLANG CHAR(10),FATHERNAME CHAR(25),FATHERMOBILENO BIGINT,MOTHERNAME CHAR(25),MOTHERMOBILENO BIGINT,EMAILID CHAR(50),ADDRESS CHAR(200));")
                cursor.execute("CREATE TABLE IF NOT EXISTS XI_XII(ADMNO BIGINT PRIMARY KEY,FNAME CHAR(25),LNAME CHAR(25),EMIS BIGINT,CLASS CHAR(5),SECTION CHAR(2),DOB DATE,DOJ DATE,GENDER CHAR(7),NATIONALITY CHAR(10),MT CHAR(30),COURSE CHAR(10),FATHERNAME CHAR(25),FATHERMOBILENO BIGINT,MOTHERNAME CHAR(25),MOTHERMOBILENO BIGINT,EMAILID CHAR(50),ADDRESS CHAR(200));")
                cursor.execute("CREATE TABLE IF NOT EXISTS TEACHERS(EMPNO BIGINT PRIMARY KEY,FNAME CHAR(25),LNAME CHAR(25),QUALIFICATION CHAR(30),DESIGNATION CHAR(30),SUBJECT CHAR(25),CT CHAR(5),CLASS CHAR(5),SECTION CHAR(2),DOB DATE,DOJ DATE,GENDER CHAR(7),AADHAR CHAR(16),PAN CHAR(11),MOBILENO BIGINT,EMAILID CHAR(50),ADDRESS CHAR(200));")
                cursor.execute("CREATE TABLE IF NOT EXISTS STAFFS(EMPNO BIGINT PRIMARY KEY,FNAME CHAR(25),LNAME CHAR(25),DESIGNATION CHAR(30),DOB DATE,DOJ DATE,GENDER CHAR(7),AADHAR CHAR(16),PAN CHAR(11),MOBILENO BIGINT,EMAILID CHAR(50),ADDRESS CHAR(200));")
                cursor.execute('''CREATE TABLE IF NOT EXISTS MARKS_LKG_UKG(ADMNO BIGINT PRIMARY KEY, MIDTERM_ENGLISH_THEORY BIGINT, QUATERLY_ENGLISH_THEORY BIGINT, HALFYEARLY_ENGLISH_THEORY BIGINT, ANNUAL_ENGLISH_THEORY BIGINT, MIDTERM_ENGLISH_INTERNAL BIGINT, QUATERLY_ENGLISH_INTERNAL BIGINT, HALFYEARLY_ENGLISH_INTERNAL BIGINT, ANNUAL_ENGLISH_INTERNAL BIGINT, MIDTERM_ENGLISH_TOTAL BIGINT, QUATERLY_ENGLISH_TOTAL BIGINT, HALFYEARLY_ENGLISH_TOTAL BIGINT, ANNUAL_ENGLISH_TOTAL BIGINT, MIDTERM_MATHEMATICS_THEORY BIGINT, QUATERLY_MATHEMATICS_THEORY BIGINT, HALFYEARLY_MATHEMATICS_THEORY BIGINT, ANNUAL_MATHEMATICS_THEORY BIGINT, MIDTERM_MATHEMATICS_INTERNAL BIGINT, QUATERLY_MATHEMATICS_INTERNAL BIGINT, HALFYEARLY_MATHEMATICS_INTERNAL BIGINT, ANNUAL_MATHEMATICS_INTERNAL BIGINT, MIDTERM_MATHEMATICS_TOTAL BIGINT, QUATERLY_MATHEMATICS_TOTAL BIGINT, HALFYEARLY_MATHEMATICS_TOTAL BIGINT, ANNUAL_MATHEMATICS_TOTAL BIGINT, MIDTERM_LANGUAGE_THEORY BIGINT, QUATERLY_LANGUAGE_THEORY BIGINT, HALFYEARLY_LANGUAGE_THEORY BIGINT, ANNUAL_LANGUAGE_THEORY BIGINT, MIDTERM_LANGUAGE_INTERNAL BIGINT, QUATERLY_LANGUAGE_INTERNAL BIGINT, HALFYEARLY_LANGUAGE_INTERNAL BIGINT, ANNUAL_LANGUAGE_INTERNAL BIGINT, MIDTERM_LANGUAGE_TOTAL BIGINT, QUATERLY_LANGUAGE_TOTAL BIGINT, HALFYEARLY_LANGUAGE_TOTAL BIGINT, ANNUAL_LANGUAGE_TOTAL BIGINT, MIDTERM_GENERAL_AWARENESS_THEORY BIGINT, QUATERLY_GENERAL_AWARENESS_THEORY BIGINT, HALFYEARLY_GENERAL_AWARENESS_THEORY BIGINT, ANNUAL_GENERAL_AWARENESS_THEORY BIGINT, MIDTERM_GENERAL_AWARENESS_INTERNAL BIGINT, QUATERLY_GENERAL_AWARENESS_INTERNAL BIGINT, HALFYEARLY_GENERAL_AWARENESS_INTERNAL BIGINT, ANNUAL_GENERAL_AWARENESS_INTERNAL BIGINT, MIDTERM_GENERAL_AWARENESS_TOTAL BIGINT, QUATERLY_GENERAL_AWARENESS_TOTAL BIGINT, HALFYEARLY_GENERAL_AWARENESS_TOTAL BIGINT, ANNUAL_GENERAL_AWARENESS_TOTAL BIGINT, MIDTERM_EVS_THEORY BIGINT, QUATERLY_EVS_THEORY BIGINT, HALFYEARLY_EVS_THEORY BIGINT, ANNUAL_EVS_THEORY BIGINT, MIDTERM_EVS_INTERNAL BIGINT, QUATERLY_EVS_INTERNAL BIGINT, HALFYEARLY_EVS_INTERNAL BIGINT, ANNUAL_EVS_INTERNAL BIGINT, MIDTERM_EVS_TOTAL BIGINT, QUATERLY_EVS_TOTAL BIGINT, HALFYEARLY_EVS_TOTAL BIGINT, ANNUAL_EVS_TOTAL BIGINT, MIDTERM_TOTAL BIGINT, QUATERLY_TOTAL BIGINT, HALFYEARLY_TOTAL BIGINT, ANNUAL_TOTAL BIGINT)''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS MARKS_I_VIII(ADMNO BIGINT PRIMARY KEY, MIDTERM_ENGLISH_THEORY BIGINT, QUATERLY_ENGLISH_THEORY BIGINT, HALFYEARLY_ENGLISH_THEORY BIGINT, ANNUAL_ENGLISH_THEORY BIGINT, MIDTERM_ENGLISH_INTERNAL BIGINT, QUATERLY_ENGLISH_INTERNAL BIGINT, HALFYEARLY_ENGLISH_INTERNAL BIGINT, ANNUAL_ENGLISH_INTERNAL BIGINT, MIDTERM_ENGLISH_TOTAL BIGINT, QUATERLY_ENGLISH_TOTAL BIGINT, HALFYEARLY_ENGLISH_TOTAL BIGINT, ANNUAL_ENGLISH_TOTAL BIGINT, MIDTERM_MATHEMATICS_THEORY BIGINT, QUATERLY_MATHEMATICS_THEORY BIGINT, HALFYEARLY_MATHEMATICS_THEORY BIGINT, ANNUAL_MATHEMATICS_THEORY BIGINT, MIDTERM_MATHEMATICS_INTERNAL BIGINT, QUATERLY_MATHEMATICS_INTERNAL BIGINT, HALFYEARLY_MATHEMATICS_INTERNAL BIGINT, ANNUAL_MATHEMATICS_INTERNAL BIGINT, MIDTERM_MATHEMATICS_TOTAL BIGINT, QUATERLY_MATHEMATICS_TOTAL BIGINT, HALFYEARLY_MATHEMATICS_TOTAL BIGINT, ANNUAL_MATHEMATICS_TOTAL BIGINT, MIDTERM_SOCIAL_SCIENCE_THEORY BIGINT, QUATERLY_SOCIAL_SCIENCE_THEORY BIGINT, HALFYEARLY_SOCIAL_SCIENCE_THEORY BIGINT, ANNUAL_SOCIAL_SCIENCE_THEORY BIGINT, MIDTERM_SOCIAL_SCIENCE_INTERNAL BIGINT, QUATERLY_SOCIAL_SCIENCE_INTERNAL BIGINT, HALFYEARLY_SOCIAL_SCIENCE_INTERNAL BIGINT, ANNUAL_SOCIAL_SCIENCE_INTERNAL BIGINT, MIDTERM_SOCIAL_SCIENCE_TOTAL BIGINT, QUATERLY_SOCIAL_SCIENCE_TOTAL BIGINT, HALFYEARLY_SOCIAL_SCIENCE_TOTAL BIGINT, ANNUAL_SOCIAL_SCIENCE_TOTAL BIGINT, MIDTERM_SCIENCE_THEORY BIGINT, QUATERLY_SCIENCE_THEORY BIGINT, HALFYEARLY_SCIENCE_THEORY BIGINT, ANNUAL_SCIENCE_THEORY BIGINT, MIDTERM_SCIENCE_INTERNAL BIGINT, QUATERLY_SCIENCE_INTERNAL BIGINT, HALFYEARLY_SCIENCE_INTERNAL BIGINT, ANNUAL_SCIENCE_INTERNAL BIGINT, MIDTERM_SCIENCE_TOTAL BIGINT, QUATERLY_SCIENCE_TOTAL BIGINT, HALFYEARLY_SCIENCE_TOTAL BIGINT, ANNUAL_SCIENCE_TOTAL BIGINT, MIDTERM_SECOND_LANGUAGE_THEORY BIGINT, QUATERLY_SECOND_LANGUAGE_THEORY BIGINT, HALFYEARLY_SECOND_LANGUAGE_THEORY BIGINT, ANNUAL_SECOND_LANGUAGE_THEORY BIGINT, MIDTERM_SECOND_LANGUAGE_INTERNAL BIGINT, QUATERLY_SECOND_LANGUAGE_INTERNAL BIGINT, HALFYEARLY_SECOND_LANGUAGE_INTERNAL BIGINT, ANNUAL_SECOND_LANGUAGE_INTERNAL BIGINT, MIDTERM_SECOND_LANGUAGE_TOTAL BIGINT, QUATERLY_SECOND_LANGUAGE_TOTAL BIGINT, HALFYEARLY_SECOND_LANGUAGE_TOTAL BIGINT, ANNUAL_SECOND_LANGUAGE_TOTAL BIGINT, MIDTERM_THIRD_LANGUAGE_THEORY BIGINT, QUATERLY_THIRD_LANGUAGE_THEORY BIGINT, HALFYEARLY_THIRD_LANGUAGE_THEORY BIGINT, ANNUAL_THIRD_LANGUAGE_THEORY BIGINT, MIDTERM_THIRD_LANGUAGE_INTERNAL BIGINT, QUATERLY_THIRD_LANGUAGE_INTERNAL BIGINT, HALFYEARLY_THIRD_LANGUAGE_INTERNAL BIGINT, ANNUAL_THIRD_LANGUAGE_INTERNAL BIGINT, MIDTERM_THIRD_LANGUAGE_TOTAL BIGINT, QUATERLY_THIRD_LANGUAGE_TOTAL BIGINT, HALFYEARLY_THIRD_LANGUAGE_TOTAL BIGINT, ANNUAL_THIRD_LANGUAGE_TOTAL BIGINT, MIDTERM_TOTAL BIGINT, QUATERLY_TOTAL BIGINT, HALFYEARLY_TOTAL BIGINT, ANNUAL_TOTAL BIGINT)''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS MARKS_IX_X(ADMNO BIGINT PRIMARY KEY, MIDTERM_ENGLISH_THEORY BIGINT, QUATERLY_ENGLISH_THEORY BIGINT, HALFYEARLY_ENGLISH_THEORY BIGINT, ANNUAL_ENGLISH_THEORY BIGINT, MIDTERM_ENGLISH_INTERNAL BIGINT, QUATERLY_ENGLISH_INTERNAL BIGINT, HALFYEARLY_ENGLISH_INTERNAL BIGINT, ANNUAL_ENGLISH_INTERNAL BIGINT, MIDTERM_ENGLISH_TOTAL BIGINT, QUATERLY_ENGLISH_TOTAL BIGINT, HALFYEARLY_ENGLISH_TOTAL BIGINT, ANNUAL_ENGLISH_TOTAL BIGINT, MIDTERM_MATHEMATICS_THEORY BIGINT, QUATERLY_MATHEMATICS_THEORY BIGINT, HALFYEARLY_MATHEMATICS_THEORY BIGINT, ANNUAL_MATHEMATICS_THEORY BIGINT, MIDTERM_MATHEMATICS_INTERNAL BIGINT, QUATERLY_MATHEMATICS_INTERNAL BIGINT, HALFYEARLY_MATHEMATICS_INTERNAL BIGINT, ANNUAL_MATHEMATICS_INTERNAL BIGINT, MIDTERM_MATHEMATICS_TOTAL BIGINT, QUATERLY_MATHEMATICS_TOTAL BIGINT, HALFYEARLY_MATHEMATICS_TOTAL BIGINT, ANNUAL_MATHEMATICS_TOTAL BIGINT, MIDTERM_SOCIAL_SCIENCE_THEORY BIGINT, QUATERLY_SOCIAL_SCIENCE_THEORY BIGINT, HALFYEARLY_SOCIAL_SCIENCE_THEORY BIGINT, ANNUAL_SOCIAL_SCIENCE_THEORY BIGINT, MIDTERM_SOCIAL_SCIENCE_INTERNAL BIGINT, QUATERLY_SOCIAL_SCIENCE_INTERNAL BIGINT, HALFYEARLY_SOCIAL_SCIENCE_INTERNAL BIGINT, ANNUAL_SOCIAL_SCIENCE_INTERNAL BIGINT, MIDTERM_SOCIAL_SCIENCE_TOTAL BIGINT, QUATERLY_SOCIAL_SCIENCE_TOTAL BIGINT, HALFYEARLY_SOCIAL_SCIENCE_TOTAL BIGINT, ANNUAL_SOCIAL_SCIENCE_TOTAL BIGINT, MIDTERM_SCIENCE_THEORY BIGINT, QUATERLY_SCIENCE_THEORY BIGINT, HALFYEARLY_SCIENCE_THEORY BIGINT, ANNUAL_SCIENCE_THEORY BIGINT, MIDTERM_SCIENCE_INTERNAL BIGINT, QUATERLY_SCIENCE_INTERNAL BIGINT, HALFYEARLY_SCIENCE_INTERNAL BIGINT, ANNUAL_SCIENCE_INTERNAL BIGINT, MIDTERM_SCIENCE_TOTAL BIGINT, QUATERLY_SCIENCE_TOTAL BIGINT, HALFYEARLY_SCIENCE_TOTAL BIGINT, ANNUAL_SCIENCE_TOTAL BIGINT, MIDTERM_SECOND_LANGUAGE_THEORY BIGINT, QUATERLY_SECOND_LANGUAGE_THEORY BIGINT, HALFYEARLY_SECOND_LANGUAGE_THEORY BIGINT, ANNUAL_SECOND_LANGUAGE_THEORY BIGINT, MIDTERM_SECOND_LANGUAGE_INTERNAL BIGINT, QUATERLY_SECOND_LANGUAGE_INTERNAL BIGINT, HALFYEARLY_SECOND_LANGUAGE_INTERNAL BIGINT, ANNUAL_SECOND_LANGUAGE_INTERNAL BIGINT, MIDTERM_SECOND_LANGUAGE_TOTAL BIGINT, QUATERLY_SECOND_LANGUAGE_TOTAL BIGINT, HALFYEARLY_SECOND_LANGUAGE_TOTAL BIGINT, ANNUAL_SECOND_LANGUAGE_TOTAL BIGINT, MIDTERM_TOTAL BIGINT, QUATERLY_TOTAL BIGINT, HALFYEARLY_TOTAL BIGINT, ANNUAL_TOTAL BIGINT)''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS MARKS_XI_XII(ADMNO BIGINT PRIMARY KEY, MIDTERM_ENGLISH_THEORY BIGINT, QUATERLY_ENGLISH_THEORY BIGINT, HALFYEARLY_ENGLISH_THEORY BIGINT, ANNUAL_ENGLISH_THEORY BIGINT, MIDTERM_ENGLISH_INTERNAL BIGINT, QUATERLY_ENGLISH_INTERNAL BIGINT, HALFYEARLY_ENGLISH_INTERNAL BIGINT, ANNUAL_ENGLISH_INTERNAL BIGINT, MIDTERM_ENGLISH_TOTAL BIGINT, QUATERLY_ENGLISH_TOTAL BIGINT, HALFYEARLY_ENGLISH_TOTAL BIGINT, ANNUAL_ENGLISH_TOTAL BIGINT, MIDTERM_MATHEMATICS_MARKETING_THEORY BIGINT, QUATERLY_MATHEMATICS_MARKETING_THEORY BIGINT, HALFYEARLY_MATHEMATICS_MARKETING_THEORY BIGINT, ANNUAL_MATHEMATICS_MARKETING_THEORY BIGINT, MIDTERM_MATHEMATICS_MARKETING_INTERNAL BIGINT, QUATERLY_MATHEMATICS_MARKETING_INTERNAL BIGINT, HALFYEARLY_MATHEMATICS_MARKETING_INTERNAL BIGINT, ANNUAL_MATHEMATICS_MARKETING_INTERNAL BIGINT, MIDTERM_MATHEMATICS_MARKETING_TOTAL BIGINT, QUATERLY_MATHEMATICS_MARKETING_TOTAL BIGINT, HALFYEARLY_MATHEMATICS_MARKETING_TOTAL BIGINT, ANNUAL_MATHEMATICS_MARKETING_TOTAL BIGINT, MIDTERM_CSC_EG_BIOLOGY_ACCOUNTANCY_THEORY BIGINT, QUATERLY_CSC_EG_BIOLOGY_ACCOUNTANCY_THEORY BIGINT, HALFYEARLY_CSC_EG_BIOLOGY_ACCOUNTANCY_THEORY BIGINT, ANNUAL_CSC_EG_BIOLOGY_ACCOUNTANCY_THEORY BIGINT, MIDTERM_CSC_EG_BIOLOGY_ACCOUNTANCY_INTERNAL BIGINT, QUATERLY_CSC_EG_BIOLOGY_ACCOUNTANCY_INTERNAL BIGINT, HALFYEARLY_CSC_EG_BIOLOGY_ACCOUNTANCY_INTERNAL BIGINT, ANNUAL_CSC_EG_BIOLOGY_ACCOUNTANCY_INTERNAL BIGINT, MIDTERM_CSC_EG_BIOLOGY_ACCOUNTANCY_TOTAL BIGINT, QUATERLY_CSC_EG_BIOLOGY_ACCOUNTANCY_TOTAL BIGINT, HALFYEARLY_CSC_EG_BIOLOGY_ACCOUNTANCY_TOTAL BIGINT, ANNUAL_CSC_EG_BIOLOGY_ACCOUNTANCY_TOTAL BIGINT, MIDTERM_CHEMISTRY_BUSINESS_STUDIES_THEORY BIGINT, QUATERLY_CHEMISTRY_BUSINESS_STUDIES_THEORY BIGINT, HALFYEARLY_CHEMISTRY_BUSINESS_STUDIES_THEORY BIGINT, ANNUAL_CHEMISTRY_BUSINESS_STUDIES_THEORY BIGINT, MIDTERM_CHEMISTRY_BUSINESS_STUDIES_INTERNAL BIGINT, QUATERLY_CHEMISTRY_BUSINESS_STUDIES_INTERNAL BIGINT, HALFYEARLY_CHEMISTRY_BUSINESS_STUDIES_INTERNAL BIGINT, ANNUAL_CHEMISTRY_BUSINESS_STUDIES_INTERNAL BIGINT, MIDTERM_CHEMISTRY_BUSINESS_STUDIES_TOTAL BIGINT, QUATERLY_CHEMISTRY_BUSINESS_STUDIES_TOTAL BIGINT, HALFYEARLY_CHEMISTRY_BUSINESS_STUDIES_TOTAL BIGINT, ANNUAL_CHEMISTRY_BUSINESS_STUDIES_TOTAL BIGINT, MIDTERM_PHYSICS_ECONOMICS_THEORY BIGINT, QUATERLY_PHYSICS_ECONOMICS_THEORY BIGINT, HALFYEARLY_PHYSICS_ECONOMICS_THEORY BIGINT, ANNUAL_PHYSICS_ECONOMICS_THEORY BIGINT, MIDTERM_PHYSICS_ECONOMICS_INTERNAL BIGINT, QUATERLY_PHYSICS_ECONOMICS_INTERNAL BIGINT, HALFYEARLY_PHYSICS_ECONOMICS_INTERNAL BIGINT, ANNUAL_PHYSICS_ECONOMICS_INTERNAL BIGINT, MIDTERM_PHYSICS_ECONOMICS_TOTAL BIGINT, QUATERLY_PHYSICS_ECONOMICS_TOTAL BIGINT, HALFYEARLY_PHYSICS_ECONOMICS_TOTAL BIGINT, ANNUAL_PHYSICS_ECONOMICS_TOTAL BIGINT, MIDTERM_TOTAL BIGINT, QUATERLY_TOTAL BIGINT, HALFYEARLY_TOTAL BIGINT, ANNUAL_TOTAL BIGINT)''')
                mydb.close()
        if x>=75:
            self.school_details()
        if x>=80:
            RECORDS("Admin" , self.Username.get(), "Admin", "Admin", self.Username.get())
        if x<100:
            self.root.after(200,lambda:self.Progressbar_update())
        else:
            self.bar.set(100)
            self.Finish_btn.config(state="normal")
            self.Loading.config(text="Completed")

    def mysql_test_conn(self):
        try:
            db=sql.connect(host="localhost",user=self.MySQL_Username.get(),passwd=self.MySQL_Password.get())
            if db.is_connected():
                messagebox.showinfo("DataHIVE","MySQL Connection Successful")
                db.close()
                self.Admin_next.config(state="normal")
                with open("sql.bin","wb") as sql_file:
                    pickle.dump({"user":self.MySQL_Username.get(),"passwd":self.MySQL_Password.get()},sql_file)
        except:
            messagebox.showerror("DataHIVE","MySQL Connection NOT Successful")
        
    def school_details(self):
        with open("School_details.txt","w") as school_file:
            school_file.write(self.School_Name_Entry.get()+"\n")
            school_file.write(self.School_Address_Entry.get()+"\n")
            school_file.write(self.School_City_Entry.get()+"\n")
            school_file.write(self.School_Pincode_Entry.get()+"\n")

    def school_field_check(self):
        if self.School_Name_Entry.get() == "":
            messagebox.showerror("DataHIVE","Enter School Name")
        elif self.School_Address_Entry.get() == "":
            messagebox.showerror("DataHIVE","Enter Address")
        elif self.School_City_Entry.get() == "":
            messagebox.showerror("DataHIVE","Enter City")
        elif self.School_Pincode_Entry.get() == "":
            messagebox.showerror("DataHIVE","Enter Pincode")
        else:
            self.setup_admin()

    def Admin_field_check(self):
        if self.Username.get() == "":
            messagebox.showerror("DataHIVE","Enter Admin Username")
        elif self.Password.get() == "":
            messagebox.showerror("DataHIVE","Enter Admin Password")
        elif self.CPassword.get() == "":
            messagebox.showerror("DataHIVE","Enter Confirm Password")
        elif self.Password.get() != self.CPassword.get():
            messagebox.showerror("DataHIVE","Password Doesn't Match")
        else:
            self.setting_up()

if __name__ == "__main__":
    root = Tk()
    School_Setup(root)
    root.mainloop()





