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
    db_file = os.path.join(os.getcwd(), 'Database_project.db')  # Database file path
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
    conn = sqlite3.connect('Database_project.db')
    cursor = conn.cursor()
    
    # Check if each status already exists before inserting
    for status in statuses:
        cursor.execute("SELECT * FROM Statuses WHERE StatusDescription=?", status)
        existing_status = cursor.fetchone()
        if existing_status is None:
            cursor.execute('''INSERT INTO Statuses (StatusDescription) VALUES (?)''', status)
    
    conn.commit()
    conn.close()

def insert_location():
    print("Inserting locations...")
    try:
        # Insert predefined locations into the database
        conn = sqlite3.connect('Database_project.db')
        cursor = conn.cursor()
        locations = [
            ('123 Pine St', 'Springfield', 'IL', '62701'),
            ('456 Maple Ave', 'Shelbyville', 'IL', '62565'),
            ('789 Oak Blvd', 'Capital City', 'IL', '60007'),
        ]
        # Check if each location already exists before inserting
        for location in locations:
            cursor.execute("SELECT * FROM Locations WHERE Address=? AND City=? AND State=? AND ZipCode=?", location)
            existing_location = cursor.fetchone()
            if existing_location is None:
                print(f"Inserting location: {location}")
                cursor.execute('''INSERT INTO Locations (Address, City, State, ZipCode) VALUES (?, ?, ?, ?)''', location)
            else:
                print(f"Location already exists: {location}")
        
        conn.commit()
        print("Location insertion complete.")

        # Retrieve data from entry fields
        address = entry_address.get()
        city = entry_city.get()
        state = entry_state.get()
        zip_code = entry_zip.get()

        # Prepare location data
        location = (address, city, state, zip_code)

        # Insert the location into the database
        cursor.execute('''INSERT INTO Locations (Address, City, State, ZipCode) VALUES (?, ?, ?, ?)''', location)
        conn.commit()
        print("Success", "Location added successfully")
        
    except sqlite3.Error as e:
        print(f"Error inserting locations: {e}")
        messagebox.showerror("Error", f"Failed to add location: {e}")
        
    finally:
        # Close the database connection
        conn.close()

