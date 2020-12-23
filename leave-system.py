import sqlite3
import tkinter
import tkinter.messagebox as tk
from tkinter.font import Font
from easygui import *
from tkinter import *
from turtle import *
import random

conn = sqlite3.connect('leaveDb.db')
cur = conn.cursor()


#conn.execute("CREATE TABLE balance (employee_id text,sickleave int,maternityleave int,emergencyleave int)")
#conn.execute("CREATE TABLE status (leave_id int,employee_id text,leave text,Date1 text,Date2 text,days int,status text)")
#conn.execute('''CREATE TABLE employee (employee_id text,Name text,ContactNumber text,Password text)''')

def AdminLogin():
    message = "Enter Username and Password"
    title = "Admin Login"
    fieldnames = ["Username", "Password"]
    field = []
    field = multpasswordbox(message, title, fieldnames)
    if field[0] == 'admin' and field[1] == 'admin':
        tkinter.messagebox.showinfo("Admin Login", "Login Successfully")
        adminwindow()
    else:
        tk.showerror("Error info", "Incorrect username or password")


def EmployeeLogin():
    message = "Enter Employee ID and Password"
    title = "Employee Login"
    fieldnames = ["Employee ID", "Password"]
    field = []
    field = multpasswordbox(message, title, fieldnames)

    for row in conn.execute('SELECT * FROM employee'):
        if field[0] == row[0] and field[1] == row[3]:
            global login
            login = field[0]
            f = 1
            print("Success")
            tkinter.messagebox.showinfo("Employee Login", "Login Successfully")
            EmployeeLoginWindow()
            break
    if not f:
        print("Invalid")
        tk.showerror("Error info", "Incorrect employee id or password")

def Employeelogout():
    global login
    login = -1
    LoginWindow.destroy()


def EmployeeLeaveStatus():
    global leaveStatus
    leaveStatus = []
    for i in conn.execute('SELECT * FROM status where employee_id=?', login):
        leaveStatus = i

    WindowStatus()


def EmployeeAllStatus():
    allStatus = Toplevel()
    txt = Text(allStatus)
    for i in conn.execute('SELECT * FROM status where employee_id=?', login):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


def EmployeeInformationWindow():
    employeeInformation = Toplevel()
    txt = Text(employeeInformation)
    for i in conn.execute('SELECT employee_id,Name,ContactNumber FROM employee where employee_id=?', login):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


def EmployeeAllInformationWindow():
    allEmployeeInformation = Toplevel()
    txt = Text(allEmployeeInformation)
    for i in conn.execute('SELECT employee_id,Name,ContactNumber FROM employee'):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


def WindowStatus():
    StatusWindow = Toplevel()
    label_1 = label(StatusWindow, text="Employee ID", fg="green", justify=LEFT, Font=("NewTimeRoman", 18))
    label_2 = label(StatusWindow, text=leaveStatus[1], Font=("NewTimeRoman", 18))
    label_3 = label(StatusWindow, text="Type=", fg="green", justify=LEFT, Font=("NewTimeRoman", 18))
    label_4= label(StatusWindow, text=leaveStatus[2], Font=("NewTimeRoman", 18))
    label_5 = label(StatusWindow, text="start=", fg="green", justify=LEFT, Font=("NewTimeRoman", 18))
    label_6 = label(StatusWindow, text=leaveStatus[3], Font=("NewTimeRoman", 18))
    label_7 = label(StatusWindow, text="end=", fg="green", justify=LEFT, Font=("NewTimeRoman", 18))
    label_8 = label(StatusWindow, text=leaveStatus[4], Font=("NewTimeRoman", 18))
    label_9 = label(StatusWindow, text="Status:", fg="green", justify=LEFT, Font=("NewTimeRoman", 18))
    label_10 = label(StatusWindow, text=leaveStatus[6], Font=("NewTimeRoman", 18))
    label_11 = label(StatusWindow, text="leave_id:", fg="green", justify=LEFT, Font=("NewTimeRoman", 18))
    label_12 = label(StatusWindow, text=leaveStatus[0], Font=("NewTimeRoman", 18))
    label_11.grid(row=0, column=0)
    label_12.grid(row=0, column=1)
    label_1.grid(row=1, column=0)
    label_2.grid(row=1, column=1)
    label_3.grid(row=2, column=0)
    label_4.grid(row=2, column=1)
    label_5.grid(row=3, column=0)
    label_6.grid(row=3, column=1)
    label_7.grid(row=4, column=0)
    label_8.grid(row=4, column=1)
    label_9.grid(row=5, column=0)
    label_10.grid(row=5, column=1)


