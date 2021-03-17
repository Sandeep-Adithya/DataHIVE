from logging import RootLogger
from tkinter import *
from tkinter import ttk
import ctypes
import pickle
import base64
from tkinter import messagebox
import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email import encoders
import mysql.connector as sql
import random
import csv
import tkmain_admin
import tkmain_student
import tkmain_teacher 
import os
import datetime

width, height = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
with open("sql.bin","rb") as sql_file:
    d=pickle.load(sql_file)
    mydb = sql.connect(host="localhost",user=d["user"],passwd=d["passwd"],database="School_Manager",auth_plugin="mysql_native_password")
mycur = mydb.cursor()

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

def Gmail() :
    with open('FILE.bin' , 'rb') as File_Open :
        while True :
            try :
                Data = pickle.load(File_Open)
                try :
                    if decrypt(Data['Mail']) == 'Encrypt' :
                        return decrypt(Data['Gmail'])
                except :
                    pass
            except :
                break

def Admin_Auth_Mail(Username , Designation, ID) :
    sender_email = "datahive.pixeldata.corp@gmail.com"
    sender_name = "DataHIVE"
    email_html = open('Mail_Admin.html')
    email_body = email_html.read()
    with open("FILE.bin",'rb') as File:
        DATA = pickle.load(File)
        Receiver_Mail = decrypt(DATA['USERNAME'])
        Receiver_Name = "Admin"

    print("Sending the email...")
    msg = MIMEMultipart()
    msg['To'] = formataddr((Receiver_Name, Receiver_Mail))
    msg['From'] = formataddr((sender_name, sender_email))
    msg['Subject'] = 'New Admission'
    if Designation == "Students":
        msg.attach(MIMEText(email_body.format("Student",Username,"Admission Number",ID), 'html'))
    elif Designation == "Teachers":
        msg.attach(MIMEText(email_body.format("Teacher",Username,"Employee Number",ID), 'html'))
    else :
        print("[Fatal Error]")
    try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            context = ssl.create_default_context()
            server.starttls(context=context)
            server.login(sender_email, Gmail())
            server.sendmail(sender_email, Receiver_Mail, msg.as_string())
            print('Email sent!')
    except Exception as e:
            print(f'Oh no! Something bad happened!n{e}')
    finally:
            print('Closing the server...')
            server.quit()

def Create_Mail(Receiver_Mail , Receiver_Name) :
    '''Sends Welcome Email'''
    sender_email = "datahive.pixeldata.corp@gmail.com"
    sender_name = "DataHIVE"
    email_html = open('Creation_Mail.html')
    email_body = email_html.read().format(Receiver_Name)
    print("Sending the email...")
    msg = MIMEMultipart()
    msg['To'] = formataddr((Receiver_Name, Receiver_Mail))
    msg['From'] = formataddr((sender_name, sender_email))
    msg['Subject'] = 'Welcome to DataHIVE '+Receiver_Name
    msg.attach(MIMEText(email_body, 'html'))
    try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            context = ssl.create_default_context()
            server.starttls(context=context)
            server.login(sender_email, Gmail())
            server.sendmail(sender_email, Receiver_Mail, msg.as_string())
            print('Email sent!')
    except Exception as e:
            print(f'Oh no! Something bad happened!n{e}')
    finally:
            print('Closing the server...')
            server.quit()

def Reset_Mail(Receiver_Mail , Receiver_Name) :
    '''Sends OTP Email for Forget Password'''
    sender_email = "datahive.pixeldata.corp@gmail.com"
    sender_name = "DataHIVE"
    email_html = open('Mail_OTP.html')
    sixnum = ''
    for i in range(6):
        sixnum += str(random.randint(0, 9))
    OTP = sixnum
    email_body = email_html.read().format(OTP)
    print("Sending the email...")
    msg = MIMEMultipart()
    msg['To'] = formataddr((Receiver_Name, Receiver_Mail))
    msg['From'] = formataddr((sender_name, sender_email))
    msg['Subject'] = 'Request for password Reset'
    msg.attach(MIMEText(email_body.format(Name=Receiver_Name), 'html'))
    try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            context = ssl.create_default_context()
            server.starttls(context=context)
            server.login(sender_email, Gmail())
            server.sendmail(sender_email, Receiver_Mail, msg.as_string())
            print('Email sent!')
    except Exception as e:
            print(f'Oh no! Something bad happened!n{e}')
    finally:
            print('Closing the server...')
            server.quit()
            return OTP

