-- script crear tablas y cargar .csv
-- crear base de datos

CREATE DATABASE IF NOT EXISTS sales_company DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sales_company;

-- crear tablas
-- tabla countries
CREATE TABLE IF NOT EXISTS countries (
	CountryID INT PRIMARY KEY,
    CountryName VARCHAR(45),
    CountryCode VARCHAR(2)
);

-- tabla cities
CREATE TABLE IF NOT EXISTS cities (
    CityID INT PRIMARY KEY,
    CityName VARCHAR(45),
    zipcode DECIMAL(5,0),
    CountryID INT,
    FOREIGN KEY (CountryID) REFERENCES countries(CountryID)
);

-- tabla categories
CREATE TABLE IF NOT EXISTS categories (
    CategoryID INT PRIMARY KEY,
    CategoryName VARCHAR(45)
);

-- tabla products
CREATE TABLE IF NOT EXISTS products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(45),
    Price DECIMAL(10,4),
    CategoryID INT,
    Class VARCHAR(45),
    ModifyDate TIME,
    Resistant VARCHAR(45),
    IsAllergic VARCHAR(10),
    VitalityDays DECIMAL(3,0),
    FOREIGN KEY (CategoryID) REFERENCES categories(CategoryID)
);

-- tabla employees
CREATE TABLE IF NOT EXISTS employees (
    EmployeeID INT PRIMARY KEY,
    Firstname VARCHAR(45),
    MiddleInitial VARCHAR(1),
    LastName VARCHAR(45),
    BirthDate DATE,
    Gender VARCHAR(1),
    CityID INT,
    HireDate DATETIME,
    FOREIGN KEY (CityID) REFERENCES cities(CityID)
);

-- table customers
CREATE TABLE IF NOT EXISTS customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(45),
    MiddleInitial VARCHAR(1),
    LastName VARCHAR(45),
    CityID INT,
    Address VARCHAR(90),
    FOREIGN KEY (CityID) REFERENCES cities(CityID)
);

-- tabla sales
CREATE TABLE IF NOT EXISTS sales (
    SalesID INT PRIMARY KEY,
    SalesPersonID INT,
    CustomerID INT,
    ProductID INT,
    Quantity INT,
    Discount DECIMAL(10,2),
    TotalPrice DECIMAL(10,2),
    SalesDate TIME,
    TransactionNumber VARCHAR(20),
    FOREIGN KEY (SalesPersonID) REFERENCES employees(EmployeeID),
    FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);

-- activar la propiedad local infile para cargar archivos
SET GLOBAL local_infile = 1;
SHOW GLOBAL VARIABLES LIKE 'local_infile';
-- cargar datos desde los .csv

LOAD DATA LOCAL INFILE 'C:/Users/veron/OneDrive/Documentos/curso Henry/Proyecto-Final/data/countries.csv'
INTO TABLE countries
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE 'C:/Users/veron/OneDrive/Documentos/curso Henry/Proyecto-Final/data/categories.csv'
INTO TABLE categories
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE 'C:/Users/veron/OneDrive/Documentos/curso Henry/Proyecto-Final/data/cities.csv'
INTO TABLE cities
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE 'C:/Users/veron/OneDrive/Documentos/curso Henry/Proyecto-Final/data/customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE 'C:/Users/veron/OneDrive/Documentos/curso Henry/Proyecto-Final/data/employees.csv'
INTO TABLE employees
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE 'C:/Users/veron/OneDrive/Documentos/curso Henry/Proyecto-Final/data/products.csv'
INTO TABLE products
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE 'C:/Users/veron/OneDrive/Documentos/curso Henry/Proyecto-Final/data/sales.csv'
INTO TABLE sales
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