def balance():
    global login
    check = (login,)
    global balanced
    balanced = []
    for i in conn.execute('SELECT * FROM balance WHERE employee_id =?', check):
        balanced = i

    WindowBalance()


def WindowBalance():
    balanceWindow = Toplevel()
    label_1 = label(balanceWindow, text="Employee ID=", fg="green", justify=LEFT, Font=("NewTime Roman", 18))
    label_2 = label(balanceWindow, text="balanced[0]", Font=("NewTime Roman", 18))
    label_3 = label(balanceWindow, text="Sick Leave=", fg="green", justify=LEFT, Font=("NewTime Roman", 18))
    label_4 = label(balanceWindow, text="balanced[1]", Font=("NewTime Roman", 18))
    label_5 = label(balanceWindow, text="Maternity=", fg="green", justify=LEFT, Font=("NewTime Roman", 18))
    label_6 = label(balanceWindow, text="balanced[2]", Font=("NewTime Roman", 18))
    label_7 = label(balanceWindow, text="Emergency Leave=", fg="green", justify=LEFT, Font=("NewTime Roman", 18))
    label_8 = label(balanceWindow, text="balanced[3]", Font=("NewTime Roman", 18))
    label_1.grid(row=0, column=0)
    label_2.grid(row=0, column=1)
    label_3.grid(row=1, column=0)
    label_4.grid(row=1, column=1)
    label_5.grid(row=2, column=0)
    label_6.grid(row=2, column=1)
    label_7.grid(row=3, column=0)
    label_8.grid(row=3, column=1)


def apply():
    message = "Enter the following details "
    title = "Leave Apply"
    fieldNames = ["Employee ID", "From", "To", "days"]
    fieldValues = []
    fieldValues = multenterbox(message, title, fieldNames)
    message1 = "Select type of leave"
    title1 = "Type of leave"
    choices = ["Sick leave", "Maternity leave", "Emergency leave"]
    choice = choicebox(message1, title1, choices)
    leaveid = random.randint(1, 1000)

    conn.execute("INSERT INTO status(leave_id,employee_id,leave,Date1,Date2,days,status) VALUES (?,?,?,?,?,?,?)",
                 (leaveid, fieldValues[0], choice, fieldValues[1], fieldValues[2], fieldValues[3], "Pending"))
    conn.commit()

def LeaveApproval():
    message = "Enter leave_id"
    title = "leave approval"
    fieldNames = ["Leave_id"]
    fieldValues = []
    fieldValues = multenterbox(message, title, fieldNames)
    message1 = "Approve/Deny"
    title1 = "leave approval"
    choices = ["approve", "deny"]
    choice = choicebox(message1, title1, choices)

    conn.execute("UPDATE status SET status = ? WHERE leave_id= ?", (choice, fieldValues[0]))
    conn.commit()

    if choice == 'approve':
        print(0)
        cur.execute("SELECT leave FROM status WHERE leave_id=?", (fieldValues[0],))
        row = cur.fetchall()
        col = row

        for row in conn.execute("SELECT employee_id FROM status WHERE leave_id=?", (fieldValues[0],)):
            print(2)
            exampleId = row[0]

        for row in conn.execute("SELECT days FROM status WHERE leave_id=?", (fieldValues[0],)):
            print(2)
            exampleDays = row[0]

        for row in conn.execute("SELECT sickleave from balance where employee_id=?", (exampleId,)):
            balance = row[0]
            print(balance)

        for row in conn.execute("SELECT maternityleave from balance where employee_id=?", (exampleId,)):
            balance1 = row[0]
            print(balance1)

        for row in conn.execute("SELECT emergencyleave from balance where employee_id=?", (exampleId,)):
            balance2 = row[0]
            print(balance2)

        if (col[0] == ('sickleave',)):
            print(3)
            conn.execute("UPDATE balance SET sickleave =? WHERE employee_id= ?", ((balance - exampleDays), (exampleId)))

        if (col[0] == ('maternityleave',)):
            print(3)
            conn.execute("UPDATE balance SET maternityleave =? WHERE employee_id= ?", ((balance1 - exampleDays), (exampleId)))

        if (col[0] == ('emergencyleave',)):
            print(3)
            conn.execute("UPDATE balance SET emergencyleave =? WHERE employee_id= ?", ((balance2 - exampleDays), (exampleId)))



