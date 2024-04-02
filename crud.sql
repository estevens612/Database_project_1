-- crud.sql

-- Create Operations

-- Add a new customer
INSERT INTO Customers (FirstName, LastName, Email, PhoneNumber) VALUES ('Alice', 'Smith', 'alicesmith@example.com', '555-6789');

-- Add a new bike
INSERT INTO Bikes (Model, Status, LastMaintenanceDate, LocationID) VALUES ('Electric 500', 'Available', '2023-03-30', 1);

-- Add a new rental
INSERT INTO Rentals (CustomerID, BikeID, RentalStartDate, RentalEndDate, Price) VALUES (3, 3, '2023-04-05', '2023-04-07', 49.99);

-- Add a new location
INSERT INTO Locations (Address, City, State, ZipCode) VALUES ('101 Cedar Rd', 'Rivertown', 'IL', '61008');

-- Read Operations

-- Get all customers
SELECT * FROM Customers;

-- Find available bikes at a specific location
SELECT * FROM Bikes WHERE Status = 'Available' AND LocationID = 1;

-- Get rental details for a specific customer
SELECT * FROM Rentals WHERE CustomerID = 1;

-- Update Operations

-- Update a customer's phone number
UPDATE Customers SET PhoneNumber = '555-9876' WHERE CustomerID = 1;

-- Change a bike's status to 'Rented'
UPDATE Bikes SET Status = 'Rented' WHERE BikeID = 1;

-- Extend a rental's end date
UPDATE Rentals SET RentalEndDate = '2023-04-09' WHERE RentalID = 1;

-- Delete Operations

-- Delete a customer
-- Ensure the CustomerID exists before running this to avoid errors.
DELETE FROM Customers WHERE CustomerID = 4;

-- Remove a bike from inventory
-- Ensure the BikeID exists before running this to avoid errors.
DELETE FROM Bikes WHERE BikeID = 4;

-- Cancel a rental
-- Ensure the RentalID exists before running this to avoid errors.
DELETE FROM Rentals WHERE RentalID = 3;