def TEMPORARY_FILE(Username) :
    with open('USER-RECORDS.csv' , 'r') as File_Open :
        CSV_FILE_READER = csv.reader(File_Open)
        FIELDS = next(CSV_FILE_READER)
        for row in CSV_FILE_READER :
            DICT = {}
            for Loop in range(len(row)) :
                DICT[FIELDS[Loop]] = row[Loop]
            if DICT['USERNAME'] == Username or DICT['ID'] == Username :
                with open('TEMPORARY.txt','w') as Temp_File_Open :
                    Temp_File_Open.write(DICT['ID'] + ',' + DICT['USERNAME'] + ',' + DICT['EMAIL'] + ',' + DICT['NAME'])

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

def New_Login(Username , ID , Password , Designation , SQL_List): 
    print(SQL_List)
    print(ID)
    if Username != SQL_List[1]:
        if Designation == 'Students' :
            if messagebox.askyesno('DATAHIVE','Admission Number not Found\nDo you want to request Admin for authentication') :
                Admin_Auth_Mail(Username,Designation,ID)
        else :
            if messagebox.askyesno('DATAHIVE','Employee number not Found\nDo you want to request Admin for authentication') :
                pass
                Admin_Auth_Mail(Username,Designation,ID)
    elif int(ID) == SQL_List[0] :
        Username = encrypt(Username)
        Password = encrypt(Password)
        ID = encrypt(ID)
        File_Present_Check = 'NO'
        DATA = {'USERNAME':Username , 'ID':ID , 'PASSWORD':Password }
        if Designation == 'Students' :
            _File = 'Login_authentication_St.bin'
        elif Designation == 'Teachers' or Designation == 'Staffs' :
            _File = 'Login_authentication_Ts.bin'
        else :
            print('[Fatal Error] : Designation Not Found !')
            return False
        for File in os.listdir():
            if File == _File:
                File_Present_Check = 'YES'
                with open(File ,'ab') as File_Open:
                    pickle.dump(DATA , File_Open)
                RECORDS(decrypt(ID),decrypt(Username),SQL_List[2]+" "+SQL_List[3],Designation,SQL_List[1])
                TEMPORARY_FILE(decrypt(Username))
                Create_Mail(SQL_List[1] , SQL_List[2]+" "+SQL_List[3])
                messagebox.showinfo("DataHIVE","Your Account Has Been Created\nLogin with your Username and Passsword")
                    
        if File_Present_Check == 'NO':
            with open(_File , 'wb') as File_Open:
                pickle.dump(DATA , File_Open)
            RECORDS(decrypt(ID),decrypt(Username),SQL_List[2]+" "+SQL_List[3],Designation,SQL_List[1])
            TEMPORARY_FILE(decrypt(Username))
            Create_Mail(SQL_List[1] , SQL_List[2]+" "+SQL_List[3])
            messagebox.showinfo("DataHIVE","Your Account Has Been Created\nLogin with your Username and Passsword")
    else:
        if Designation == 'Students' :
            if messagebox.askyesno('DATAHIVE','Admission Number not Found\nDo you want to request Admin for authentication') :
                Admin_Auth_Mail(Username,Designation,ID)
        else :
            if messagebox.askyesno('DATAHIVE','Employee number not Found\nDo you want to request Admin for authentication') :
                Admin_Auth_Mail(Username,Designation,ID)

