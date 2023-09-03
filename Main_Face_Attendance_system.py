from tkinter import *
from tkinter.font import Font
from tkhtmlview import HTMLLabel
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from pathlib import Path
import pickle
from collections import Counter
import time
import my_util
import face_recognition
import cv2
from PIL import Image,ImageTk,ImageDraw
from datetime import datetime
import os

class App:
    DEFAULT_ECONDINGS_PATH = Path('./output/encodings.pkl')
    def __init__(self):
        # WINDOW SETTINGS
        self.window = Tk()
        self.window.title("CLASS FACE RECOGNITION ATTENDANCE SYSTEM-- ")
        # self.window.attributes('-alpha', 0.8)

        self.window.config(bg='black')
        # self.window.wm_attributes('-transparentcolor', 'black')

        self.winht = self.window.winfo_screenheight()
        self.winwdt = self.window.winfo_screenwidth()
        self.mainwinh = self.winht - 100
        self.mainwidt = self.winwdt - 200
        self.window.geometry("%dx%d" % (self.mainwidt, self.mainwinh))
        self.icon = PhotoImage(file='app_data/img/ggg.png')
        self.window.iconphoto(False, self.icon)
        # DATE AND TIME FORMATING
        self.tm = time.localtime()
        self.dt = time.asctime(self.tm)
        self.nowdt = datetime.now()
        self.months = self.nowdt.strftime('%B')
        # COLOR CODES
        self.mainbg = '#757aa8'
        self.sidebar = '#7688A1'
        self.tablebg = '#CCCCCC'
        self.donebg = '#054505'
        self.canclebg = '#990C0C'
        self.BOUNDING_BOX_COLOR = 'blue'
        self.TEXT_COLOR = 'white'
        # THIS IS THE DATA BASE SECTION

        self.CLASS_REC_ATTAINDANCE = 1
        # PICSBASE LOCATION
        self.trainImg = './training/'
        #THE CLICK SWICTH COUNTER
        self.counter = 0
        Path('training').mkdir(exist_ok=True)
        Path('output').mkdir(exist_ok=True)
    # FUNCTIONS AND SYSTEM MANAGER OF THE APP
        self.curr_filter = None
        self.font1 = Font(family='comic', size=12, weight='bold', slant='roman', )

        # THE WINDOWS FRAME AND DIFFRENT APPS
        self.First_frm = Frame(self.window, bg='black')
        self.Subfrm = Frame(self.First_frm, relief=SUNKEN, background=self.mainbg)
        self.Subfrm.pack(fill=BOTH, pady=10, padx=10)
        # my data entry
        self.genderinput = StringVar()

        self.Mysecondwind = Frame(self.window, bg='black')
        self.display_sub_wind = Frame(self.Mysecondwind, relief=SUNKEN, bd=5, bg=self.mainbg)
        self.display_sub_wind.pack(fill=BOTH, expand=True)
        self.menu_bar = Menu(self.display_sub_wind)

        # Create the "Admin" menu
        self.admin_menu = Menu(self.menu_bar, tearoff=0)

        self.admin_menu.add_command(label='Login', command=self.navlog)
        self.admin_menu.add_command(label="View", command=self.userprofile)
        self.menu_bar.add_cascade(label="Admin", menu=self.admin_menu)
        self.menu_bar.add_command(label="Home", command=self.showhome )
        self.menu_bar.add_command(label="Attendance_List", command=self.showlist)
        self.menu_bar.add_command(label="Take Attendance", command=self.create_attendance_frame)
        self.menu_bar.add_command(label="Help", command=self.showhelp )
        self.window.config(menu=self.menu_bar)
        self.attendance_frame = Frame(self.display_sub_wind, background=self.mainbg, height=500, width=700, bd=0,
                                         padx=20)
        # END OF MENU
        self.homepage = Frame(self.display_sub_wind, background=self.mainbg,height=500, width=700, bd=0,padx=20)

        ImagSection = Frame(self.homepage, bg=self.mainbg, padx=10, pady=20)
        ImagSection.pack(fill=BOTH, expand=True)
        ImagesShow = Frame(ImagSection, bg='#eee', padx=10, pady=20)
        show1 = PhotoImage(file='app_data/img/imag1.png')
        showcim1 = show1.subsample(2, 2)
        showseeim1 = Label(ImagesShow, image=showcim1, justify=LEFT, bd=5, relief=SUNKEN)
        showseeim1.grid(row=0, column=0)

        show2 = PhotoImage(file='app_data/img/imag2.png')
        showcim2 = show2.subsample(2, 2)
        showseeim2 = Label(ImagesShow, image=showcim2, justify=LEFT, bd=5, relief=SUNKEN)
        showseeim2.grid(row=0, column=1)

        show3 = PhotoImage(file='app_data/img/imag3.png')
        showcim3 = show3.subsample(2, 2)
        showseeim3 = Label(ImagesShow, image=showcim3, justify=LEFT, bd=5, relief=SUNKEN)
        showseeim3.grid(row=1, column=0)

        show4 = PhotoImage(file='app_data/img/img4.png')
        showcim4 = show4.subsample(2, 2)
        showseeim4 = Label(ImagesShow, image=showcim4, justify=LEFT, bd=5, relief=SUNKEN)
        showseeim4.grid(row=1, column=1)

        ImagesShow.pack()
        self.activeld_no = Label(self.homepage, bg=self.mainbg, fg='white',font=self.font1)
        self.activeld_no1 = Label(self.homepage, bg=self.mainbg, fg='white', font=self.font1)
        self.activeld_no1.pack()
        self.activeld_no.pack()

        # self.homepage.pack(expand=True, anchor=CENTER)

        # THE LIST STARTS HERE
        self.List_frame = Frame(self.display_sub_wind, background=self.mainbg, width=700, bd=0,
                                         padx=20)

        # my_tip = HTMLLabel(self.List_frame, html=tip, background=self.mainbg, font=self.font1, height=800)
        my_tip =Label(self.List_frame, text='Class Attendance', font=self.font1,bg=self.mainbg)
        my_tip.grid(row=0, column=1, pady=10, sticky='nsew', columnspan=2)
        self.display_report = Frame(self.List_frame,background=self.mainbg)
        self.display_report.grid(row=1, column=1, sticky='nsew')
        self.columnrp = ('#', 'Name', 'RegNo', 'Department', 'Class', 'Date')
        self.report_item = ttk.Treeview(self.display_report, columns=self.columnrp, show='headings', height=15, )
        style = ttk.Style()
        style.map("Treeview",
                  foreground=[("selected", "black")],
                  background=[("selected", "#FFCCCB")])
        # Style for rows
        style.configure("Treeview",
                        background="#ECECEC",
                        foreground="black",
                        rowheight=25,  # Adjust the row height as needed
                        fieldbackground=self.mainbg)

        # Style for columns
        style.configure("Treeview.Heading",
                        background="blue",
                        foreground="black",
                        font=("Helvetica", 12, "bold"))

        myscrollbar = ttk.Scrollbar(self.display_report, orient=VERTICAL, command=self.report_item.yview, )
        self.report_item.configure(yscroll = myscrollbar.set)
        self.report_item.column('0', width=50, anchor='c')

        myscrollbar.grid(row=1, column=3, sticky='ns')
        self.report_item.heading('#0', text='S/N')
        self.report_item.heading('Name', text='Students Name')
        self.report_item.heading('RegNo', text='Registration Number')
        self.report_item.heading('Department', text='Department')
        self.report_item.heading('Class', text='Course')
        self.report_item.heading('Date', text='Date of Attendance')
        self.report_item.grid(row=1, column=1, sticky='nsew')
        deletebu5 = Button(self.List_frame, text='Delete', bg='red', fg="white", font=self.font1, command= self.deletxxstudent)
        deletebu5.grid(row=3, column=0, sticky='w')
        self.Help_frame = Frame(self.display_sub_wind, background=self.mainbg,height=500, width=700, bd=0,padx=20)
        # self.homepage.pack(expand=True, anchor=CENTER)
        self.user_page = Frame(self.display_sub_wind)
        self.signupNewuser = Frame(self.Subfrm, bg=self.mainbg, height=700, width=800, bd=0, padx=20)
        # signupNewuser.pack(fill=BOTH, pady=10, padx=10)
        log_head = Label(self.signupNewuser, text='REGISTER LECTURER', font=('Impact', 20, 'bold', 'roman'), bg=self.mainbg,
                         fg='Black')
        staffName = Label(self.signupNewuser, text='Name:', bg=self.mainbg, font=self.font1)
        email = Label(self.signupNewuser, text='Email:', bg=self.mainbg, font=self.font1)
        course = Label(self.signupNewuser, text='Course', bg=self.mainbg, font=self.font1)
        pass_word = Label(self.signupNewuser, text='Password:', bg=self.mainbg, font=self.font1)
        fistdate_input = Label(self.signupNewuser, text='Confirm Password:', bg=self.mainbg, font=self.font1)
        phone = Label(self.signupNewuser, text='Phone:', bg=self.mainbg, font=self.font1)
        self.namein = Entry(self.signupNewuser,fg='grey', insertbackground='white', background=self.mainbg, width=30,
                       font=('Lucida Sans', 15, 'bold', 'roman',))

        self.emailin = Entry(self.signupNewuser,fg='grey', insertbackground='white', background=self.mainbg,
                        width=30, font=('Lucida Sans', 15, 'bold', 'roman',))
        self.coursein = Entry(self.signupNewuser,fg='grey', insertbackground='white', background=self.mainbg,
                         width=30, font=('Lucida Sans', 15, 'bold', 'roman',))
        self.gen = ttk.Radiobutton(self.signupNewuser, text='Male', variable=self.genderinput, value='male')
        self.gen2 = ttk.Radiobutton(self.signupNewuser, text='Female', variable=self.genderinput, value='female')
        self.pass1 = Entry(self.signupNewuser,fg='grey', insertbackground='white', show='*', background=self.mainbg,
                    width=30, font=('Lucida Sans', 15, 'bold', 'roman',))
        self.pass2 = Entry(self.signupNewuser, insertbackground='white', show='*', background=self.mainbg,
                       width=30, font=('Lucida Sans', 15, 'bold', 'roman',))
        self.phonein = Entry(self.signupNewuser, insertbackground='white', background=self.mainbg,
                        width=30, font=('Lucida Sans', 15, 'bold', 'roman',))
        reg_new_user = Button(self.signupNewuser, text='Sign up', bg=self.donebg, fg='#fff',
                              width=25, font=('Lucida Sans', 15, 'bold', 'roman',),
                              activebackground='green', command=self.register_superuser)
        snupCancle = Button(self.signupNewuser, text='Cancle', command=self.navlog, bg=self.canclebg, fg='#fff',
                            font=('Lucida Sans', 10, 'bold', 'roman',),
                            activebackground='green',)
        # ---------------------------- ADMIN PLACE SECTION
        log_head.place(relx=0.5, rely=0.04, anchor=CENTER)
        staffName.place(relx=0.22, rely=0.2, anchor=S)
        self.namein.place(relx=0.2, rely=0.25, anchor=SW)
        email.place(relx=0.22, rely=0.3, anchor=S)
        self.emailin.place(relx=0.2, rely=0.35, anchor=SW)
        course.place(relx=0.22, rely=0.4, anchor=S)
        self.coursein.place(relx=0.2, rely=0.45, anchor=SW)
        pass_word.place(relx=0.2, rely=0.5, anchor=SW)
        self.pass1.place(relx=0.2, rely=0.55, anchor=SW)
        fistdate_input.place(relx=0.26, rely=0.6, anchor=S)
        self.pass2.place(relx=0.2, rely=0.65, anchor=SW)
        phone.place(relx=0.26, rely=0.7, anchor=S)
        self.phonein.place(relx=0.2, rely=0.75, anchor=SW)
        self.gen.place(relx=0.8, rely=0.35, anchor=SW)
        self.gen2.place(relx=0.8, rely=0.45, anchor=SW)
        reg_new_user.place(relx=0.5, rely=0.9, anchor=CENTER)
        snupCancle.place(relx=0.8, rely=0.099, anchor=W)
        self.loginFr = Frame(self.Subfrm, height=700, width=500, bd=0, bg=self.mainbg, relief=RAISED)
        self.loginFr.pack()
    # THIS IS MY LOG-IN FRAME  AND  THE TEXT PATTERNS
    # THE HOME OF THE APP IS FROM HERE
        mlogo = PhotoImage(file='app_data/img/ggg.png')
        logodic = mlogo.subsample(3, 3)
        thelogo = Label(self.loginFr, image=logodic, justify=CENTER, bg=self.mainbg)
        thelogo.place(relx=0.5, rely=0.3, anchor=CENTER)
        name_box = Label(self.loginFr, text='Username ',fg='#fce23d', bg=self.mainbg, font=self.font1)
        pass_word = Label(self.loginFr, text='Password:',fg='#fce23d', bg=self.mainbg, font=self.font1)
        # log in inputs and get value
        self.useremail = StringVar()
        self.uniq_pass_key = StringVar()
    # INPUTS OF THE FORM
        self.user = Entry(self.loginFr, insertbackground='white',fg='grey', textvariable=self.useremail, background=self.mainbg, font=('Impact',20,'bold','roman'),
                     foreground='black', width=40, )
        self.identity = Entry(self.loginFr, insertbackground='white',fg='grey', show='*', textvariable=self.uniq_pass_key, background=self.mainbg,
                         font=('Impact',20,'bold','roman'),
                         foreground='black', width=40)
        send = Button(self.loginFr, text='Log-In',bg=self.donebg,fg='#fff',width=25,font=('Lucida Sans', 15, 'bold','roman',),
                      activebackground='green',command=self.lognin)
        userreg = Button(self.loginFr, text='Sign-Up', bg=self.canclebg, fg='#fff',font=('Lucida Sans', 10, 'bold','roman',),
                         command=self.Rnavlog, activebackground='green')
        Auto = Label(self.loginFr, text='This project was done by  Uchennam Nzubechi (zubegpro) ', bg=self.mainbg, fg='white',
                     font=Font(family='Lucida Sans', size=8, slant='roman', ))
        # my grid for the labels
        name_box.place(relx=0.2, rely=0.5, anchor=S)
        self.user.place(relx=0.1, rely=0.59, anchor=SW)
        pass_word.place(relx=0.2, rely=0.65, anchor=S)
        self.identity.place(relx=0.1, rely=0.74, anchor=SW)
        send.place(relx=0.55, rely=0.84, anchor=CENTER)
        userreg.place(relx=0.8, rely=0.099, anchor=W)
        Auto.place(relx=0.55, rely=0.95, anchor=CENTER)
