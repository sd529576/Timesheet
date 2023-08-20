import tkinter
from tkinter import *
from tkcalendar import DateEntry
from Timesheet_server import *
import Timesheet_server
import Timesheet_login
#I have to close the display initially to stop the duplicates / Importing issues.
Timesheet_login.window.destroy

travel_state = ""
note_var = ""
# Declaring new variable from the id_entry variable declared from Timesheet_login.py
username = Timesheet_login.ID_entry_val
update_target = ()
a = 150
dict1 = {}
last_value = 0
b = 0
 
window_ts = tkinter.Tk()
window_ts.title("Timesheet Page")
window_ts.geometry("1920x1080")
window_ts.configure(bg = '#eeeeee')
frame_main = tkinter.Frame(bg='#eeeeee')
canvas = Canvas()

def check_travel():
    global status
    global travel_state
    if status.get() == 0:
        travel_state = "X"
    else:
        travel_state = "O"
        #print(username)

# Found alternative ways of simply updating the values by using add/edit hours feature 

def update():
    global calendar_entry,Hours_entry,Note_text_entry,update_target,travel_state
    global a,last_value
    global dict1
    query = "SELECT user_name,Date,Hours,Notes FROM user_info"
    data_fetching(connection,query)
    print(Timesheet_server.result)
    calendar_val = calendar_entry.get()
    # needed to create an iterator to be able to loop through every tuple element in result list.
    list1 = []
    for i in range(len(Timesheet_server.result)):
        list1.append(Timesheet_server.result[i][1])
    print(list1)
    print(calendar_val)
    if calendar_val not in list1:
        insert_user_query ="""INSERT INTO user_info VALUES (%s,%s,%s,%s,%s)"""
        Insert_user_info_query(connection,insert_user_query,username[0],calendar_entry.get(),Hours_entry.get(),travel_state,Note_text_entry.get("1.0","end-1c"))
        Timesheet_rows = tkinter.Label(canvas,text = "{}      {}hours        Notes: {}    Travel:  {}" .format(calendar_entry.get(),Hours_entry.get(),Note_text_entry.get("1.0","end-1c"),travel_state), bg ="#E0E0E0", fg = "#000000", font = ("Arial",15,'bold'),width = 85,height = 2)
        Timesheet_rows.place(x = 450,y = a)
        dict1[calendar_val] = a
        a += 50 

    else:
        update_user_info_query = """UPDATE User_info
    SET Date = %s, Hours = %s, Notes = %s ,Travel = %s WHERE user_name = %s AND Date = %s"""
        Insert_user_query(connection,update_user_info_query,calendar_entry.get(),Hours_entry.get(),Note_text_entry.get("1.0","end-1c"),username[0],travel_state)
        Timesheet_rows = tkinter.Label(canvas,text = "{}      {}hours        Notes: {}    Travel:  {}".format(calendar_entry.get(),Hours_entry.get(),Note_text_entry.get("1.0","end-1c"),travel_state), bg ="#E0E0E0", fg = "#000000", font = ("Arial",15,'bold'),width = 85,height = 2)
        Timesheet_rows.place(x= 450, y = dict1[calendar_val])

def orderby_date():
    global a,dict1
    a = 150
    query = "SELECT user_name,Date,Hours,Travel,Notes FROM user_info WHERE user_name = %s ORDER BY DATE"
    user_name_filtering(connection,query,[username])
    for i in range(1,len(Timesheet_server.result)):
        #print(Timesheet_server.result[i][0])
        Timesheet_rows = tkinter.Label(canvas,text = "{}      {}hours        Notes: {}    Travel:  {}".format(Timesheet_server.result[i][1],Timesheet_server.result[i][2],Timesheet_server.result[i][4],Timesheet_server.result[i][3]), bg ="#E0E0E0", fg = "#000000", font = ("Arial",15,'bold'),width = 85,height = 2)
        Timesheet_rows.place(x= 450, y = a)
        dict1[Timesheet_server.result[i][1]] = a
        a += 50