def User_Check(Username , Designation):
    if Designation == 'Students' :
        _File = 'Login_authentication_St.bin'
    elif Designation == 'Teachers' :
        _File = 'Login_authentication_Ts.bin'
    else :
        print('[Fatal Error] : Designation Not Found !')
        return False
    try:
        with open(_File,'rb') as File_Open:
            try:
                while True:
                    DATA = pickle.load(File_Open)
                    if decrypt(DATA['USERNAME']) == Username :
                        return True 
            except:
                return False
    except:
        False

def User_Check_Forgot(Username):
    for Designation in ['Students','Teachers']:
        if Designation == 'Students' :
            _File = 'Login_authentication_St.bin'
        elif Designation == 'Teachers' :
            _File = 'Login_authentication_Ts.bin'
        else :
            print('[Fatal Error] : Designation Not Found !')
            return False
        try:
            with open(_File,'rb') as File_Open:
                try:
                    while True:
                        DATA = pickle.load(File_Open)
                        if decrypt(DATA['USERNAME']) == Username :
                            return True,Designation
                            break
                except:
                    return False
        except:
            False

def Login_Authenticate(Username_ID , Password):
    Files = [ 'Login_authentication_St.bin' , 'Login_authentication_Ts.bin' , 'FILE.bin']
    for File in Files :
        try:
            with open(File,'rb') as File_Open:        
                try:
                    while True:
                        DATA , LOGIN_ERROR = pickle.load(File_Open) , True
                        try :
                            if decrypt(DATA['USERNAME']) == Username_ID or decrypt(DATA['ID']) == Username_ID :
                                if decrypt(DATA['PASSWORD']) == Password :
                                    if File != "FILE.bin":
                                        TEMPORARY_FILE(Username_ID)
                                    LOGIN_ERROR = False                          
                                    return [True , File]
                        except :
                            pass
                except:                        
                    pass
        except:
            pass
    else:
        if LOGIN_ERROR == True:
            return [False]

def close_window():
    if messagebox.askyesno("DATAHIVE","Are you sure? Do you want to exit"):
        root.destroy()
    else:
        pass

def call_logout():
    global root
    root=Tk()
    Login_UI(root)