def leavelist():
    leavelistwindow = Toplevel()
    txt = Text(leavelistwindow)
    for i in conn.execute('SELECT * FROM status'):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


def registration():
    message = "Enter Details of Employee"
    title = "Registration"
    fieldNames = ["Employee ID", "Name", "Contact Number", "Password"]
    fieldValues = []
    fieldValues = multpasswordbox(message, title, fieldNames)
    while 1:
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])

        if errmsg == "": break


        fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)
    conn.execute("INSERT INTO employee(employee_id,Name,ContactNumber,Password) VALUES (?,?,?,?)",
                 (fieldValues[0], fieldValues[1], fieldValues[2], fieldValues[3]))
    conn.execute("INSERT INTO balance(employee_id,sickleave,maternityleave,emergencyleave) VALUES (?,?,?,?)", (fieldValues[0], 12, 12, 50))
    conn.commit()


def EmployeeLoginWindow():
    # employee login window after successful login
    global LoginWindow
    LoginWindow = Toplevel()
    LoginWindow.wm_attributes('-fullscreen', '1')
    Background_Label = Label(LoginWindow, image=filename)
    Background_Label.place(x=0, y=0, relwidth=1, relheight=1)

    informationEmployee = Button(LoginWindow, text='Employee information', command=EmployeeInformationWindow, bd=12, relief=GROOVE, fg="blue", bg="#ffffb3",
                      font=("Calibri", 36, "bold"), pady=3)
    informationEmployee['font'] = BtnFont
    informationEmployee.pack(fill=X)

    submit = Button(LoginWindow, text='Submit Leave', command=apply, bd=12, relief=GROOVE, fg="blue", bg="#ffffb3",
                      font=("Calibri", 36, "bold"), pady=3)
    submit['font'] = BtnFont
    submit.pack(fill=X)

    LeaveBalance = Button(LoginWindow, text='Leave Balance', command=balance, bd=12, relief=GROOVE, fg="blue", bg="#ffffb3",
                      font=("Calibri", 36, "bold"), pady=3)
    LeaveBalance['font'] = BtnFont
    LeaveBalance.pack(fill=X)

    LeaveApplicationStatus = Button(LoginWindow, text='Last leave status', command=EmployeeLeaveStatus, bd=12, relief=GROOVE, fg="blue", bg="#ffffb3",
                      font=("Calibri", 36, "bold"), pady=3)
    LeaveApplicationStatus['font'] = BtnFont
    LeaveApplicationStatus.pack(fill=X)

    AllLeaveStatus = Button(LoginWindow, text='All leave status', command=EmployeeAllStatus, bd=12, relief=GROOVE, fg="blue", bg="#ffffb3",
                      font=("Calibri", 36, "bold"), pady=3)
    AllLeaveStatus['font'] = BtnFont
    AllLeaveStatus.pack(fill=X)


    LogoutBtn = Button(LoginWindow, text='Logout', bd=12, relief=GROOVE, fg="red", bg="#ffffb3",
                      font=("Calibri", 36, "bold"), pady=3, command=Employeelogout)
    LogoutBtn['font'] = BtnFont
    LogoutBtn.pack(fill=X)

    informationEmployee.pack()
    submit.pack()
    LeaveBalance.pack()
    LeaveApplicationStatus.pack()
    AllLeaveStatus.pack()
    LogoutBtn.pack()
    ExitBtn.pack()



