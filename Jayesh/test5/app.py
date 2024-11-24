# import os
# from flask import Flask, render_template, request, redirect, url_for, flash, session
# import sqlite3
# from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime
# from werkzeug.utils import secure_filename

from flask import Flask
from config import Config
from db import create_tables
from routes.home import home_bp
from routes.auth import auth_bp
from routes.customer import customer_bp
from routes.restaurant import restaurant_bp

app = Flask(__name__)
app.config.from_object(Config)

# app.secret_key = 'supersecretkey'
# DATABASE = 'lieferspatz.db'

# Configure the uploads folder
# UPLOAD_FOLDER = 'static/images'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# def get_db_connection():
#     conn = sqlite3.connect(DATABASE)
#     conn.row_factory = sqlite3.Row
#     return conn

# def allowed_file(filename): - THIS IS CALLED BY THE util.py
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def create_tables():
#     conn = get_db_connection()

#     # Create Customers Table
#     conn.execute('''
#         CREATE TABLE IF NOT EXISTS customers (
#             CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
#             FirstName TEXT,
#             LastName TEXT,
#             Address TEXT,
#             ZipCode TEXT,
#             PhoneNumber TEXT,
#             Password TEXT,
#             Role TEXT DEFAULT 'customer',
#             Balance REAL DEFAULT 100.0,
#             CreatedAt DATETIME
#         )
#     ''')

#     # Create Restaurants Table
#     conn.execute('''
#         CREATE TABLE IF NOT EXISTS restaurants (
#             RestaurantID INTEGER PRIMARY KEY AUTOINCREMENT,
#             Name TEXT,
#             Email TEXT UNIQUE,  -- Unique email for restaurant login
#             Address TEXT,
#             ZipCode TEXT,
#             Description TEXT,
#             ImageURL TEXT, -- Store the file path instead of URL
#             Password TEXT,
#             Balance REAL DEFAULT 0.0,
#             OpenTime TIME,
#             CloseTime TIME,
#             CreatedAt DATETIME
#         )
#     ''')

#     # Create Delevery ZIP Codes Table
#     conn.execute('''
#         CREATE TABLE IF NOT EXISTS delivery_zip_codes (
#             ZipCodeID INTEGER PRIMARY KEY AUTOINCREMENT,
#             RestaurantID INTEGER,
#             ZipCode TEXT,
#             FOREIGN KEY (RestaurantID) REFERENCES restaurants(RestaurantID)
#         )
#     ''')

#     conn.commit()
#     conn.close()


create_tables()


### **Routes**

# Home Page
# @app.route('/')
# def home():
#     return render_template('home.html')
app.register_blueprint(home_bp)

app.register_blueprint(auth_bp)



# Customer Registration
# @app.route('/register/customer', methods=['GET', 'POST'])
# def register_customer():
#     if request.method == 'POST':
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         address = request.form['address']
#         zip_code = request.form['zip_code']
#         phone_number = request.form['phone_number']
#         password = generate_password_hash(request.form['password'])

#         conn = get_db_connection()
#         conn.execute('''
#             INSERT INTO customers (FirstName, LastName, Address, ZipCode, PhoneNumber, Password, CreatedAt)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         ''', (first_name, last_name, address, zip_code, phone_number, password, datetime.now()))
#         conn.commit()
#         conn.close()

#         flash('Customer registration successful!', 'success')
#         return redirect(url_for('login'))
#     return render_template('register_customer.html')
app.register_blueprint(customer_bp)



# Restaurant Registration
# @app.route('/register/restaurant', methods=['GET', 'POST'])
# def register_restaurant():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']  # Unique email for login
#         address = request.form['address']
#         zip_code = request.form['zip_code']
#         description = request.form['description']
#         image = request.files['image_url']
#         password = generate_password_hash(request.form['password'])
#         open_time = request.form['open_time']
#         close_time = request.form['close_time']
#         delivery_zip_codes = request.form.getlist('delivery_zip_codes') # Get a list of delivery zip codes

#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM restaurants WHERE Email = ?', (email,))
#         existing_restaurant = cursor.fetchone()

#         if existing_restaurant:
#             flash('Emial is already in use, please choose a different one.', 'danger')
#             conn.close()
#             return render_template('register_restaurant.html')

#         image_path = None
#         if image and allowed_file(image.filename):
#             filename = secure_filename(image.filename)
#             image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
#             image.save(image_path)

#         relative_image_path = image_path if image_path else None
        
#         # Insert new restaurant into the database only if the username is unique - USE cursor here instead of conn
#         cursor.execute('''
#             INSERT INTO restaurants (Name, Email, Address, ZipCode, Description, ImageURL, Password, OpenTime, CloseTime, CreatedAt)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         ''', (name, email, address, zip_code, description, relative_image_path, password, open_time, close_time, datetime.now()))

#         restaurant_id = cursor.lastrowid # Gets the RestaurantID of the latest created restaurant

#         for zip_code in delivery_zip_codes:
#             cursor.execute('''
#                 INSERT INTO delivery_zip_codes (RestaurantID, ZipCode)
#                 VALUES (?, ?)
#             ''', (restaurant_id, zip_code))

#         conn.commit()
#         conn.close()

#         flash('Restaurant registration successful!', 'success')
#         return redirect(url_for('login'))
#     return render_template('register_restaurant.html')
app.register_blueprint(restaurant_bp)



# Login Page - THIS IS DONE BY THE auth.py
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']  # Email or Username
#         password = request.form['password']
#         role = request.form['role']

#         conn = get_db_connection()
#         cursor = conn.cursor()

#         if role == 'customer':
#             cursor.execute('SELECT * FROM customers WHERE PhoneNumber = ?', (username,))
#         else:
#             cursor.execute('SELECT * FROM restaurants WHERE Email = ?', (username,))

#         user = cursor.fetchone()
#         conn.close()

#         if user and check_password_hash(user['Password'], password):
#             session['user_id'] = user['CustomerID'] if role == 'customer' else user['RestaurantID']
#             session['role'] = role
#             session['user'] = dict(user)
#             flash('Login successful!', 'success')
#             return redirect(url_for(f'{role}_dashboard'))
#         else:
#             flash('Invalid credentials', 'danger')

#     return render_template('login.html')


# Customer Dashboard - THIS IS CALLED BY THE customer.py
# @app.route('/customer/dashboard')
# def customer_dashboard():
#     if 'user_id' not in session or session['role'] != 'customer':
#         return redirect(url_for('login'))
#     return render_template('dashboard_customer.html', user=session['user'])


# Restaurant Dashboard - THIS IS CALLED BY THE restaurant.py
# @app.route('/restaurant/dashboard')
# def restaurant_dashboard():
#     if 'user_id' not in session or session['role'] != 'restaurant':
#         return redirect(url_for('login'))
#     return render_template('dashboard_restaurant.html', user=session['user'])


# Logout Route - THIS IS CALLED BY THE auth.py
# @app.route('/logout')
# def logout():
#     session.clear()  # Clear all session data
#     flash('You have logged out successfully!', 'success')
#     return redirect(url_for('login'))


# Prevent caching of sensitive pages (like the login page) after logout
@app.after_request
def add_cache_control(response):
    # Set cache control to prevent caching of the page
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


if __name__ == '__main__':
    app.run(debug=True)
