CREATE TABLE Customers (
    CustomerID SERIAL PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    PhoneNumber VARCHAR(20)
);

-- Create Statuses table for bike status management
CREATE TABLE Statuses (
    StatusID SERIAL PRIMARY KEY,
    StatusDescription VARCHAR(50)
);

-- Create Bikes table
CREATE TABLE Bikes (
    BikeID SERIAL PRIMARY KEY,
    Model VARCHAR(100),
    StatusID INT,
    LastMaintenanceDate DATE,
    FOREIGN KEY (StatusID) REFERENCES Statuses(StatusID)
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

CREATE INDEX idx_customer ON Rentals(CustomerID);
CREATE INDEX idx_bike ON Rentals(BikeID);

-- Create Locations table
CREATE TABLE Locations (
    LocationID SERIAL PRIMARY KEY,
    Address VARCHAR(255),
    City VARCHAR(100),
    State VARCHAR(40), 
    ZipCode VARCHAR(10) 
);
