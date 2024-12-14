import sqlite3
from datetime import datetime
from flask import session

def connect_to_database():
    conn = sqlite3.connect('lieferspatz.db',isolation_level=None)
    return conn
    
def add_item_to_database(conn,Name, Price, Description, ImageURL):
    conn.execute('''
            INSERT INTO Items (Name,
                    RestaurantID,
                    Price,
                    Description,
                    ImageURL,
                    CreatedAt)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (Name, session['user_id'], Price, Description,ImageURL, datetime.now()))
    conn.commit()
    conn.close()

def update_item_to_database(conn,Name, Price, Description, ImageURL,ItemID):
    print(ItemID)
    conn.execute('''
            UPDATE Items 
            Set Name = ?, Price = ?,Description = ?, ImageURL = ?
            WHERE ItemID = ?
        ''', (Name, Price, Description,ImageURL, ItemID))
    conn.commit()
    conn.close()


def get_all_items_from_database(conn):
    cursor  = conn.cursor()

    cursor.execute("SELECT ItemID, Name, Price, Description, CreatedAt FROM Items WHERE RestaurantID = ?", (session['user_id'],))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_item_from_database(conn, ItemID):
    cursor  = conn.cursor()
    cursor.execute("SELECT ItemID, Name, Price, Description, CreatedAt FROM Items WHERE ItemID = ?", ItemID)
    row = cursor.fetchall()
    conn.close()
    return row

def delete_item_from_database(conn, ItemID):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Items WHERE ItemID = ?", ItemID)

def get_all_orders_from_database(conn):
    cursor  = conn.cursor()

    cursor.execute("SELECT * FROM Orders WHERE RestaurantID = ?", (session['user_id'],))
    rows = cursor.fetchall()
    return rows

def get_customer(conn, CustomerID):
    cursor  = conn.cursor()
    cursor.execute("SELECT FirstName, LastName FROM Customers WHERE CustomerID = ?", (CustomerID,))
    rows = cursor.fetchall()
    return rows