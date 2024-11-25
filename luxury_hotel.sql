CREATE DATABASE LuxuryHotel;

USE LuxuryHotel;



CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,  -- Store hashed passwords, not plain text
    Role VARCHAR(50) NOT NULL,  -- Role like Admin, Staff, etc.
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE Guests (
    GuestID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    PhoneNumber VARCHAR(15) UNIQUE,
    Email VARCHAR(100) UNIQUE,
    Address TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE Rooms (
    RoomID INT AUTO_INCREMENT PRIMARY KEY,
    RoomNumber VARCHAR(10) UNIQUE,
    RoomType VARCHAR(50),
    PricePerNight DECIMAL(10, 2),
    IsAvailable BOOLEAN DEFAULT TRUE
);


CREATE TABLE Bookings (
    BookingID INT AUTO_INCREMENT PRIMARY KEY,
    GuestID INT,
    RoomID INT,
    CheckInDate DATE,
    CheckOutDate DATE,
    TotalAmount DECIMAL(10, 2),
    BookingDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (GuestID) REFERENCES Guests(GuestID),
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID)
);


CREATE TABLE Payments (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    BookingID INT,
    AmountPaid DECIMAL(10, 2),
    PaymentMethod VARCHAR(50),
    PaymentDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (BookingID) REFERENCES Bookings(BookingID)
);


CREATE TABLE Staff (
    StaffID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Role VARCHAR(50),
    PhoneNumber VARCHAR(15) UNIQUE,
    Email VARCHAR(100) UNIQUE,
    Salary DECIMAL(10, 2),
    HireDate DATE
);


CREATE TABLE Services (
    ServiceID INT AUTO_INCREMENT PRIMARY KEY,
    BookingID INT,
    ServiceDescription TEXT,
    ServiceCost DECIMAL(10, 2),
    ServiceDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (BookingID) REFERENCES Bookings(BookingID)
);


CREATE TABLE Feedback (
    FeedbackID INT AUTO_INCREMENT PRIMARY KEY,
    GuestID INT,
    FeedbackText TEXT,
    Rating INT CHECK (Rating BETWEEN 1 AND 5),
    SubmittedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (GuestID) REFERENCES Guests(GuestID)
);
