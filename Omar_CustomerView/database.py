import sqlite3

DATABASE = 'testing.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn    
def create_table():
    conn = get_db_connection()
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT,
            LastName TEXT,
            Address TEXT,
            ZipCode TEXT,
            PhoneNumber TEXT,
            Password TEXT,
            Role TEXT,
            Status TEXT,
            Balance REAL DEFAULT 100.0,
            CreatedAt DATETIME
        ) ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            RestaurantID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name	TEXT,
            Email	TEXT,
            Address	TEXT,
            ZipCode	TEXT,
            Password TEXT,
            Balance	REAL DEFAULT 0.0,
            Description	TEXT,
            OpeningTime	TIME,
            ClosingTime	TIME,
            ImageURL	TEXT,
            CreatedAt	DATETIME
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS items (
        ItemID	INTEGER,
        RestaurantID INTEGER,
        Name	TEXT,
        Price	REAL,
        Description	TEXT,
        ImageURL	TEXT,
        CreatedAt	DATETIME,
        PRIMARY KEY("ItemID" AUTOINCREMENT),
        FOREIGN KEY("RestaurantID") REFERENCES "restaurants"("RestaurantID")
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS zipcodes (
        ZipCodeID INTEGER,
        RestaurantID INTEGER,
        ZipCode	INTEGER,
        PRIMARY KEY("ZipCodeID" AUTOINCREMENT),
        FOREIGN KEY("RestaurantID") REFERENCES "restaurants"("RestaurantID")
        )
    ''')
    # Adding DB Records Invidiually!
    conn.execute("INSERT OR REPLACE INTO users (UserID, FirstName, LastName, Address, ZipCode, Password, Balance, PhoneNumber, CreatedAt) VALUES ('1', 'Josi', 'Kim', 'Dinslaker Straße 20', '47169', '4675', '100', '1778080312', '2024-02-07 17:24:21');")
    conn.execute("INSERT OR REPLACE INTO users (UserID, FirstName, LastName, Address, ZipCode, Password, Balance, PhoneNumber, CreatedAt) VALUES ('2', 'Solomon', 'Carson', 'Auf dem Damm 17', '47229', '7125', '100', '1778532638', '2024-01-08 10:21:48');")
    conn.execute("INSERT OR REPLACE INTO users (UserID, FirstName, LastName, Address, ZipCode, Password, Balance, PhoneNumber, CreatedAt) VALUES ('3', 'David', 'Bell', 'Kammerstraße 4', '47057', '6558', '100', '1777608050', '2024-04-07 18:54:05');")
    conn.execute("INSERT OR REPLACE INTO users (UserID, FirstName, LastName, Address, ZipCode, Password, Balance, PhoneNumber, CreatedAt) VALUES ('4', 'Heather', 'Watt', 'Kaßlerfelder Straße 45', '47059', '4663', '100', '1772407992', '2024-02-20 12:26:07');")
    conn.execute("INSERT OR REPLACE INTO users (UserID, FirstName, LastName, Address, ZipCode, Password, Balance, PhoneNumber, CreatedAt) VALUES ('5', 'Tim', 'Wayne', 'Ruhrorter Straße 70', '47059', '6786', '100', '1773720093', '2024-02-07 10:29:18');")
    conn.execute("INSERT OR REPLACE INTO users (UserID, FirstName, LastName, Address, ZipCode, Password, Balance, PhoneNumber, CreatedAt) VALUES ('6', 'Peter', 'Park', 'Lotharstraße 6', '47057', '6520', '100', '1770837657', '2024-04-02 14:02:11');")
    conn.execute("INSERT OR REPLACE INTO users (UserID, FirstName, LastName, Address, ZipCode, Password, Balance, PhoneNumber, CreatedAt) VALUES ('7', 'Joe', 'Mame', 'Bismarckstraße 10', '47229', '7454', '100', '1773259565', '2024-10-09 10:55:50');")
    conn.execute("INSERT OR REPLACE INTO users (UserID, FirstName, LastName, Address, ZipCode, Password, Balance, PhoneNumber, CreatedAt) VALUES ('8', 'John', 'Doe', 'Brehmsweg 8', '47057', '5030', '100', '1770807364', '2024-07-11 17:50:25');")
    conn.execute("INSERT OR REPLACE INTO users (UserID, FirstName, LastName, Address, ZipCode, Password, Balance, PhoneNumber, CreatedAt) VALUES ('9', 'Ezra', 'Wu', 'Auf dem Werth 7', '47058', '1586', '100', '1776532311', '2024-01-02 17:48:23');")
    conn.execute("INSERT OR REPLACE INTO users (UserID, FirstName, LastName, Address, ZipCode, Password, Balance, PhoneNumber, CreatedAt) VALUES ('10', 'Abid', 'Gafoor', 'Dachsstraße 34', '47055', '3979', '100', '1779164498', '2024-11-06 08:25:00');")

    conn.execute("INSERT OR REPLACE INTO restaurants (RestaurantID, Name, Email, Address, ZipCode, Password, Balance, Description, OpeningTime, ClosingTime, ImageURL, CreatedAt) VALUES ('1', 'AnandHub', 'AnandHub@gmail.com', 'Kammerstraße 20', '47057', '9223', '0', 'Noodles I guess?', '10:00:00', '20:00:00', 'images/Image1.jpg', '2024-07-06 19:05:35');")
    conn.execute("INSERT OR REPLACE INTO restaurants (RestaurantID, Name, Email, Address, ZipCode, Password, Balance, Description, OpeningTime, ClosingTime, ImageURL, CreatedAt) VALUES ('2', 'Ichiraku Sushi', 'Ichirakusushi@gmail.com', 'Dachsstraße 33', '47055', '260', '0', 'Sushi brooo', '08:00:00', '18:00:00', 'images/Image2.jpg', '2024-11-25 09:37:35');")
    conn.execute("INSERT OR REPLACE INTO restaurants (RestaurantID, Name, Email, Address, ZipCode, Password, Balance, Description, OpeningTime, ClosingTime, ImageURL, CreatedAt) VALUES ('3', 'Sharma Palace', 'Sharmapalace@gmail.com', 'Bismarckstraße 56', '47229', '2998', '0', 'Indian food ', '08:00:00', '18:00:00', 'images/Image6.jpg', '2024-01-05 11:31:13');")
    conn.execute("INSERT OR REPLACE INTO restaurants (RestaurantID, Name, Email, Address, ZipCode, Password, Balance, Description, OpeningTime, ClosingTime, ImageURL, CreatedAt) VALUES ('4', 'Zaatar Darwish', 'ZaatarDarwish@gmail.com', 'Dinslaker Straße 40', '47169', '5758', '0', 'Manakish of all flavours', '08:00:00', '18:00:00', 'images/Image5.jpg', '2024-01-19 08:43:14');")
    conn.execute("INSERT OR REPLACE INTO restaurants (RestaurantID, Name, Email, Address, ZipCode, Password, Balance, Description, OpeningTime, ClosingTime, ImageURL, CreatedAt) VALUES ('5', 'Shakir de Samosay', 'ShakirdeSamosay@gmail.com', 'Kaßlerfelder Straße 66', '47059', '9783', '0', 'I have best Samoae', '08:00:00', '19:30:00', 'images/Image4.jpg', '2024-02-23 18:12:05');")
    #with open('images\Image1.jpg', 'rb') as file:
    #image_data = file.read()
    #cursor.execute("INSERT OR REPLACE INTO restaurants (ImageURL) VALUES (?)", (image_data,))

    conn.execute("INSERT OR REPLACE INTO items (ItemID, RestaurantID, Name, Price, Description, ImageURL, CreatedAt) VALUES ('1', '5', 'Potato Samosa', '2', 'Per piece', '', '2024-11-04 13:06:01');")
    conn.execute("INSERT OR REPLACE INTO items (ItemID, RestaurantID, Name, Price, Description, ImageURL, CreatedAt) VALUES ('2', '5', 'Chicken Samosa', '2.5', 'Per piece', '', '2024-12-27 08:53:58');")
    conn.execute("INSERT OR REPLACE INTO items (ItemID, RestaurantID, Name, Price, Description, ImageURL, CreatedAt) VALUES ('3', '1', 'Spicy Fried Noodles', '10', 'Very lecker!', '', '2024-02-06 15:21:17');")
    conn.execute("INSERT OR REPLACE INTO items (ItemID, RestaurantID, Name, Price, Description, ImageURL, CreatedAt) VALUES ('4', '1', 'Soupy sour Noodles', '7', 'Good for health', '', '2024-06-21 12:05:23');")
    conn.execute("INSERT OR REPLACE INTO items (ItemID, RestaurantID, Name, Price, Description, ImageURL, CreatedAt) VALUES ('5', '2', 'Fish Sushi', '6', '6 sushis in pack', '', '2024-08-10 12:36:04');")
    conn.execute("INSERT OR REPLACE INTO items (ItemID, RestaurantID, Name, Price, Description, ImageURL, CreatedAt) VALUES ('6', '2', 'Cucumber Sushi', '4', '6 sushis in pack', '', '2024-04-06 17:41:33');")
    conn.execute("INSERT OR REPLACE INTO items (ItemID, RestaurantID, Name, Price, Description, ImageURL, CreatedAt) VALUES ('7', '3', 'Daal', '10', 'Very boring but comes with rice', '', '2024-07-21 14:50:22');")
    conn.execute("INSERT OR REPLACE INTO items (ItemID, RestaurantID, Name, Price, Description, ImageURL, CreatedAt) VALUES ('8', '3', 'Paneer', '15', 'Mid food comes with Naan', '', '2024-09-09 10:48:35');")
    conn.execute("INSERT OR REPLACE INTO items (ItemID, RestaurantID, Name, Price, Description, ImageURL, CreatedAt) VALUES ('9', '4', 'Zaatar Manakish', '3', 'Best snack', '', '2024-11-26 10:54:06');")
    conn.execute("INSERT OR REPLACE INTO items (ItemID, RestaurantID, Name, Price, Description, ImageURL, CreatedAt) VALUES ('10', '4', 'Cheese Manakish', '2', '2nd best snack', '', '2024-09-21 15:04:53');")
    
    conn.execute("INSERT OR REPLACE INTO zipcodes (ZipCodeID, RestaurantID, ZipCode) VALUES ('1', '1', '47057');")
    conn.execute("INSERT OR REPLACE INTO zipcodes (ZipCodeID, RestaurantID, ZipCode) VALUES ('2', '1', '47058');")
    conn.execute("INSERT OR REPLACE INTO zipcodes (ZipCodeID, RestaurantID, ZipCode) VALUES ('3', '1', '47059');")
    conn.execute("INSERT OR REPLACE INTO zipcodes (ZipCodeID, RestaurantID, ZipCode) VALUES ('4', '2', '47055');")
    conn.execute("INSERT OR REPLACE INTO zipcodes (ZipCodeID, RestaurantID, ZipCode) VALUES ('5', '2', '47056');")
    conn.execute("INSERT OR REPLACE INTO zipcodes (ZipCodeID, RestaurantID, ZipCode) VALUES ('6', '2', '47057');")
    conn.execute("INSERT OR REPLACE INTO zipcodes (ZipCodeID, RestaurantID, ZipCode) VALUES ('7', '2', '47058');")
    conn.execute("INSERT OR REPLACE INTO zipcodes (ZipCodeID, RestaurantID, ZipCode) VALUES ('8', '2', '47059');")
    conn.execute("INSERT OR REPLACE INTO zipcodes (ZipCodeID, RestaurantID, ZipCode) VALUES ('9', '3', '47229');")
    conn.execute("INSERT OR REPLACE INTO zipcodes (ZipCodeID, RestaurantID, ZipCode) VALUES ('10', '3', '47228');")
    conn.execute("INSERT OR REPLACE INTO zipcodes (ZipCodeID, RestaurantID, ZipCode) VALUES ('11', '3', '47227');")
    conn.execute("INSERT OR REPLACE INTO zipcodes (ZipCodeID, RestaurantID, ZipCode) VALUES ('12', '4', '47169');")
    conn.execute("INSERT OR REPLACE INTO zipcodes (ZipCodeID, RestaurantID, ZipCode) VALUES ('13', '4', '47170');")
    conn.execute("INSERT OR REPLACE INTO zipcodes (ZipCodeID, RestaurantID, ZipCode) VALUES ('14', '4', '47168');")
    conn.execute("INSERT OR REPLACE INTO zipcodes (ZipCodeID, RestaurantID, ZipCode) VALUES ('15', '5', '47057');")
    conn.execute("INSERT OR REPLACE INTO zipcodes (ZipCodeID, RestaurantID, ZipCode) VALUES ('16', '5', '47058');")
    conn.execute("INSERT OR REPLACE INTO zipcodes (ZipCodeID, RestaurantID, ZipCode) VALUES ('17', '5', '47059');")
 
    conn.commit()
    conn.close()
