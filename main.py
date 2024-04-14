import tkinter
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os

# Define the Tkinter window
window = tkinter.Tk()
window.title("CRUD Application")

# Function to create tables in the database
def create_tables():
    db_file = os.path.join(os.getcwd(), 'data.db')  # Database file path
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Drop the existing tables if they exist
    cursor.execute("DROP TABLE IF EXISTS Customers")
    cursor.execute("DROP TABLE IF EXISTS Bikes")
    cursor.execute("DROP TABLE IF EXISTS Rentals")
    cursor.execute("DROP TABLE IF EXISTS Locations")
    cursor.execute("DROP TABLE IF EXISTS Statuses")
    
    # Recreate the tables
    cursor.execute('''CREATE TABLE Customers (
                        CustomerID INTEGER PRIMARY KEY,
                        FirstName TEXT,
                        LastName TEXT,
                        Email TEXT,
                        PhoneNumber TEXT)''')

    cursor.execute('''CREATE TABLE Bikes (
                    BikeID INTEGER PRIMARY KEY,
                    Model TEXT,
                    StatusID INTEGER,
                    LastMaintenanceDate TEXT,
                    LocationID INTEGER,
                    FOREIGN KEY (LocationID) REFERENCES Locations(LocationID) ON DELETE CASCADE,
                    FOREIGN KEY (StatusID) REFERENCES Statuses(StatusID) ON DELETE CASCADE)''')

    cursor.execute('''CREATE TABLE Rentals (
                        RentalID INTEGER PRIMARY KEY,
                        CustomerID INTEGER,
                        BikeID INTEGER,
                        RentalStartDate TEXT,
                        RentalEndDate TEXT,
                        Price DECIMAL(10, 2),
                        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE,
                        FOREIGN KEY (BikeID) REFERENCES Bikes(BikeID) ON DELETE CASCADE)''')

    cursor.execute('''CREATE TABLE Locations (
                        LocationID INTEGER PRIMARY KEY,
                        Address TEXT,
                        City TEXT,
                        State TEXT,
                        ZipCode TEXT)''')
    
    cursor.execute('''CREATE TABLE Statuses (
                        StatusID INTEGER PRIMARY KEY,
                        StatusDescription TEXT)''')
    
    conn.commit()
    conn.close()

# Function to insert data into Statuses
def insert_statuses():
    statuses = [
        ('Available',),
        ('Rented',),
        ('Under Maintenance',),
    ]
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.executemany('''INSERT INTO Statuses (StatusDescription) VALUES (?)''', statuses)
    conn.commit()
    conn.close()

# Function to insert data into Locations
def insert_locations():
    locations = [
        ('123 Pine St', 'Springfield', 'IL', '62701'),
        ('456 Maple Ave', 'Shelbyville', 'IL', '62565'),
        ('789 Oak Blvd', 'Capital City', 'IL', '60007'),
    ]
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.executemany('''INSERT INTO Locations (Address, City, State, ZipCode) VALUES (?, ?, ?, ?)''', locations)
    conn.commit()
    conn.close()

# Function to insert data into Customers
def insert_customers():
    customers = [
        ('John', 'Doe', 'johndoe@example.com', '555-1234'),
        ('Jane', 'Doe', 'janedoe@example.com', '555-5678'),
        ('Jim', 'Beam', 'jimbeam@example.com', '555-9012'),
    ]
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.executemany('''INSERT INTO Customers (FirstName, LastName, Email, PhoneNumber) VALUES (?, ?, ?, ?)''', customers)
    conn.commit()
    conn.close()

# Function to insert data into Bikes
def insert_bikes():
    bikes = [
        ('Mountain 1000', 1, '2023-03-15'),  # StatusID 1 for 'Available'
        ('Road 550', 2, '2023-03-20'),        # StatusID 2 for 'Rented'
        ('Hybrid 300', 3, '2023-03-25')       # StatusID 3 for 'Under Maintenance'
    ]
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.executemany('''INSERT INTO Bikes (Model, StatusID, LastMaintenanceDate) VALUES (?, ?, ?)''', bikes)
    conn.commit()
    conn.close()

# Function to insert data into Rentals
def insert_rentals():
    rentals = [
        (1, 2, '2023-04-01', '2023-04-03', 29.99),
        (2, 1, '2023-04-02', '2023-04-04', 39.99),
    ]
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.executemany('''INSERT INTO Rentals (CustomerID, BikeID, RentalStartDate, RentalEndDate, Price) VALUES (?, ?, ?, ?, ?)''', rentals)
    conn.commit()
    conn.close()

# Function to execute a query and display results
def execute_query_and_display_result(sql_query, result_text_widget):
    # Execute the SQL query
    conn = sqlite3.connect('data.db')
    cursor = conn.execute(sql_query)
    result = cursor.fetchall()
    conn.close()

    # Display the result in the text widget
    result_text_widget.delete(1.0, tkinter.END)
    for row in result:
        result_text_widget.insert(tkinter.END, row_to_string(row) + '\n')

# Convert a row to a formatted string
def row_to_string(row):
    return ', '.join(map(str, row))

# Function to display customers
def display_customers():
    query = "SELECT * FROM Customers"
    execute_query_and_display_result(query, result_text_customers)

# Function to display bikes
def display_bikes():
    query = "SELECT * FROM Bikes"
    execute_query_and_display_result(query, result_text_bikes)

# Function to display rentals
def display_rentals():
    query = "SELECT * FROM Rentals"
    execute_query_and_display_result(query, result_text_rentals)

