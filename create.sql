CREATE TABLE Customers (
    CustomerID SERIAL PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100),
    PhoneNumber VARCHAR(20)
);
 
-- Create Bikes table
CREATE TABLE Bikes (
    BikeID SERIAL PRIMARY KEY,
    Model VARCHAR(100),
    Status ENUM('Available', 'Rented', 'Under Maintenance'),
    LastMaintenanceDate DATE
);
 
-- Create Rentals table
CREATE TABLE Rentals (
    RentalID SERIAL PRIMARY KEY,
    CustomerID INT,
    BikeID INT,
    RentalStartDate DATE,
    RentalEndDate DATE,
    Price DECIMAL(10, 2),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE,
    FOREIGN KEY (BikeID) REFERENCES Bikes(BikeID) ON DELETE CASCADE
);
 
-- Create Locations table
CREATE TABLE Locations (
    LocationID SERIAL PRIMARY KEY,
    Address VARCHAR(255),
    City VARCHAR(100),
    State VARCHAR(40), -- longest state name is 'Rhode Island and Providence Plantations'
    ZipCode VARCHAR(10) -- zipcodes with hyphens can have 9 digits
);