class Login_UI:
    def __init__(self, root):
        self.root=root
        self.root.geometry("740x490+"+str(int((width/2)-340))+"+"+str(int((height/2)-275)))
        self.root.resizable(0, 0)
        self.root.title("DATAHIVE School Manager - Login")
        self.root.configure(background="#d9d9d9")

        style_config = ttk.Style()
        try:
            style_config.theme_create( "Custom_theme", parent="classic", settings={
            "TNotebook": {
                "configure": {"background": "#4da6ff","borderwidth": 0,"bordercolor":"#1CBAE9" ,"relief":"flat", "tabmargins": [0, 0, 10, 0] }},
            "TNotebook.Tab": {
                "configure": {"background": "#4da6ff", "foreground": '#00264d', "padding": 10, "borderwidth": 0},
                "map":       {"background": [("selected", "#00264d")],
                            "foreground": [("selected", "white")],
                            "expand": [("selected", [0, 0, 0, 0])]
                            } } } )
        except:
            pass
        style_config.theme_use('Custom_theme')

        self.username=StringVar()

        self.Frame1 = Frame(self.root,width=270,background="#00264d")
        self.Frame1.pack(side= LEFT,fill= BOTH)
        self.logo_img = PhotoImage(file = "icons\\logo-welcome.png")
        self.logo =  Label(self.Frame1,image=self.logo_img,background="#00264d")
        self.logo.img=self.logo_img
        self.logo.pack(fill= BOTH,padx=15,pady=30)
        Label(self.Frame1,text="DATA HIVE",font=(('Segoe UI Light'), 25 ),fg='#d9d9d9',bg='#00264d').pack()
        Label(self.Frame1,text="School Manager",font=(('Segoe UI'), 15 ),fg='#d9d9d9',bg='#00264d').pack()
        self.Frame2 =  Frame(self.root,background="#4da6ff")
        self.Frame2.pack(side= LEFT,fill= BOTH,expand=True)
        self.Frame2.grid_rowconfigure(0, weight=1)
        self.Frame2.grid_columnconfigure(0, weight=1)
        
        self.Login_Frame = Frame(self.Frame2,background="#4da6ff")
        Label(self.Login_Frame,text="Login",font=(('Segoe UI Light'), 25 ),fg='#00264d',bg='#4da6ff').pack(pady=25)
        Label(self.Login_Frame,text="Username",bg="#4da6ff",font=('Segoe UI',15,'normal'),anchor=W).pack(anchor=W,padx=40,pady=15)
        self.Username_box = LabelFrame(self.Login_Frame,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
        self.Username_l = Entry(self.Username_box,bd=0,font=('Segoe UI', 11),width=45,textvariable=self.username)
        self.Username_l.pack(fill=BOTH,padx=4,ipady=3)
        self.Username_box.pack(anchor=W,padx=45)
        Label(self.Login_Frame,text="Password",bg="#4da6ff",font=('Segoe UI',15,'normal'),anchor=W).pack(anchor=W,padx=40,pady=15)
        self.Password_box = LabelFrame(self.Login_Frame,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
        self.Password_l = Entry(self.Password_box,bd=0,font=('Segoe UI', 14),width=45,show=u"\u2022")
        self.Password_l.pack(fill=BOTH,padx=4,ipady=3)
        self.Password_box.pack(anchor=W,padx=45)
        Button(self.Login_Frame,text="Forgot Password",font=('Segoe UI',11,'normal'),width=15,height=1,bd=0,bg="#00264d",activeforeground="white",activebackground="#000817",fg="white",cursor="arrow",command=lambda: self.fgtpwd_frm.tkraise()).pack(pady=5,padx=45,anchor=E)
        self.Login_Frm_btn =  Frame(self.Login_Frame,bg="#4da6ff",height=20)
        Button(self.Login_Frm_btn,text="New User",font=('Segoe UI',11,'normal'),width=15,height=1,bd=0,bg="#00264d",activeforeground="white",activebackground="#000817",fg="white",cursor="arrow",command=lambda: self.New_User_Frame.tkraise()).pack(side=LEFT,padx=6)
        Button(self.Login_Frm_btn,text="Login",font=('Segoe UI',11,'normal'),width=15,height=1,bd=0,bg="#00264d",activeforeground="white",activebackground="#000817",fg="white",cursor="arrow",command=lambda: self.Login_User()).pack(side=LEFT,padx=6)
        self.Login_Frm_btn.pack(side=BOTTOM,pady=20)
        self.Login_Frame.grid(row=0,column=0,sticky=NSEW)

        self.New_User_Frame =  Frame(self.Frame2,background="#4da6ff")
        self.New_User_Frame.grid(row=0,column=0,sticky=NSEW)
        Label(self.New_User_Frame,text="New User",font=(('Segoe UI Light'), 25 ),fg='#00264d',bg='#4da6ff').pack(pady=5)

        self.TNotebook = ttk.Notebook(self.New_User_Frame,style="TNotebook")
        self.TNotebook.pack(fill= BOTH,expand=True,padx=5)
        self.TNotebook.configure(takefocus="")

        self.Student_User = Frame(self.TNotebook,background="#4da6ff")
        self.TNotebook.add(self.Student_User, padding=3)
        self.TNotebook.tab(0, text="Students",compound="left",underline="1")
        
        Label(self.Student_User,text="Username",bg="#4da6ff",font=('Segoe UI',15,'normal'),anchor=W).pack(anchor=W,padx=40,pady=15)
        self.Username_box = LabelFrame(self.Student_User,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
        self.Username_s = Entry(self.Username_box,bd=0,font=('Segoe UI', 11),width=45,textvariable=self.username)
        self.Username_s.pack(fill=BOTH,padx=4,ipady=3)
        self.Username_box.pack(anchor=W,padx=45)
        Label(self.Student_User,text="Admission Number",bg="#4da6ff",font=('Segoe UI',15,'normal'),anchor=W).pack(anchor=W,padx=40,pady=15)
        self.Admno_box = LabelFrame(self.Student_User,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
        self.Admno = Entry(self.Admno_box,bd=0,font=('Segoe UI', 11),width=45)
        self.Admno.pack(fill=BOTH,padx=4,ipady=3)
        self.Admno_box.pack(anchor=W,padx=45)
        Label(self.Student_User,text="Password",bg="#4da6ff",font=('Segoe UI',15,'normal'),anchor=W).pack(anchor=W,padx=40,pady=15)
        self.Password_box = LabelFrame(self.Student_User,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
        self.Password_s = Entry(self.Password_box,bd=0,font=('Segoe UI', 14),width=45,show=u"\u2022")
        self.Password_s.pack(fill=BOTH,padx=4,ipady=3)
        self.Password_box.pack(anchor=W,padx=45)

        self.Teachers_User = Frame(self.TNotebook,background="#4da6ff")
        self.TNotebook.add(self.Teachers_User, padding=3)
        self.TNotebook.tab(1, text="Teachers",compound="left",underline="1",)

        Label(self.Teachers_User,text="Username",bg="#4da6ff",font=('Segoe UI',15,'normal'),anchor=W).pack(anchor=W,padx=40,pady=15)
        self.Username_box = LabelFrame(self.Teachers_User,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
        self.Username_t = Entry(self.Username_box,bd=0,font=('Segoe UI', 11),width=45,textvariable=self.username)
        self.Username_t.pack(fill=BOTH,padx=4,ipady=3)
        self.Username_box.pack(anchor=W,padx=45)
        Label(self.Teachers_User,text="Employee Number",bg="#4da6ff",font=('Segoe UI',15,'normal'),anchor=W).pack(anchor=W,padx=40,pady=15)
        self.Empno_box = LabelFrame(self.Teachers_User,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
        self.Empno_t = Entry(self.Empno_box,bd=0,font=('Segoe UI', 11),width=45)
        self.Empno_t.pack(fill=BOTH,padx=4,ipady=3)
        self.Empno_box.pack(anchor=W,padx=45)
        Label(self.Teachers_User,text="Password",bg="#4da6ff",font=('Segoe UI',15,'normal'),anchor=W).pack(anchor=W,padx=40,pady=15)
        self.Password_box = LabelFrame(self.Teachers_User,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
        self.Password_t = Entry(self.Password_box,bd=0,font=('Segoe UI', 14),width=45,show=u"\u2022")
        self.Password_t.pack(fill=BOTH,padx=4,ipady=3)
        self.Password_box.pack(anchor=W,padx=45)

        self.Frame3 =  Frame(self.New_User_Frame,bg="#4da6ff")
        Button(self.Frame3,text="Back",font=('Segoe UI',11,'normal'),width=15,height=1,bd=0,bg="#00264d",activeforeground="white",activebackground="#000817",fg="white",cursor="arrow",command=lambda: self.Login_Frame.tkraise()).grid(row=0,column=0,padx=6,sticky=N+S+W+E)
        Button(self.Frame3,text="Create User",font=('Segoe UI',11,'normal'),width=15,height=1,bd=0,bg="#00264d",activeforeground="white",activebackground="#000817",fg="white",cursor="arrow",command=lambda: self.create_user()).grid(row=0,column=1,padx=6,sticky=N+S+W+E)
        self.Frame3.pack(side=BOTTOM,pady=20)

        self.fgtpwd_frm =  Frame(self.Frame2,background="#4da6ff")
        self.fgtpwd_frm.grid(row=0,column=0,sticky=NSEW)
        Label(self.fgtpwd_frm,text="Forgot Password",font=(('Segoe UI Light'), 25 ),fg='#00264d',bg='#4da6ff').pack(pady=5)

        Label(self.fgtpwd_frm,text="Username",bg="#4da6ff",font=('Segoe UI',15,'normal'),anchor=W).pack(anchor=W,padx=40,pady=10)
        self.Username_box = LabelFrame(self.fgtpwd_frm,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
        self.Username_f = Entry(self.Username_box,bd=0,font=('Segoe UI', 11),width=45,textvariable=self.username)
        self.Username_f.pack(fill=BOTH,padx=4,ipady=3)
        self.Username_box.pack(anchor=W,padx=45)
        self.send_otp=Button(self.fgtpwd_frm,text="Send OTP",font=('Segoe UI',11,'normal'),width=15,height=1,bd=0,bg="#00264d",activeforeground="white",activebackground="#000817",fg="white",cursor="arrow",command=lambda: self.get_otp())
        self.send_otp.pack(anchor=E,pady=5,padx=45)
        
        self.Frame3 =  Frame(self.fgtpwd_frm,bg="#4da6ff")
        Button(self.Frame3,text="Back",font=('Segoe UI',11,'normal'),width=15,height=1,bd=0,bg="#00264d",activeforeground="white",activebackground="#000817",fg="white",cursor="arrow",command=lambda: self.forgot_back()).grid(row=0,column=0,padx=6,sticky=N+S+W+E)
        self.Frame3.pack(side=BOTTOM,pady=20)

        self.Login_Frame.tkraise()

    def get_otp(self):
        with open('USER-RECORDS.csv' , 'r') as File_Open :
            CSV_FILE_READER = csv.reader(File_Open)
            FIELDS = next(CSV_FILE_READER)
            for row in CSV_FILE_READER :
                DICT = {}
                for Loop in range(len(row)) :
                    DICT[FIELDS[Loop]] = row[Loop]
                if DICT['USERNAME'] == self.Username_f.get():
                    self.otp_lbl=Label(self.fgtpwd_frm,text="One Time Passcode",bg="#4da6ff",font=('Segoe UI',15,'normal'),anchor=W)
                    self.otp_lbl.pack(anchor=W,padx=40,pady=10)
                    self.OTP_box = LabelFrame(self.fgtpwd_frm,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
                    self.OTP = Entry(self.OTP_box,bd=0,font=('Segoe UI', 11),width=45)
                    self.OTP.pack(fill=BOTH,padx=4,ipady=3)
                    self.OTP_box.pack(anchor=W,padx=45)
                    self.ver_otp=Button(self.fgtpwd_frm,text="Verify",font=('Segoe UI',11,'normal'),width=15,height=1,bd=0,bg="#00264d",activeforeground="white",activebackground="#000817",fg="white",cursor="arrow",command=lambda: self.verify_otp())
                    self.ver_otp.pack(anchor=E,pady=5,padx=45)
                    self.OTP_number=Reset_Mail(self.Username_f.get(),DICT['NAME'])
                    messagebox.showinfo("DataHIVE","OTP has been sent to your email")
                    self.send_otp.config(state="disabled")
                    break
            else:
                messagebox.showinfo("DataHIVE","Username not found")

    def verify_otp(self):
        if self.OTP.get() == self.OTP_number:
            messagebox.showinfo("DataHIVE","OTP has been verified. Enter a new password")
            self.pwd_frm = Frame(self.fgtpwd_frm,bg="#4da6ff")
            Label(self.pwd_frm,text="New Password",bg="#4da6ff",font=('Segoe UI',15,'normal'),anchor=W).grid(row=0,column=0,pady=2,sticky=NSEW)
            self.np_box = LabelFrame(self.pwd_frm,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
            self.np = Entry(self.np_box,bd=0,font=('Segoe UI', 14),width=45,show=u"\u2022")
            self.np.pack(fill=BOTH,padx=4,ipady=3)
            self.np_box.grid(row=0,column=1,padx=4,pady=2)
            Label(self.pwd_frm,text="Confirm Password",bg="#4da6ff",font=('Segoe UI',15,'normal'),anchor=W).grid(row=1,column=0,pady=2,sticky=NSEW)
            self.cp_box = LabelFrame(self.pwd_frm,bd=0,highlightthickness=2,highlightcolor="#00264d",bg="white")
            self.cp = Entry(self.cp_box,bd=0,font=('Segoe UI', 14),width=45,show=u"\u2022")
            self.cp.pack(fill=BOTH,padx=4,ipady=3)
            self.cp_box.grid(row=1,column=1,padx=4,pady=2)
            self.pwd_frm.pack(padx=45,pady=10)
            self.ch_pwd_btn=Button(self.Frame3,text="Change Password",font=('Segoe UI',11,'normal'),width=19,height=1,bd=0,bg="#00264d",activeforeground="white",activebackground="#000817",fg="white",cursor="arrow",command=lambda: self.change_pwd())
            self.ch_pwd_btn.grid(row=0,column=1,padx=6,sticky=N+S+W+E)
            self.ver_otp.config(state="disabled")
        else:
            messagebox.showinfo("DataHIVE","OTP Doesn't Match")

    def change_pwd(self):
        if self.np.get()==self.cp.get():    
            check, Designation = User_Check_Forgot(self.Username_f.get())
            if check:
                if Designation == "Students":
                    _FILE='Login_authentication_St.bin'
                elif Designation == "Teachers":
                    _FILE='Login_authentication_Ts.bin'
                with open(_FILE,'rb') as File_Open:
                        with open('Login_Temp.bin','wb') as Temp_Open:
                            try:
                                while True:
                                    DATA , Email_ID = pickle.load(File_Open) , self.Username_f.get()
                                    if  decrypt(DATA['USERNAME']) == Email_ID :
                                        DATA['PASSWORD'] = encrypt(self.cp.get())
                                        pickle.dump(DATA,Temp_Open)
                                    else:
                                        pickle.dump(DATA,Temp_Open)
                            except:
                                pass
                os.remove(_FILE)
                os.rename('Login_Temp.bin',_FILE)
                self.send_otp.config(state="normal")
                self.pwd_frm.destroy()
                self.ch_pwd_btn.destroy()
                self.otp_lbl.destroy()
                self.OTP_box.destroy()
                self.ver_otp.destroy()
                self.Login_Frame.tkraise()
                messagebox.showinfo("DataHIVE","Your Password Has Been Changed\nLogin with your new Passsword")
        else:
            messagebox.showinfo("DataHIVE","Password Doesn't Match")

    def forgot_back(self):
        self.send_otp.config(state="normal")
        try:
            self.otp_lbl.destroy()
            self.OTP_box.destroy()
            self.ver_otp.destroy()
        except:
            pass
        try:
            self.pwd_frm.destroy()
            self.ch_pwd_btn.destroy()
        except:
            pass
        self.Login_Frame.tkraise()
    
    def create_user(self):
        sel=self.TNotebook.tab(self.TNotebook.select(), "text")
        print(sel)
        if User_Check(self.Username_s.get(),sel):
            messagebox.showerror("DATAHIVE","User Already Exists")
        else:
            if sel == "Students":
                if self.Username_s.get()=="":
                    messagebox.showerror("DATAHIVE","Please Enter Username")
                elif self.Admno.get()=="":
                    messagebox.showerror("DATAHIVE","Please Enter Admission Number")
                elif self.Password_s.get()=="":
                    messagebox.showerror("DATAHIVE","Please Enter Password")
                elif self.Username_s.get()==self.Admno.get():
                    messagebox.showerror("DATAHIVE","Username and Admission Number Cannot be Same")
                else:
                    sdata=[]
                    mycur.execute('SELECT ADMNO, EMAILID, FNAME, LNAME FROM LKG_UKG WHERE ADMNO = {}'.format(self.Admno.get()))
                    sdata+=list(mycur.fetchall())
                    mycur.execute('SELECT ADMNO, EMAILID, FNAME, LNAME FROM I_VIII WHERE ADMNO = {}'.format(self.Admno.get()))
                    sdata+=list(mycur.fetchall())
                    mycur.execute('SELECT ADMNO, EMAILID, FNAME, LNAME FROM IX_X WHERE ADMNO = {}'.format(self.Admno.get()))
                    sdata+=list(mycur.fetchall())
                    mycur.execute('SELECT ADMNO, EMAILID, FNAME, LNAME FROM XI_XII WHERE ADMNO = {}'.format(self.Admno.get()))
                    sdata+=list(mycur.fetchall())
                    if sdata == []:
                        if messagebox.askyesno('DATAHIVE','Admission Number not Found\nDo you want to request Admin for authentication') :
                            Admin_Auth_Mail(self.Username_s.get(),"Students", self.Admno.get())
                    elif self.Username_s.get() != sdata[0][1]:
                        if messagebox.askyesno('DATAHIVE','Admission Number not Found\nDo you want to request Admin for authentication') :
                            Admin_Auth_Mail(self.Username_s.get(),"Students", self.Admno.get())
                    elif sdata != []:
                        New_Login(self.Username_s.get() , self.Admno.get() , self.Password_s.get() , sel , sdata[0])
                        self.Login_Frame.tkraise()
            elif sel == "Teachers":
                if self.Username_t.get()=="":
                    messagebox.showerror("DATAHIVE","Please Enter Username")
                elif self.Empno_t.get()=="":
                    messagebox.showerror("DATAHIVE","Please Enter Employee Number")
                elif self.Password_t.get()=="":
                    messagebox.showerror("DATAHIVE","Please Enter Password")
                elif self.Username_t.get()==self.Empno_t.get():
                    messagebox.showerror("DATAHIVE","Username and Employee Number Cannot be Same")
                else:
                    tdata=[]
                    mycur.execute('SELECT EMPNO, EMAILID, FNAME, LNAME FROM TEACHERS WHERE EMPNO = {}'.format( self.Empno_t.get()))
                    tdata+=list(mycur.fetchall())
                    print(tdata)
                    if tdata == []:
                        if messagebox.askyesno('DATAHIVE','Employee number not Found\nDo you want to request Admin for authentication') :
                            Admin_Auth_Mail(self.Username_t.get(),"Teachers",self.Empno_t.get())
                    elif self.Username_t.get() != tdata[0][1]:
                        if messagebox.askyesno('DATAHIVE','Employee number not Found\nDo you want to request Admin for authentication') :
                            Admin_Auth_Mail(self.Username_t.get(),"Teachers",self.Empno_t.get())
                    elif tdata != []:
                        New_Login(self.Username_t.get() , self.Empno_t.get() , self.Password_t.get() , sel , tdata[0])
                        self.Login_Frame.tkraise()
   
    def Login_User(self) :
        global Main
        Username = self.Username_l.get()
        Password = self.Password_l.get()
        Auth = Login_Authenticate(Username , Password) 
        if Auth[0] :
            if Auth[1] == 'Login_authentication_St.bin' :
                self.root.destroy()
                TEMPORARY_FILE(Username)
                tkmain_student.launch_manager()
                
            elif Auth[1] ==  'Login_authentication_Ts.bin' :
                self.root.destroy()
                TEMPORARY_FILE(Username)
                tkmain_teacher.launch_manager()
            else :
                print("admin")
                self.root.destroy()
                TEMPORARY_FILE(Username)
                tkmain_admin.launch_manager()

        else:
            messagebox.showerror('DATAHIVE','Invalid username or password')

if __name__ == "__main__":
    root=Tk()
    Login_UI(root)
    root.mainloop()