def Summary_get():
    hours_list = {}
    total_hours = 0
    months_list = {"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}

    # filtering through the value given by the OptionMenu entry and filtering through each month. Query is structured in a way to filter starting certain number in a list. constructing dictionary to represent 
    # the number to the actual string of each months.
    
    for i in months_list:
        if month_status.get() == i:
            query = "SELECT user_name,Date,Hours FROM user_info WHERE Date LIKE '%s%'"
            Filtering_Dates(connection,query,[months_list[i]])
            print(Timesheet_server.result)

    for i in range(len(Timesheet_server.result)):
        hours_list[Timesheet_server.result[i][1]] = int(Timesheet_server.result[i][2])
    
    # adding total hours from hours_list updated from the loop above.
    for j in range(len(hours_list)):
        total_hours += hours_list[Timesheet_server.result[j][1]]
    
    # Adding big blank strings initially to not leave the strings that's already labeled. Had an issue trying to erase the label and didn't work out well.
    Total_hrs_label = tkinter.Label(canvas,text = '      ' ,bg ="#87CEEB",fg = "#000000", font = ("Arial,32,'bold"))
    Total_hrs_label.place(x = 250, y = 200)
    # actual total hours labeling in the summary section
    Total_hrs_label = tkinter.Label(canvas,text = total_hours ,bg ="#87CEEB",fg = "#000000", font = ("Arial,32,'bold"))
    Total_hrs_label.place(x = 250, y = 200)

    print(total_hours)
    print(hours_list)
#still need improvement

# def delete():
#     global delete_entry
#     print(delete_entry.get())
#     query = """DELETE FROM user_info where Date = %s"""
#     delete_user_info_query(connection,query,[delete_entry.get()])

# Labels / entry
Timesheet_label1 = tkinter.Label(frame_main,text= "Timesheet Entry", fg = "#000000", font = ("Arial",32,'bold'))
Summary_label = tkinter.Label(canvas,text = "Summary",bg = "#87CEEB", fg = "#FFFFFF", font = ("Arial",26,'bold'))
Total_hrs_info_label = tkinter.Label(canvas,text = "Total Hours worked in :" ,bg ="#87CEEB",fg = "#000000", font = ("Arial,32,'bold"))
#Total_hrs_month_label = tkinter.Label(canvas,textvariable= variable,bg ="#87CEEB",fg = "#000000", font = ("Arial,32,'bold"))
Add_edit_label = tkinter.Label(canvas,text = "Add/Edit Hour",bg ="#778899", fg = "#FFFFFF", font = ("Arial",26,'bold'))
choose_date_label = tkinter.Label(canvas,text = "Choose a Date:",bg ="#778899", fg = "#000000", font = ("Arial",15,'bold'))
calendar_entry = DateEntry(window_ts,selectmode='day',year=2023)

ww = calendar_entry.get().replace("/",",")
print(ww)

Hours_label = tkinter.Label(canvas,text = "Hours:",bg ="#778899", fg = "#000000", font = ("Arial",15,'bold'))
Hours_entry = tkinter.Entry(window_ts,font = ("Arial",16))
status = IntVar()
month_status = StringVar()

Travel_label = tkinter.Checkbutton(window_ts, text = "Travel" ,bg = "#778899", font= ("Arial",16),variable = status,command = check_travel)
Note_text_label = tkinter.Label(canvas,text="Note:",bg ="#778899", fg = "#000000", font = ("Arial",15,'bold'))
Note_text_entry = tkinter.Text(canvas,font = ("Arial",12),width = 25,height = 7)
#delete_entry = tkinter.Entry(window_ts,font = ("Arial",16))

#Button
Save_button = tkinter.Button(canvas,text = "Save", bg = "#eeeeee",font= ("Arial",16), command = update)
update_button = tkinter.Button(canvas,text = "Update", bg ="#87CEEB",fg = "#000000", font = ("Arial",16), command = Summary_get)
#Delete_button = tkinter.Button(canvas,text = "Delete", bg = "#D3D3D3", font = ("Arial",16), command = delete)
month_menu = OptionMenu(canvas,month_status,"January","February","March","April","May","June","July","August","September","October","November","December")

# Creating separate spaces for each section
canvas.create_rectangle(0, 100, 400, 800, fill="#87CEEB")
canvas.create_rectangle(400, 100, 1520, 800, fill="#D3D3D3")
canvas.create_rectangle(1520,100,1920,800,fill="#778899")

# Label fixed position (grid)
Timesheet_label1.grid(column = 0)

# Label fixed position (x,y)
Summary_label.place(x=120,y=120)
Total_hrs_info_label.place(x = 60, y= 200)
#Total_hrs_month_label.place(x = 250, y = 200)
Add_edit_label.place(x=1600,y=120)
choose_date_label.place(x=1540,y=180)
calendar_entry.place(x=1570,y=270)
Hours_label.place(x=1540,y=450)
Hours_entry.place(x=1570,y=550)
Travel_label.place(x=1540,y=600)
Note_text_label.place(x = 1540,y=580)
Note_text_entry.place(x=1570,y =620)
Save_button.place(x=1825,y=650)
# delete_entry.place(x= 1150, y= 750)
# Delete_button.place(x = 1400, y = 680)
update_button.place(x = 60, y = 480)
month_menu.place(x = 250, y = 170)

# Testing
# Only consider the values, which are from the login value/ID_entry(username) = the database rows.
query = "SELECT user_name,Date,Hours,Travel,Notes FROM user_info WHERE user_name = %s ORDER BY DATE"
user_name_filtering(connection,query,[username])


#need to find a way to display only the user's timesheet values. Curretly showing all the rows including the other username values. Potnetially using Id_entry but it's not working. (Completed)
# Still need to brush up on displaying them.

for i in range(1,len(Timesheet_server.result)):
    #print(Timesheet_server.result[i][0])
    Timesheet_rows = tkinter.Label(canvas,text = "{}      {}hours        Notes: {}    Travel:  {}".format(Timesheet_server.result[i][1],Timesheet_server.result[i][2],Timesheet_server.result[i][4],Timesheet_server.result[i][3]), bg ="#E0E0E0", fg = "#000000", font = ("Arial",15,'bold'),width = 85,height = 2)
    Timesheet_rows.place(x= 450, y = a)
    dict1[Timesheet_server.result[i][1]] = a
    a += 50


frame_main.pack()
canvas.pack(fill= BOTH,expand=1)

#window_ts.mainloop()