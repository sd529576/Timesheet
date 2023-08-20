import tkinter
from tkinter import *
from tkinter import messagebox
from Timesheet_server import *
import Timesheet_server
 
window = tkinter.Tk()
window.title("Login Page for timesheet")
window.geometry('750x550')
window.configure(bg = '#eeeeee')
bg = PhotoImage(file = "bg_Image.png")
background = Label(window,image = bg)
background.place(x=0,y=50)

dict1 = {}
keys = []
insert_query = ""
primary = 0
data_sql = "SELECT user_name, password FROM Login_Info"
primary_sql = "SELECT login_id, user_name, password FROM Login_Info"
i = 0

class Login:
    def __init__(self,id,password):
        self.id = id
        self.password = password

    def login(self):
        global ID_entry_val
        data_fetching(connection,data_sql)
        ID_entry_val = id_entry.get()
        if (id_entry.get(),password_entry.get()) in Timesheet_server.result:
            messagebox.showinfo(title = "Login successful!", message= "you successfully logged in!")
            window.destroy()
            import Timesheet_Main
            # need to add another tap with timesheet given
        else:
            messagebox.showerror(title = "invalid login", message= "try again.")

    def signup(self):
        global keys
        global primary
        data_fetching(connection,primary_sql)
        # Conditional statement to implement the primary key and auto-incremented values
        if len(Timesheet_server.result) == 0:
            primary = 0
            insert_login_query = """ INSERT INTO Login_Info VALUES (%s,%s,%s)"""
            Insert_login_query(connection,insert_login_query,primary,id_entry.get(),password_entry.get())
            #initial values with only specific username given / will be updated through add/edit hour section later.
            insert_user_query ="""INSERT INTO user_info VALUES (%s,%s,%s,%s,%s)"""
            Insert_user_info_query(connection,insert_user_query,id_entry.get(),None,None,None,None)
            messagebox.showinfo(title = "Sign-up Completed", message= "Sign up was successful! you can log into your timesheet now!")
        else:
            primary = Timesheet_server.result[-1][0] + 1
            for i in Timesheet_server.result:
                a = (i[0],id_entry.get(),password_entry.get())
                print(a)
            if id_entry.get() in i[1]:
                messagebox.showinfo(title = "Already have the account", message= "Username already taken!, try other username.")
            else:
                insert_login_query = """ INSERT INTO Login_Info VALUES (%s,%s,%s)"""
                Insert_login_query(connection,insert_login_query,primary,id_entry.get(),password_entry.get())
                messagebox.showinfo(title = "Sign-up Completed", message= "Sign up was successful! you can log into your timesheet now!")
                insert_user_query ="""INSERT INTO user_info VALUES (%s,%s,%s,%s,%s)"""
                Insert_user_info_query(connection,insert_user_query,id_entry.get(),None,None,None,None)


id_label = tkinter.Label(window, text="Username", bg='#a1e9d1', fg="#000000", font=("Arial", 16, 'bold'))
password_label = tkinter.Label(window, text="Password", bg='#a1e9d1', fg="#000000", font=("Arial", 16, 'bold'))
timesheet_label = tkinter.Label(window,text = "Timesheet", fg ="#000000", font = ("Arial", 30))

id_entry = tkinter.Entry(window,font = ("Arial",16))
password_entry = tkinter.Entry(window,font = ("Arial",16))


login = Login(id_entry,password_entry)

Login_button = tkinter.Button(window,text = " Login ", bg = "#50C878", font=("Arial",16),command = login.login)
signup_button = tkinter.Button(window,text = "signup",bg = "#50C878", font=("Arial",16), command = login.signup)

# positions:
timesheet_label.place(x = 275, y = 0)
id_label.place(x = 400, y= 150)
password_label.place(x = 400, y = 200)
id_entry.place(x = 520 , y = 150, width = 200)
password_entry.place(x = 520, y = 200, width = 200)
Login_button.place(x = 460, y = 250)
signup_button.place(x = 560, y = 250)


window.mainloop()