def adminwindow():
    adminmainwindow = Toplevel()
    adminmainwindow.wm_attributes('-fullscreen', '1')
    Background_Label = Label(adminmainwindow, image=filename)

    Background_Label.place(x=0, y=0, relwidth=1, relheight=1)
    informationEmployee = Button(adminmainwindow, text='All Employee information', command=EmployeeAllInformationWindow, bd=12, relief=GROOVE, fg="green", bg="#ffffb3",
                      font=("NewTime Roman", 40, "bold"), pady=3)
    informationEmployee['font'] = BtnFont
    informationEmployee.pack(fill=X)



    LeaveListButton = Button(adminmainwindow, text='Leave approval list', command=leavelist, bd=12, relief=GROOVE, fg="green", bg="#ffffb3",
                      font=("NewTime Roman", 40, "bold"), pady=3)
    LeaveListButton['font'] = BtnFont
    LeaveListButton.pack(fill=X)

    ApprovalButton = Button(adminmainwindow, text='Approve leave', command=LeaveApproval, bd=12, relief=GROOVE, fg="green", bg="#ffffb3",
                      font=("NewTime Roman", 40, "bold"), pady=3)
    ApprovalButton['font'] = BtnFont
    ApprovalButton.pack(fill=X)

    LogoutBtn = Button(adminmainwindow, text='Logout', command=adminmainwindow.destroy, bd=12, relief=GROOVE, fg="red",
                     bg="#ffffb3",
                     font=("NewTime Roman", 40, "bold"), pady=3)
    LogoutBtn['font'] = BtnFont
    LogoutBtn.pack(fill=X)

    informationEmployee.pack()
    LeaveListButton.pack()
    ApprovalButton.pack()
    ExitBtn.pack()


root = Tk()
root.wm_attributes('-fullscreen', '1')
root.title("Eze Leave Management System")
root.iconbitmap(default='leavelogo.ico')
filename = PhotoImage(file="background.gif")
background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
BtnFont = Font(family='NewTime Roman(Body)', size=24)
MainLabel = Label(root, text="Leave Management System", bd=12, relief=GROOVE, fg="White", bg="green",
                      font=("NewTime Roman", 40, "bold"), pady=3)
MainLabel.pack(fill=X)
im = PhotoImage(file='login.gif')

AdminLgnBtn = Button(root, text='Admin login',  bd=12, relief=GROOVE, fg="green", bg="#ffffb3",
                      font=("NewTime Roman", 40, "bold"), pady=3, command=AdminLogin)
AdminLgnBtn['font'] = BtnFont
AdminLgnBtn.pack(fill=X)


LoginBtn = Button(root, text='Employee login', bd=12, relief=GROOVE, fg="green", bg="#ffffb3",
                      font=("NewTime Roman", 40, "bold"), pady=3, command=EmployeeLogin)
LoginBtn['font'] = BtnFont
LoginBtn.pack(fill=X)


EmployeeRegistration = Button(root, text='Employee registration', command=registration, bd=12, relief=GROOVE, fg="green", bg="#ffffb3",
                      font=("NewTime Roman", 40, "bold"), pady=3)
EmployeeRegistration['font'] = BtnFont
EmployeeRegistration.pack(fill=X)

ExitBtn = Button(root, text='Exit', command=root.destroy, bd=12, relief=GROOVE, fg="red", bg="#ffffb3",
                      font=("NewTime Roman", 40, "bold"), pady=3)
ExitBtn['font'] = BtnFont
ExitBtn.pack(fill=X)
MainLabel.pack()
AdminLgnBtn.pack()
LoginBtn.pack()
EmployeeRegistration.pack()
ExitBtn.pack()


root.mainloop()