# THE TWO WINDOW PACK SECTIONS FOR BOTH THE FIRST FRAME AND SECOND FRAME IN THE APPLICATION
        self.First_frm.pack(fill=BOTH, expand=True)
#         self.Mysecondwind.pack(fill=BOTH, expand=True)
        self.window.mainloop()
    # THIS THE SECOND OR THE INNER PAGE OF THE DESKTOP APP
    # THE REGISTER NEW USER SECTION REGISTER NEW USER SECTION IS OVER  HERE-----------
    # THIS THE STUDENT REG SECTION
    def create_studentreg_frame(self):
        self.studentreg_frame = Toplevel(self.window, bg='#757aa8')
        self.studentreg_frame.geometry("%dx%d" % (self.mainwidt - 100, self.mainwinh - 100))
        # STUDENT REGISTRATION  COMPONENTS
        self.stu_gnder = StringVar()

        self.lab_name = my_util.mytextLabel(self.studentreg_frame, 'Students Fullname')
        self.stu_name = my_util.myentry(self.studentreg_frame)
        self.lab_reg = my_util.mytextLabel(self.studentreg_frame, 'Students Reg.No')
        self.stu_reg = my_util.myentry(self.studentreg_frame)
        self.lab_dept = my_util.mytextLabel(self.studentreg_frame, 'Students Department')
        self.stu_dept = my_util.myentry(self.studentreg_frame)
        self.lab_phone = my_util.mytextLabel(self.studentreg_frame, 'Contact PhoneNo')
        self.stu_phone = my_util.myentry(self.studentreg_frame)
        self.stu_gen = ttk.Radiobutton(self.studentreg_frame, text='Male', variable=self.stu_gnder, value='male')
        self.stu_gen2 = ttk.Radiobutton(self.studentreg_frame, text='Female', variable=self.stu_gnder, value='female')
        self.start_reg_btn = my_util.mybutton(self.studentreg_frame, 'Start', self.donebg, self.registerNewStudent)
        self.cancle_reg_btn = my_util.mybutton(self.studentreg_frame, 'Cancle', self.canclebg, self.Retakepics)
        self.capture_show = my_util.myimgLabel(self.studentreg_frame)
        self.capture_show.place(x=10, y=10, width=600, height=500)
        self.lab_name.place(x=620, y=20)
        self.stu_name.place(x=620, y=50)
        self.lab_reg.place(x=620, y=100)
        self.stu_reg.place(x=620, y=130)
        self.lab_dept.place(x=620, y=180)
        self.stu_dept.place(x=620, y=210)
        self.lab_phone.place(x=620, y=260)
        self.stu_phone.place(x=620, y=300)
        self.stu_gen.place(x=620, y=360)
        self.stu_gen2.place(x=680, y=360)
        self.start_reg_btn.place(x=620, y=380)
        self.cancle_reg_btn.place(x=620, y=425)
        if not os.path.exists(self.trainImg):
            os.mkdir(self.trainImg)


    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        self.newuserCapture = self.most_recent_capture_arr.copy()


    def registerNewStudent(self):
        connection1 = sqlite3.connect("CLASS_REC_ATTAINDANCE.db")
        cursor1 = connection1.cursor()

        if self.counter == 0:
            self.counter = +1
            self.add_img_to_label(self.capture_show)
        elif self.counter > 0:
            if self.stu_name.get(1.0, "end-1c") == '' or self.stu_reg.get(1.0, "end-1c") == '' or self.stu_dept.get(1.0, "end-1c") == '' or self.stu_phone.get(1.0, "end-1c") == '' or self.stu_gnder.get() == '':
                messagebox.showerror('Error', 'All fields are required', parent=self.studentreg_frame)
            else:
                try:
                    cursor1.execute(
                        '''CREATE TABLE IF NOT EXISTS Student_base(Student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Student_name TEXT,
                        RegNo TEXT,Department TEXT,Phone TEXT,Gender TEXT,Created TEXT)
                        ''')

                    connection1.execute('SELECT * FROM Student_base WHERE RegNo= ?', (self.stu_reg.get(1.0, "end-1c"),))
                    row = cursor1.fetchone()

                    if row != None:
                        messagebox.showerror("Error", 'User already exist, pls try again with another registration number')
                    else:
                        connection = sqlite3.connect("CLASS_REC_ATTAINDANCE.db")
                        cursor = connection.cursor()
                        cursor.execute(
                            "INSERT INTO Student_base(Student_name ,RegNo , Department ,Phone ,Gender ,Created) VALUES (?,?,?,?,?,?)",
                            (
                                self.stu_name.get(1.0, "end-1c"), self.stu_reg.get(1.0, "end-1c"), self.stu_dept.get(1.0, "end-1c"), self.stu_phone.get(1.0, "end-1c"),
                                self.stu_gnder.get(),
                                self.dt,))
                        connection.commit()
                        connection.close()
                        messagebox.showinfo('Success', 'Registerd sucessfully', parent=self.studentreg_frame)

                    connection1.commit()
                    connection1.close()
                    # self.add_img_to_label(self.capture_show)
                    name = self.stu_name.get(1.0, 'end-1c')
                    cv2.imwrite(os.path.join(self.trainImg, '{}.jpg'.format(name)), self.newuserCapture)
                    messagebox.showinfo('Successful', f'YOU have registerd {name} successfuly')
                    self.counter = 0
                except Exception as ex:
                    messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.studentreg_frame)


    def Retakepics(self):
        self.studentreg_frame.destroy()
        self.counter = 0