# Update Location Function
def update_location():
    location_id = entry_location_id.get()  # Get the location ID from the entry widget
    if not location_id:
        messagebox.showerror("Error", "Please enter a Location ID")
        return

    # Retrieve updated data from entry fields
    address = entry_address.get()
    city = entry_city.get()
    state = entry_state.get()
    zip_code = entry_zip.get()

    conn = sqlite3.connect('Database_project.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Locations SET Address=?, City=?, State=?, ZipCode=? WHERE LocationID=?",
                   (address, city, state, zip_code, location_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Location updated successfully")

# Delete Location Function
def delete_location():
    location_id = entry_location_id.get()  # Get the location ID from the entry widget
    if not location_id:
        messagebox.showerror("Error", "Please enter a Location ID")
        return

    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this location?")
    if confirm:
        conn = sqlite3.connect('Database_project.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Locations WHERE LocationID=?", (location_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Location deleted successfully")

# Function to insert data into Customers
def insert_customer():
    print("Inserting customers...")
    try:
        # Insert predefined customers into the database
        conn = sqlite3.connect('Database_project.db')
        cursor = conn.cursor()
        customers = [
            ('John', 'Doe', 'johndoe@example.com', '555-1234'),
            ('Jane', 'Doe', 'janedoe@example.com', '555-5678'),
            ('Jim', 'Beam', 'jimbeam@example.com', '555-9012'),
        ]
        # Check if each customer already exists before inserting
        for customer in customers:
            cursor.execute("SELECT * FROM Customers WHERE FirstName=? AND LastName=? AND Email=? AND PhoneNumber=?", customer)
            existing_customer = cursor.fetchone()
            if existing_customer is None:
                print(f"Inserting customer: {customer}")
                cursor.execute('''INSERT INTO Customers (FirstName, LastName, Email, PhoneNumber) VALUES (?, ?, ?, ?)''', customer)
            else:
                print(f"Customer already exists: {customer}")
        
        conn.commit()
        print("Customer insertion complete.")

        # Retrieve data from entry fields
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        email = entry_email.get()
        phone = entry_phone.get()
        
        # Prepare customer data
        customer = (first_name, last_name, email, phone)

        # Insert the customer into the database
        cursor.execute('''INSERT INTO Customers (FirstName, LastName, Email, PhoneNumber) VALUES (?, ?, ?, ?)''', customer)
        conn.commit()
        print("Success", "Customer added successfully")
        
    except sqlite3.Error as e:
        print(f"Error inserting customers: {e}")
        messagebox.showerror("Error", f"Failed to add customer: {e}")
        
    finally:
        # Close the database connection
        conn.close()

# Update Customer Function
def update_customer():
    customer_id = entry_customer_id.get()
    if not customer_id:
        messagebox.showerror("Error", "Please enter a Customer ID")
        return

    # Retrieve updated data from entry fields
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    phone = entry_phone.get()

    conn = sqlite3.connect('Database_project.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Customers SET FirstName=?, LastName=?, Email=?, PhoneNumber=? WHERE CustomerID=?",
                   (first_name, last_name, email, phone, customer_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Customer updated successfully")

# Delete Customer Function
def delete_customer():
    customer_id = entry_customer_id.get()
    if not customer_id:
        messagebox.showerror("Error", "Please enter a Customer ID")
        return

    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this customer?")
    if confirm:
        conn = sqlite3.connect('Database_project.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Customers WHERE CustomerID=?", (customer_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Customer deleted successfully")

# Function to insert data into Bikes
def insert_bike():
    print("Inserting bikes...")
    try:
        # Insert predefined bikes into the database
        conn = sqlite3.connect('Database_project.db')
        cursor = conn.cursor()
        bikes = [
            ('Mountain 1000', 1, '2023-03-15'),  # StatusID 1 for 'Available'
            ('Road 550', 2, '2023-03-20'),        # StatusID 2 for 'Rented'
            ('Hybrid 300', 3, '2023-03-25')       # StatusID 3 for 'Under Maintenance'
        ]
        # Check if each bike already exists before inserting
        for bike in bikes:
            cursor.execute("SELECT * FROM Bikes WHERE Model=? AND StatusID=? AND LastMaintenanceDate=?", bike)
            existing_bike = cursor.fetchone()
            if existing_bike is None:
                print(f"Inserting bike: {bike}")
                cursor.execute('''INSERT INTO Bikes (Model, StatusID, LastMaintenanceDate) VALUES (?, ?, ?)''', bike)
            else:
                print(f"Bike already exists: {bike}")
        
        conn.commit()
        print("Bike insertion complete.")

        # Retrieve data from entry fields
        model = entry_model.get()
        status_id = entry_status_id.get()
        last_maintenance = entry_last_maintenance.get()

        # Prepare bike data
        bike = (model, status_id, last_maintenance)

        # Insert the bike into the database
        cursor.execute('''INSERT INTO Bikes (Model, StatusID, LastMaintenanceDate) VALUES (?, ?, ?)''', bike)
        conn.commit()
        print("Success", "Bike added successfully")
        
    except sqlite3.Error as e:
        print(f"Error inserting bikes: {e}")
        messagebox.showerror("Error", f"Failed to add bike: {e}")
        
    finally:
        # Close the database connection
        conn.close()

# Update Bike Function
def update_bike():
    bike_id = entry_bike_id.get()
    if not bike_id:
        messagebox.showerror("Error", "Please enter a Bike ID")
        return

    # Retrieve updated data from entry fields
    model = entry_model.get()
    status_id = entry_status_id.get()
    last_maintenance = entry_last_maintenance.get()

    conn = sqlite3.connect('Database_project.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Bikes SET Model=?, StatusID=?, LastMaintenanceDate=? WHERE BikeID=?",
                   (model, status_id, last_maintenance, bike_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Bike updated successfully")

# Delete Bike Function
def delete_bike():
    bike_id = entry_bike_id.get()
    if not bike_id:
        messagebox.showerror("Error", "Please enter a Bike ID")
        return

    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this bike?")
    if confirm:
        conn = sqlite3.connect('Database_project.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Bikes WHERE BikeID=?", (bike_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Bike deleted successfully")

# Function to insert data into Rentals
def insert_rental():
    print("Inserting rentals...")
    try:
        # Insert predefined rentals into the database
        conn = sqlite3.connect('Database_project.db')
        cursor = conn.cursor()
        rentals = [
            (1, 2, '2023-04-01', '2023-04-03', 29.99),
            (2, 1, '2023-04-02', '2023-04-04', 39.99),
        ]
        # Check if each rental already exists before inserting
        for rental in rentals:
            cursor.execute("SELECT * FROM Rentals WHERE CustomerID=? AND BikeID=? AND RentalStartDate=? AND RentalEndDate=? AND Price=?", rental)
            existing_rental = cursor.fetchone()
            if existing_rental is None:
                print(f"Inserting rental: {rental}")
                cursor.execute('''INSERT INTO Rentals (CustomerID, BikeID, RentalStartDate, RentalEndDate, Price) VALUES (?, ?, ?, ?, ?)''', rental)
            else:
                print(f"Rental already exists: {rental}")
        
        conn.commit()
        print("Rental insertion complete.")

        # Retrieve data from entry fields
        customer_id = entry_customer_id_rental.get()
        bike_id = entry_bike_id_rental.get()
        start_date = entry_start_date.get()
        end_date = entry_end_date.get()
        price = entry_price.get()
        
        # Prepare rental data
        rental = (customer_id, bike_id, start_date, end_date, price)

        # Insert the rental into the database
        cursor.execute('''INSERT INTO Rentals (CustomerID, BikeID, RentalStartDate, RentalEndDate, Price) VALUES (?, ?, ?, ?, ?)''', rental)
        conn.commit()
        print("Success", "Rental added successfully")
        
    except sqlite3.Error as e:
        print(f"Error inserting rentals: {e}")
        messagebox.showerror("Error", f"Failed to add rental: {e}")
        
    finally:
        # Close the database connection
        conn.close()

# Update Rental Function
def update_rental():
    rental_id_value = entry_customer_id_rental.get()
    if not rental_id_value:
        messagebox.showerror("Error", "Please enter a Rental ID")
        return

    # Retrieve updated data from entry fields
    customer_id = entry_customer_id_rental.get()
    bike_id = entry_bike_id_rental.get()
    start_date = entry_start_date.get()
    end_date = entry_end_date.get()
    price = entry_price.get()

    conn = sqlite3.connect('Database_project.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Rentals SET CustomerID=?, BikeID=?, RentalStartDate=?, RentalEndDate=?, Price=? WHERE RentalID=?",
                   (customer_id, bike_id, start_date, end_date, price, rental_id_value))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Rental updated successfully")

# Delete Rental Function
def delete_rental():
    rental_id_value = entry_customer_id_rental.get()
    if not rental_id_value:
        messagebox.showerror("Error", "Please enter a Rental ID")
        return

    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this rental?")
    if confirm:
        conn = sqlite3.connect('Database_project.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Rentals WHERE RentalID=?", (rental_id_value,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Rental deleted successfully")

# Function to execute a query and display results
def execute_query_and_display_result(sql_query, result_text_widget):
    # Execute the SQL query
    conn = sqlite3.connect('Database_project.db')
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

# Function to display locations
def display_locations():
    query = "SELECT * FROM Locations"
    execute_query_and_display_result(query, result_text_locations)

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

# Define labels for each Table
label_customers = tkinter.Label(window, text="Customers:")
label_customers.grid(row=0, column=1, padx=5, pady=5)

label_locations = tkinter.Label(window, text="Locations:")
label_locations.grid(row=6, column=1, padx=5, pady=5)

label_bikes = tkinter.Label(window, text="Bikes:")
label_bikes.grid(row=12, column=1, padx=5, pady=5)

label_rentals = tkinter.Label(window, text="Rentals:")
label_rentals.grid(row=17, column=1, padx=5, pady=5)

# Define entry fields and labels for Customer
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

# Define entry fields and labels for Locations
label_location_id = tkinter.Label(window, text="Location ID:")
label_location_id.grid(row=7, column=0, padx=5, pady=5)

entry_location_id = tkinter.Entry(window)
entry_location_id.grid(row=7, column=1, padx=5, pady=5)

label_address = tkinter.Label(window, text="Address:")
label_address.grid(row=8, column=0, padx=5, pady=5)

entry_address = tkinter.Entry(window)
entry_address.grid(row=8, column=1, padx=5, pady=5)

label_city = tkinter.Label(window, text="City:")
label_city.grid(row=9, column=0, padx=5, pady=5)

entry_city = tkinter.Entry(window)
entry_city.grid(row=9, column=1, padx=5, pady=5)

label_state = tkinter.Label(window, text="State:")
label_state.grid(row=10, column=0, padx=5, pady=5)

entry_state = tkinter.Entry(window)
entry_state.grid(row=10, column=1, padx=5, pady=5)

label_zip = tkinter.Label(window, text="Zip Code:")
label_zip.grid(row=11, column=0, padx=5, pady=5)

entry_zip = tkinter.Entry(window)
entry_zip.grid(row=11, column=1, padx=5, pady=5)

# Define entry fields and labels for Bikes
label_bike_id = tkinter.Label(window, text="Bike ID:")
label_bike_id.grid(row=13, column=0, padx=5, pady=5)

entry_bike_id = tkinter.Entry(window)
entry_bike_id.grid(row=13, column=1, padx=5, pady=5)

label_model = tkinter.Label(window, text="Model:")
label_model.grid(row=14, column=0, padx=5, pady=5)

entry_model = tkinter.Entry(window)
entry_model.grid(row=14, column=1, padx=5, pady=5)

label_status_id = tkinter.Label(window, text="Status ID:")
label_status_id.grid(row=15, column=0, padx=5, pady=5)

entry_status_id = tkinter.Entry(window)
entry_status_id.grid(row=15, column=1, padx=5, pady=5)

label_last_maintenance = tkinter.Label(window, text="Last Maintenance Date:")
label_last_maintenance.grid(row=16, column=0, padx=5, pady=5)

entry_last_maintenance = tkinter.Entry(window)
entry_last_maintenance.grid(row=16, column=1, padx=5, pady=5)

# Define entry fields and labels for Rentals
label_customer_id_rental = tkinter.Label(window, text="Customer ID:")
label_customer_id_rental.grid(row=18, column=0, padx=5, pady=5)

entry_customer_id_rental = tkinter.Entry(window)
entry_customer_id_rental.grid(row=18, column=1, padx=5, pady=5)

label_bike_id_rental = tkinter.Label(window, text="Bike ID:")
label_bike_id_rental.grid(row=19, column=0, padx=5, pady=5)

entry_bike_id_rental = tkinter.Entry(window)
entry_bike_id_rental.grid(row=19, column=1, padx=5, pady=5)

label_start_date = tkinter.Label(window, text="Rental Start Date:")
label_start_date.grid(row=20, column=0, padx=5, pady=5)

entry_start_date = tkinter.Entry(window)
entry_start_date.grid(row=20, column=1, padx=5, pady=5)

label_end_date = tkinter.Label(window, text="Rental End Date:")
label_end_date.grid(row=21, column=0, padx=5, pady=5)

entry_end_date = tkinter.Entry(window)
entry_end_date.grid(row=21, column=1, padx=5, pady=5)

label_price = tkinter.Label(window, text="Price:")
label_price.grid(row=22, column=0, padx=5, pady=5)

entry_price = tkinter.Entry(window)
entry_price.grid(row=22, column=1, padx=5, pady=5)

# Define buttons for CRUD operations
button_insert_customer = tkinter.Button(window, text="Insert Customer", command=insert_customer)
button_insert_customer.grid(row=1, column=3, padx=5, pady=5)

button_update_customer = tkinter.Button(window, text="Update Customer", command=update_customer)
button_update_customer.grid(row=2, column=3, padx=5, pady=5)

button_delete_customer = tkinter.Button(window, text="Delete Customer", command=delete_customer)
button_delete_customer.grid(row=3, column=3, padx=5, pady=5)


button_insert_location = tkinter.Button(window, text="Insert Location", command=insert_location)
button_insert_location.grid(row=7, column=3, padx=5, pady=5)

button_update_location = tkinter.Button(window, text="Update Location", command=lambda: update_location)
button_update_location.grid(row=8, column=3, padx=5, pady=5)

button_delete_location = tkinter.Button(window, text="Delete Location", command=lambda: delete_location)
button_delete_location.grid(row=9, column=3, padx=5, pady=5)


button_insert_bike = tkinter.Button(window, text="Insert Bike", command=insert_bike)
button_insert_bike.grid(row=13, column=3, padx=5, pady=5)

button_insert_bike = tkinter.Button(window, text="Update Bike", command=update_bike)
button_insert_bike.grid(row=14, column=3, padx=5, pady=5)

button_delete_bike = tkinter.Button(window, text="Delete Bike", command=delete_bike)
button_delete_bike.grid(row=15, column=3, padx=5, pady=5)


button_insert_rental = tkinter.Button(window, text="Insert Rental", command=insert_rental)
button_insert_rental.grid(row=18, column=3, padx=5, pady=5)

button_insert_rental = tkinter.Button(window, text="Update Rental", command=update_rental)
button_insert_rental.grid(row=19, column=3, padx=5, pady=5)

button_delete_rental = tkinter.Button(window, text="Delete Rental", command=delete_rental)
button_delete_rental.grid(row=20, column=3, padx=5, pady=5)

# Define buttons to display results
button_display_customers = tkinter.Button(window, text="Display Customers", command=display_customers)
button_display_customers.grid(row=0, column=4, padx=5, pady=5)

button_display_locations = tkinter.Button(window, text="Display Locations", command=display_locations)
button_display_locations.grid(row=6, column=4, padx=5, pady=5)

button_display_bikes = tkinter.Button(window, text="Display Bikes", command=display_bikes)
button_display_bikes.grid(row=12, column=4, padx=5, pady=5)

button_display_rentals = tkinter.Button(window, text="Display Rentals", command=display_rentals)
button_display_rentals.grid(row=17, column=4, padx=5, pady=5)

# Define text widgets to display query results
result_text_customers = tkinter.Text(window, width=50, height=10)
result_text_customers.grid(row=1, rowspan=5, column=4, padx=5, pady=5)

result_text_locations = tkinter.Text(window, width=50, height=10)
result_text_locations.grid(row=7, rowspan=4, column=4, padx=5, pady=5)

result_text_bikes = tkinter.Text(window, width=50, height=10)
result_text_bikes.grid(row=13, rowspan=3, column=4, padx=5, pady=5)

result_text_rentals = tkinter.Text(window, width=50, height=10)
result_text_rentals.grid(row=18, rowspan=5, column=4, padx=5, pady=5)

# Define buttons for predefined SQL join queries
button_display_customers_with_bikes = tkinter.Button(window, text="Customers with Bikes", command=display_customers_with_bikes)
button_display_customers_with_bikes.grid(row=0, column=5, padx=5, pady=5)

button_display_bikes_by_popularity = tkinter.Button(window, text="Bikes by Popularity", command=display_bikes_by_popularity)
button_display_bikes_by_popularity.grid(row=12, column=5, padx=5, pady=5)

# Define text widgets to display results for predefined SQL join queries
result_text_customers_with_bikes = tkinter.Text(window, width=40, height=10)
result_text_customers_with_bikes.grid(row=1, rowspan=5, column=5, padx=5, pady=5)

result_text_bikes_by_popularity = tkinter.Text(window, width=40, height=10)
result_text_bikes_by_popularity.grid(row=13, rowspan=3, column=5, padx=5, pady=5)

# Call the function to create tables before any operations
create_tables()

# Call the functions to insert data
insert_statuses()
insert_location()
insert_customer()
insert_bike()
insert_rental()

# Define example queries
query_customers = "SELECT * FROM Customers"
query_locations = "SELECT * FROM Locations"
query_bikes = "SELECT * FROM Bikes"
query_rentals = "SELECT * FROM Rentals"

# Display query results
execute_query_and_display_result(query_customers, result_text_customers)
execute_query_and_display_result(query_customers, result_text_locations)
execute_query_and_display_result(query_bikes, result_text_bikes)
execute_query_and_display_result(query_rentals, result_text_rentals)

window.mainloop()
