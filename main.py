import tkinter
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def enter_data():
    accepted = accept_var.get()
    
    if accepted=="Accepted":
        # User info
        FirstName = first_name_entry.get()
        LastName = last_name_entry.get()
        
        if FirstName and LastName:
            Email = Email_entry.get()
            PhoneNumber = PhoneNumber_entry.get()
            
            # register info
            registration_status = reg_status_var.get()

            
            print("First name: ", FirstName, "Last name: ", LastName)
            print("Email: ", Email, "PhoneNumber: ", PhoneNumber)
            print("------------------------------------------")
            
            # Create Table
            conn = sqlite3.connect('data.db')
            table_create_query = '''CREATE TABLE IF NOT EXISTS Student_Data 
                    (FirstName TEXT, LastName TEXT, Email TEXT, PhoneNumber TEXT, 
                    registration_status TEXT)
            '''
            conn.execute(table_create_query)
            
            # Insert Data
            data_insert_query = '''INSERT INTO Student_Data (FirstName, LastName, Email, 
            PhoneNumber, registration_status) VALUES 
            (?, ?, ?, ?, ?, ?, ?, ?)'''
            data_insert_tuple = (FirstName, LastName, Email,
                                  PhoneNumber, registration_status)
            cursor = conn.cursor()
            cursor.execute(data_insert_query, data_insert_tuple)
            conn.commit()
            conn.close()

            
                
        else:
            tkinter.messagebox.showwarning(Email="Error", message="First name and last name are required.")
    else:
        tkinter.messagebox.showwarning(Email= "Error", message="You have not accepted the terms")

window = tkinter.Tk()
window.Email("Data Entry Form")

frame = tkinter.Frame(window)
frame.pack()

# Saving User Info
user_info_frame =tkinter.LabelFrame(frame, text="User Information")
user_info_frame.grid(row= 0, column=0, padx=20, pady=10)

first_name_label = tkinter.Label(user_info_frame, text="First Name")
first_name_label.grid(row=0, column=0)
last_name_label = tkinter.Label(user_info_frame, text="Last Name")
last_name_label.grid(row=0, column=1)

first_name_entry = tkinter.Entry(user_info_frame)
last_name_entry = tkinter.Entry(user_info_frame)
first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)

Email_label = tkinter.Label(user_info_frame, text="Email")
Email_entry = tkinter.Entry(user_info_frame)
Email_label.grid(row=0, column=2)
Email_entry.grid(row=1, column=2)

PhoneNumber_label = tkinter.Label(user_info_frame, text="PhoneNumber")
PhoneNumber_entry = tkinter.Entry(user_info_frame)
PhoneNumber_label.grid(row=2, column=1)
PhoneNumber_entry.grid(row=3, column=1)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Saving Course Info
courses_frame = tkinter.LabelFrame(frame)
courses_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

registered_label = tkinter.Label(courses_frame, text="Registration Status")

reg_status_var = tkinter.StringVar(value="Not Registered")
registered_check = tkinter.Checkbutton(courses_frame, text="Currently Registered",
                                       variable=reg_status_var, onvalue="Registered", offvalue="Not registered")

registered_label.grid(row=0, column=0)
registered_check.grid(row=1, column=0)


for widget in courses_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Accept terms
terms_frame = tkinter.LabelFrame(frame, text="Terms & Conditions")
terms_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

accept_var = tkinter.StringVar(value="Not Accepted")
terms_check = tkinter.Checkbutton(terms_frame, text= "I accept the terms and conditions.",
                                  variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
terms_check.grid(row=0, column=0)

# Button
button = tkinter.Button(frame, text="Enter data", command= enter_data)
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)
 
window.mainloop()