# THIS IS FOR CHECKING TAKING THE ATTAINDANCE   ATTAINDANCE SECTION
    # THIS IS THE FUNCTION THAT CONTROLS THE VIEWS OF DIFFERENT PAGES
    def create_attendance_frame(self):

        self.attendance_frame.pack(fill=BOTH, expand=True)
        self.homepage.pack_forget()
        self.user_page.pack_forget()
        self.List_frame.pack_forget()
        self.Help_frame.pack_forget()
        # ALL  ATTENDANCE IS TAKEN IN THIS SECTION
        # ATTENDANCE COMPONENTS
        self.course = my_util.myentry(self.attendance_frame)
        self.start_attendance_btn = my_util.mybutton(self.attendance_frame, 'Start', self.donebg, self.startAttance)
        self.cancle_attendance_btn = my_util.mybutton(self.attendance_frame, 'Stop', self.canclebg,
                                                      self.Stopattend)
        self.Reg_newStudent_attendance_btn = my_util.mybutton(self.attendance_frame, 'Add Student', 'grey',self.create_studentreg_frame)
        promptinfo = my_util.mytextLabel(self.attendance_frame, 'Take attendance in 5-10 ')
        info_text = my_util.mytextLabel(self.attendance_frame, 'Enter the Course Title ')
        self.webcam_show = my_util.myimgLabel(self.attendance_frame)
        self.webcam_show.place(x=10, y=10, width=600, height=500)
        self.add_webcam(self.webcam_show)
        promptinfo.place(x=620, y=10, )
        info_text.place(x=620, y=50, )
        self.course.place(x=620, y=100)
        self.start_attendance_btn.place(x=620, y=200)
        self.cancle_attendance_btn.place(x=620, y=300)
        self.Reg_newStudent_attendance_btn.place(x=620, y=400)
        self.attendance_frame.pack(fill=BOTH, )


    def showhome(self):
        self.List_frame.pack_forget()
        self.Help_frame.pack_forget()
        self.homepage.pack(fill=BOTH)
        self.user_page.pack_forget()
        self.attendance_frame.pack_forget()

        if 'regface' in self.__dict__:
            self.regface.release()
        try:
            sl = sqlite3.connect("CLASS_REC_ATTAINDANCE.db")
            slcursor = sl.cursor()
            slcursor.execute("SELECT seq FROM sqlite_sequence")
            tsl = slcursor.fetchall()
            # for i in tsl:

            self.activeld_no.configure(text=f'NUmber of Students that you teach : {tsl[0]}')
            self.activeld_no1.configure(text=f'Number of students in Attandance list: {tsl[1]}')
            sl.commit()
            sl.close()
        except Exception as es:
            messagebox.showerror('Error', f"Error due to :{str(es)}", parent=self.homepage)


    def showlist(self):
        self.Help_frame.pack_forget()
        self.homepage.pack_forget()
        self.user_page.pack_forget()
        self.attendance_frame.pack_forget()
        if 'regface' in self.__dict__:
            self.regface.release()


        listcur = None
        listconnec = None
        rep = True
        try:
            if rep:
                listconnec = sqlite3.connect("CLASS_REC_ATTAINDANCE.db")
                listcur = listconnec.cursor()
                listcur.execute('SELECT Attend_id, AttendStname, StRegNo, StDepartment,Class,TimeArrived FROM Attaindance_list')
                listtc = listcur.fetchall()

                for item in self.report_item.get_children():
                    self.report_item.delete(item)
                for cont in listtc:
                    self.report_item.insert('', END, values=cont)

        except Exception as es:
            messagebox.showerror('Error', f"Error due to :{str(es)}", parent=self.List_frame)
        finally:
            if listcur is not None:
                listcur.close()
            if listconnec is not None:
                listconnec.close()
        self.List_frame.pack(expand=True, fill=BOTH)


    def showhelp(self):
        if 'regface' in self.__dict__:
            self.regface.release()
        self.List_frame.pack_forget()
        self.Help_frame.pack(expand=True, fill=BOTH)
        self.homepage.pack_forget()
        self.user_page.pack_forget()
        self.attendance_frame.pack_forget()
        details = f'''
            <h3>Face Recoginition Attaindance System:</h3>
            <span style='font-size:10px'>Your next menstruation will start on <span>
            <p style="color:white;"><b>{self.nowdt.strftime("%A/%b/%Y")}<b></p> TO
            <p><b>
            Face recognition technology is a biometric technology that involves the identification of individuals based on their unique facial features. It is a type of computer vision technology that uses algorithms and mathematical models to analyse and recognize human faces in images or video footage.
            The technology works by capturing an image or video of a person's face and then analysing the features of the face, such as the distance between the eyes, the shape of the nose, and the contours of the face. These features are then compared to a database of known faces to identify the individual.

            <b></p>
            '''
        Introduction = HTMLLabel(self.Help_frame, foreground='white', html=details, padx=10, background='black')
        Introduction.pack()


    def userprofile(self):
        self.List_frame.pack_forget()
        self.Help_frame.pack_forget()
        self.user_page.pack(expand=True, anchor=CENTER)
        self.attendance_frame.pack_forget()
        if 'regface' in self.__dict__:
            self.regface.release()
        self.homepage.pack_forget()
        cur = None
        connec = None

        try:
            connec = sqlite3.connect("CLASS_REC_ATTAINDANCE.db")
            cur = connec.cursor()
            cur.execute(
                'SELECT * FROM Staff_base WHERE email= ?', (self.useremail.get(),))
            tc = cur.fetchall()
            for cont in tc:
                htmldetails = f'''
                    <div>
                        <h4>{self.useremail.get()}</h4>
                        <div>
                         YOU ARE WELCOME TO YOUR PROFILE PAGE 
                        </div>
                        <div>
                            Staff's Name : {cont[0]}
                        </div>
                        <div>
                            Course You Handle : {cont[1]}
                        </div>
                        <div>
                            Email-address : {cont[2]}
                        </div>
                        <div>
                            Phone Number : {cont[3]}
                        </div>
                        <div>
                            Gender : {cont[4]}
                        </div>
                        <div>
                            Passwowrd : {cont[5]}
                        </div> 
                        <div>
                            Account was Created : {cont[6]}
                        </div> 


                '''
                my_label = HTMLLabel(self.user_page, html=htmldetails, padx=5, background=self.mainbg, font=self.font1, height=self.winht,
                                     width=150)
                my_label.grid(row=1, column=1, pady=10, sticky=NSEW)
        except Exception as es:
            messagebox.showerror('Error', f"Error due to :{str(es)}", parent=self.user_page)
        finally:
            if cur is not None:
                cur.close()
            if connec is not None:
                connec.close()


    # THE CAMERA PROCESSING
    def add_webcam(self, label):
        if 'regface ' not in self.__dict__:
            self.regface  = cv2.VideoCapture(0)
        self._lable = label
        self.process_webcam()


    def process_webcam(self):
        ret, frame = self.regface.read()
        if ret:
            self.most_recent_capture_arr = frame
            img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
            self.most_recent_capture_pil = Image.fromarray(img_)
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            self._lable.imgtk = imgtk
            self._lable.configure(image=imgtk)
            self._lable.after(20, self.process_webcam)


    def encode_known_faces(self, model: str = 'hog', encodings_location: Path = DEFAULT_ECONDINGS_PATH) -> None:
        names = []
        encodings = []
        list_img = os.listdir(self.trainImg)

        for filename in list_img:
            filepath = os.path.join(self.trainImg, filename)
            name = os.path.splitext(filename)[0]
            image = face_recognition.load_image_file(filepath)
            face_locatiions = face_recognition.face_locations(image, model=model)
            face_encodings = face_recognition.face_encodings(image, face_locatiions)
            for encoding in face_encodings:
                names.append(name)
                encodings.append(encoding)

        name_endcoing = {'names': names, 'encodings': encodings}
        with encodings_location.open(mode='wb') as f:
            pickle.dump(name_endcoing, f)


    def recognize_face(self, image_location, model='hog', encodings_location=DEFAULT_ECONDINGS_PATH):
        self.encode_known_faces()

        with encodings_location.open(mode='rb') as f:
            loaded_encodings = pickle.load(f)

        input_image = face_recognition.load_image_file(image_location)
        input_face_locations = face_recognition.face_locations(input_image, model=model)
        input_face_encodings = face_recognition.face_encodings(input_image, input_face_locations)
        pillow_image = Image.fromarray(input_image)
        draw = ImageDraw.Draw(pillow_image)

        # Create the table outside the loop if it doesn't exist
        connection1 = sqlite3.connect("CLASS_REC_ATTAINDANCE.db")
        with connection1:
            connection1.execute('''
                    CREATE TABLE IF NOT EXISTS Attaindance_list(
                    Attend_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    AttendStname TEXT,
                    StRegNo TEXT, StDepartment TEXT, Class TEXT, TimeArrived TEXT)
                ''')

        for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings):
            name = self._recognize_face(unknown_encoding, loaded_encodings)

            if not name:
                name = 'Unknown'

            if name != 'Unknown':
                try:
                    with sqlite3.connect("CLASS_REC_ATTAINDANCE.db") as connec:
                        cur = connec.cursor()
                        cur.execute(
                            'SELECT * FROM Student_base WHERE Student_name = ?', (name,))
                        tc = cur.fetchall()
                        with connec:
                            clur = connec.cursor()
                            for cont in tc:
                                clur.execute(
                                    'INSERT INTO Attaindance_list (AttendStname,StRegNo, StDepartment, Class, TimeArrived) VALUES(?,?,?,?,?)',
                                    (cont[1], cont[2], cont[3], self.course.get(1.0, "end-1c"), self.nowdt,))
                except sqlite3.Error as es:
                    messagebox.showerror('Error', f"Error due to :{str(es)}", parent=self.user_page)
            self._display_face(draw, bounding_box, name)

        del draw
        pillow_image.show()


    def deletxxstudent(self):
        try:
            inconnection = sqlite3.connect("CLASS_REC_ATTAINDANCE.db")
            icursor = inconnection.cursor()
            curItem = self.report_item.focus()
            tt4 = tuple(self.report_item.item(curItem)['values'])
            tcheck = tt4[0]

            icursor.execute(
                "DELETE FROM Attaindance_list WHERE Attend_id =? ", (tcheck,))

            self.report_item.delete(curItem)
        except Exception as es:
            messagebox.showerror('info', f'you selected nothing {es}', parent=self.List_frame )
        inconnection.commit()
        inconnection.close()


    def _display_face(self, draw, bounding_box, name):
        top, right, bottom, left = bounding_box
        draw.rectangle(((left, top), (right, bottom)), outline=self.BOUNDING_BOX_COLOR)
        text_left, text_top, text_right, text_bottom = draw.textbbox((left, bottom), name)
        draw.rectangle(((text_left, text_top), (text_right, text_bottom)), fill='blue', outline='blue', )
        draw.text((text_left, text_top), name, fill='white', )


    def _recognize_face(self, unknown_encoding, loaded_encodings):
        boolean_matches = face_recognition.compare_faces(loaded_encodings['encodings'], unknown_encoding)
        votes = Counter(name
                        for match, name in zip(boolean_matches, loaded_encodings['names'])
                        if match
                        )
        if votes:
            return votes.most_common(1)[0][0]


    def startAttance(self):
        if self.course.get(1.0, "end-1c") != '':
            unknown_img_path = './.tmp.jpg'
            # Capture the most recent frame from the webcam and save it as a temporary image file
            cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
            # Load the image as a numpy array
            self.recognize_face(unknown_img_path)
        else:
            messagebox.showerror('Error', 'The course title is Empty', parent=self.attendance_frame)


    def Stopattend(self):
        pass


