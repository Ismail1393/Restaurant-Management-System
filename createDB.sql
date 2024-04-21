USE dbmsproject;

CREATE TABLE users (
    userID INT AUTO_INCREMENT,
    fname VARCHAR(255),
    lname VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    wage DECIMAL(10,2),
    permission_level INT,
    PRIMARY KEY (userID)
);

CREATE TABLE Menu (
    ItemID INT AUTO_INCREMENT,
    ItemName VARCHAR(255),
    ItemDescription VARCHAR(255),
    ItemPrice DECIMAL(10,2),
    Available BOOLEAN,
    PRIMARY KEY (ItemID )
);

CREATE TABLE Orders (
    OrderID INT AUTO_INCREMENT,
    OrderDate DATE,
    TotalPrice DECIMAL(10,2),
    EmployeeID INT,
    Quantity INT,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (EmployeeID) REFERENCES users(userID)
);

CREATE TABLE Reservations (
    ReservationID INT AUTO_INCREMENT,
    Available BOOLEAN,
    PRIMARY KEY (ReservationID)
);

CREATE TABLE Inventory (
    InventoryID INT AUTO_INCREMENT,
    ItemName VARCHAR(255),
    Quantity INT,
    PRIMARY KEY (InventoryID),
    FOREIGN KEY (InventoryID) REFERENCES Menu(ItemID)
);

CREATE TABLE Payments (
    PaymentID INT AUTO_INCREMENT,
    PaymentDate DATE,
    PaymentAmount DECIMAL(10,2),
    OrderID INT,
    PRIMARY KEY (PaymentID),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

-- Inserting data into the tables

INSERT INTO users (fname, lname, email, password, wage, permission_level)
VALUES
('John', 'Doe', 'johndoe@example.com', 'password123', 25000.00, 2),
('Jane', 'Smith', 'janesmith@example.com', 'password123', 30000.00, 0),
('Alice', 'Johnson', 'alicejohnson@example.com', 'password123', 35000.00, 1),
('Bob', 'Brown', 'bobbrown@example.com', 'password123', 28000.00, 2);


INSERT INTO Menu (ItemName, ItemDescription, ItemPrice, Available)
VALUES
('Cheese Pizza', 'Classic cheese pizza with a rich tomato base', 9.99, TRUE),
('Veggie Burger', 'A plant-based burger loaded with vegetables', 8.99, TRUE),
('Chicken Salad', 'Grilled chicken salad with a variety of greens', 7.99, FALSE),
('Ice Cream', 'Vanilla ice cream with chocolate syrup', 4.99, TRUE);

INSERT INTO Orders (OrderDate, TotalPrice)
VALUES
('2023-04-01', 45.97),
('2023-04-02', 19.98),
('2023-04-03', 34.95),
('2023-04-04', 24.96);


INSERT INTO Reservations (Available)
VALUES
(TRUE),
(FALSE),
(TRUE),
(TRUE);

INSERT INTO Inventory (ItemName, Quantity)
VALUES
('Cheese Pizza', 150),
('Veggie Burger', 120),
('Chicken Salad', 100),
('Ice Cream', 50);

INSERT INTO Payments (PaymentDate, PaymentAmount, OrderID)
VALUES
('2023-04-01', 45.97, 1),
('2023-04-02', 19.98, 2),
('2023-04-03', 34.95, 3),
('2023-04-04', 24.96, 4);