# Function to display customers with all the bikes they rented
def display_customers_with_bikes():
    query = '''
    SELECT Customers.FirstName, Customers.LastName, GROUP_CONCAT(Bikes.Model, ', ') AS RentedBikes
    FROM Customers
    JOIN Rentals ON Customers.CustomerID = Rentals.CustomerID
    JOIN Bikes ON Rentals.BikeID = Bikes.BikeID
    GROUP BY Customers.FirstName, Customers.LastName
    '''
    execute_query_and_display_result(query, result_text_customers_with_bikes)

# Function to display bikes in the order of popularity
def display_bikes_by_popularity():
    query = '''
    SELECT Bikes.Model, COUNT(Rentals.RentalID) AS RentalsCount
    FROM Bikes
    LEFT JOIN Rentals ON Bikes.BikeID = Rentals.BikeID
    GROUP BY Bikes.Model
    ORDER BY RentalsCount DESC
    '''
    execute_query_and_display_result(query, result_text_bikes_by_popularity)

# Define entry fields and labels for CRUD operations
label_customer_id = tkinter.Label(window, text="Customer ID:")
label_customer_id.grid(row=1, column=0, padx=5, pady=5)

entry_customer_id = tkinter.Entry(window)
entry_customer_id.grid(row=1, column=1, padx=5, pady=5)

label_first_name = tkinter.Label(window, text="First Name:")
label_first_name.grid(row=2, column=0, padx=5, pady=5)

entry_first_name = tkinter.Entry(window)
entry_first_name.grid(row=2, column=1, padx=5, pady=5)

label_last_name = tkinter.Label(window, text="Last Name:")
label_last_name.grid(row=3, column=0, padx=5, pady=5)

entry_last_name = tkinter.Entry(window)
entry_last_name.grid(row=3, column=1, padx=5, pady=5)

label_email = tkinter.Label(window, text="Email:")
label_email.grid(row=4, column=0, padx=5, pady=5)

entry_email = tkinter.Entry(window)
entry_email.grid(row=4, column=1, padx=5, pady=5)

label_phone = tkinter.Label(window, text="Phone:")
label_phone.grid(row=5, column=0, padx=5, pady=5)

entry_phone = tkinter.Entry(window)
entry_phone.grid(row=5, column=1, padx=5, pady=5)

# Define buttons for CRUD operations
button_insert_customer = tkinter.Button(window, text="Insert Customer", command=insert_customers)
button_insert_customer.grid(row=6, column=0, padx=5, pady=5)

button_update_customer = tkinter.Button(window, text="Update Customer")
button_update_customer.grid(row=6, column=1, padx=5, pady=5)

button_delete_customer = tkinter.Button(window, text="Delete Customer")
button_delete_customer.grid(row=6, column=2, padx=5, pady=5)

# Define buttons to display results
button_display_customers = tkinter.Button(window, text="Display Customers", command=display_customers)
button_display_customers.grid(row=8, column=0, padx=5, pady=5)

button_display_bikes = tkinter.Button(window, text="Display Bikes", command=display_bikes)
button_display_bikes.grid(row=8, column=1, padx=5, pady=5)

button_display_rentals = tkinter.Button(window, text="Display Rentals", command=display_rentals)
button_display_rentals.grid(row=8, column=2, padx=5, pady=5)

# Define labels for each query result
label_customers = tkinter.Label(window, text="Customers:")
label_customers.grid(row=9, column=0, padx=5, pady=5)

label_bikes = tkinter.Label(window, text="Bikes:")
label_bikes.grid(row=9, column=1, padx=5, pady=5)

label_rentals = tkinter.Label(window, text="Rentals:")
label_rentals.grid(row=9, column=2, padx=5, pady=5)

# Define text widgets to display query results
result_text_customers = tkinter.Text(window, width=30, height=10)
result_text_customers.grid(row=10, column=0, padx=5, pady=5)

result_text_bikes = tkinter.Text(window, width=30, height=10)
result_text_bikes.grid(row=10, column=1, padx=5, pady=5)

result_text_rentals = tkinter.Text(window, width=30, height=10)
result_text_rentals.grid(row=10, column=2, padx=5, pady=5)

# Define buttons for predefined SQL join queries
button_display_customers_with_bikes = tkinter.Button(window, text="Customers with Bikes", command=display_customers_with_bikes)
button_display_customers_with_bikes.grid(row=11, column=0, padx=5, pady=5)

button_display_bikes_by_popularity = tkinter.Button(window, text="Bikes by Popularity", command=display_bikes_by_popularity)
button_display_bikes_by_popularity.grid(row=11, column=2, padx=5, pady=5)

# Define text widgets to display results for predefined SQL join queries
result_text_customers_with_bikes = tkinter.Text(window, width=50, height=10)
result_text_customers_with_bikes.grid(row=12, column=0, columnspan=2, padx=5, pady=5)

result_text_bikes_by_popularity = tkinter.Text(window, width=50, height=10)
result_text_bikes_by_popularity.grid(row=12, column=2, padx=5, pady=5)

# Call the function to create tables before any operations
create_tables()

# Call the functions to insert data
insert_statuses()
insert_locations()
insert_customers()
insert_bikes()
insert_rentals()

# Define example queries
query_customers = "SELECT * FROM Customers"
query_bikes = "SELECT * FROM Bikes"
query_rentals = "SELECT * FROM Rentals"

# Display query results
execute_query_and_display_result(query_customers, result_text_customers)
execute_query_and_display_result(query_bikes, result_text_bikes)
execute_query_and_display_result(query_rentals, result_text_rentals)

window.mainloop()
