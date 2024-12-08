import sqlite3
from config import Config

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()

    # Create Customers Table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT,
            LastName TEXT,
            Address TEXT,
            ZipCode TEXT,
            PhoneNumber TEXT UNIQUE,
            Password TEXT,
            Role TEXT DEFAULT 'customer',
            Balance REAL DEFAULT 100.0,
            CreatedAt DATETIME
        )
    ''')

    # Create Restaurants Table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            RestaurantID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Email TEXT UNIQUE,  -- Unique email for restaurant login
            Address TEXT,
            ZipCode TEXT,
            Description TEXT,
            ImageURL TEXT, -- Store the file path instead of URL
            Password TEXT,
            Balance REAL DEFAULT 0.0,
            OpenTime TIME,
            CloseTime TIME,
            CreatedAt DATETIME
        )
    ''')

    # Create Delevery ZIP Codes Table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS delivery_zip_codes (
            ZipCodeID INTEGER PRIMARY KEY AUTOINCREMENT,
            RestaurantID INTEGER,
            ZipCode TEXT,
            FOREIGN KEY (RestaurantID) REFERENCES restaurants(RestaurantID)
        )
    ''')

    # Create Items Table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Items(
            ItemID INTEGER PRIMARY KEY AUTOINCREMENT,
            RestaurantID INTEGER,
            Name TEXT,
            Price INTEGER,
            Description TEXT,
            ImageURL TEXT,
            CreatedAt DATETIME,
            FOREIGN KEY (RestaurantID) REFERENCES restaurants(RestaurantID)
        )
    ''')

    # Create OrderItems Table
    conn.execute('''
            CREATE TABLE IF NOT EXISTS OrderItems (
                OrderID INTEGER,
                ItemID INTEGER FORIEGN KEY,
                Quantity INTEGER,
                Price REAL
            )
        ''')


    conn.commit()
    conn.close()