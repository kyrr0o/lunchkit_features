CREATE DATABASE IF NOT EXISTS `lunchkit_database`;
use lunchkit_database;

CREATE TABLE IF NOT EXISTS Users (
    google_id VARCHAR(30) PRIMARY KEY NOT NULL,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    CONSTRAINT valid_email CHECK (email LIKE '%@g.msuiit.edu.ph'),
	Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	Updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);



CREATE TABLE IF NOT EXISTS sessions (
   id VARCHAR(255) PRIMARY KEY,
   user_data TEXT,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   expires_at TIMESTAMP NOT NULL,
   ip_address VARCHAR(45),
   user_agent TEXT
);


CREATE TABLE IF NOT EXISTS StoreOwners (
	StoreOwnerId INT AUTO_INCREMENT PRIMARY KEY,
    OwnerName VARCHAR(25) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Mobile_Num VARCHAR(11) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Application_Status VARCHAR(50) NOT NULL,  -- Defualt | Processing | Completed
    Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS StoreApplications (
	StoreApplicationId VARCHAR(7) PRIMARY KEY NOT NULL,
    StoreOwnerId INT NOT NULL,
    StoreName VARCHAR(100) NOT NULL,
    ApplicationStatus VARCHAR(50) NOT NULL, -- Approved | Pending | Rejected
    SubmissionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ReviewDate TIMESTAMP,
    FOREIGN KEY (StoreOwnerId) REFERENCES StoreOwners (StoreOwnerId)
);


CREATE TABLE IF NOT EXISTS ApplicationDocuments (
	ApplicationDocumentsId INT AUTO_INCREMENT PRIMARY KEY,
    StoreApplicationId VARCHAR(7) NOT NULL,
    SanitaryPermit VARCHAR(255) NOT NULL,
    CertificateOfBusinessNameRegistration VARCHAR(255) NOT NULL,
    BusinessPermit VARCHAR(255) NOT NULL,
    FireSafetyInspectionCertificate VARCHAR(255) NOT NULL,
    CertificateOfRegistration VARCHAR(255) NOT NULL,
    TaxPaymentForm VARCHAR(255) NOT NULL,
	FOREIGN KEY (StoreApplicationId) REFERENCES StoreApplications (StoreApplicationId)
);

CREATE TABLE IF NOT EXISTS Store(
	StoreId INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    StoreName VARCHAR(100) NOT NULL,
    StoreDescription TEXT,
    StorePhoto VARCHAR(100),
	StoreApplicationId VARCHAR(7),
	StoreOwnerId INT NOT NULL,
    FOREIGN KEY (StoreApplicationId) REFERENCES StoreApplications (StoreApplicationId),
    FOREIGN KEY (StoreOwnerId) REFERENCES StoreOwners (StoreOwnerId)
);

CREATE TABLE IF NOT EXISTS Items(
	ItemId INT AUTO_INCREMENT PRIMARY KEY,
    ItemName VARCHAR(55) NOT NULL,
    ItemDescription TEXT NOT NULL,
    ItemPrice INT,
    ItemPhoto VARCHAR(255),
    StoreId INT,
    FOREIGN KEY (StoreId) REFERENCES Store(StoreId)
);

CREATE TABLE IF NOT EXISTS Admins(
    AdminId INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(255)
)
