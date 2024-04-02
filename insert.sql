-- insert.sql

-- Insert data into Locations
INSERT INTO Locations (Address, City, State, ZipCode) VALUES
('123 Pine St', 'Springfield', 'IL', '62701'), -- Edit to change data
('456 Maple Ave', 'Shelbyville', 'IL', '62565'),
('789 Oak Blvd', 'Capital City', 'IL', '60007');

-- Insert data into Customers
INSERT INTO Customers (FirstName, LastName, Email, PhoneNumber) VALUES
('John', 'Doe', 'johndoe@example.com', '555-1234'),
('Jane', 'Doe', 'janedoe@example.com', '555-5678'),
('Jim', 'Beam', 'jimbeam@example.com', '555-9012');

-- Insert data into Bikes
INSERT INTO Bikes (Model, Status, LastMaintenanceDate, LocationID) VALUES
('Mountain 1000', 'Available', '2023-03-15', 1),
('Road 550', 'Rented', '2023-03-20', 2),
('Hybrid 300', 'Under Maintenance', '2023-03-25', 3);

-- Insert data into Rentals
INSERT INTO Rentals (CustomerID, BikeID, RentalStartDate, RentalEndDate, Price) VALUES
(1, 2, '2023-04-01', '2023-04-03', 29.99),
(2, 1, '2023-04-02', '2023-04-04', 39.99);