# THIS SECTION IF FOR THE USER REGISTRATION AND LOGIN TO THE DATABASE
    def addsuperUser(self):
        self.Subfrm.pack_forget()
        self.signupNewuser.pack(fill=BOTH, padx=10, pady=10)
        self.namein.delete(0, END)
        self.coursein.delete(0, END)
        self.emailin.delete(0, END)
        self.phonein.delete(0, END)
        self.pass1.delete(0, END)
        self.pass2.delete(0, END)


    def register_superuser(self):
        if (
                self.namein.get() == ''
                or self.coursein.get() == ''
                or self.emailin.get() == ''
                or self.phonein.get() == ''
                or self.pass1.get() == ''
                or self.pass2.get() == ''
        ):
            messagebox.showerror('Error', 'All fields are required', parent=self.signupNewuser)
        elif self.pass1.get() != self.pass2.get():
            messagebox.showerror('Error', "Your passwords don't match", parent=self.signupNewuser)
        else:
            try:
                connection = sqlite3.connect("CLASS_REC_ATTAINDANCE.db")
                cursor = connection.cursor()

                cursor.execute(
                    '''CREATE TABLE IF NOT EXISTS Staff_base(
                            Name TEXT,
                            Course TEXT,
                            Email TEXT,
                            Phone TEXT,
                            Gender TEXT,
                            Password TEXT,
                            Created TEXT,
                            student_id INTEGER,
                            FOREIGN KEY(student_id) REFERENCES students(student_id)
                                ON DELETE SET NULL
                        )'''
                )

                cursor.execute('SELECT * FROM Staff_base WHERE Email = ?', (self.useremail.get(),))
                row = cursor.fetchone()

                if row is not None:
                    messagebox.showerror("Error", 'User already exists, please try again with another email')
                else:
                    cursor.execute(
                        "INSERT INTO Staff_base(Name, Course, Email, Phone, Gender, Password, Created) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (
                            self.namein.get(),
                            self.coursein.get(),
                            self.emailin.get(),
                            self.phonein.get(),
                            self.genderinput.get(),
                            self.pass1.get(),
                            self.dt,
                        )
                    )

                    connection.commit()
                    connection.close()
                    messagebox.showinfo('Success', 'Registered successfully', parent=self.signupNewuser)

            except Exception as ex:
                messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.signupNewuser)


    def navlog(self):
        self.signupNewuser.pack_forget()
        self.loginFr.pack()


    def lognin(self):
        if self.useremail.get() == '' or self.uniq_pass_key.get() == '':
            messagebox.showerror('Input Error', 'All fields are required', parent=self.loginFr)
        else:
            connection1 = sqlite3.connect("CLASS_REC_ATTAINDANCE.db")
            # cursor1 = connection1.cursor()
            cur = None
            conec = None
            try:
                checkinput = connection1.execute('SELECT * FROM Staff_base WHERE Email= ? OR Phone=? AND password=?',
                                                 (self.useremail.get(), self.phonein.get(), self.uniq_pass_key.get(),))
                row = checkinput.fetchone()
                if row == None:
                    messagebox.showerror('Wrong input', 'Not Registered in our system')
                else:
                    self.First_frm.pack_forget()
                    self.Mysecondwind.pack(fill=BOTH, expand=True)
                    self.homepage.pack(fill=BOTH)
                    self.List_frame.pack_forget()
                    self.Help_frame.pack_forget()
                    self.attendance_frame.pack_forget()

                    welcome_me = f'Hi {self.useremail.get()}'
                    h4 = HTMLLabel(self.homepage, html=welcome_me, background=self.mainbg, height=800)
                    h4.pack()

                    self.admin_menu.delete("Login")  # Remove "Login" command
                    self.admin_menu.add_command(label="Logout", command=self.logout)
                connection1.commit()
                connection1.close()

            except Exception as es:
                messagebox.showerror('Error', f"Error due to :{str(es)}", parent=self.loginFr)


    def logout(self):
        lm = messagebox.askyesno(title='Logout', message='Do you want to LOG out ?')
        if lm:
            self.admin_menu.delete("Logout")  # Remove "Logout" command
            self.admin_menu.add_command(label="Login", command=self.navlog)
            self.First_frm.pack(fill=BOTH)
            # self.connection1.commit()
            # self.connection1.close()
            self.Mysecondwind.pack_forget()
        else:
            messagebox.showinfo('Return', 'Returning to my Dashboard')


    def Rnavlog(self):
        self.signupNewuser.pack()
        self.loginFr.pack_forget()


if __name__ == "__main__":
    app = App()