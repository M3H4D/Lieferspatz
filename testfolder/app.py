from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from os import path

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a secure key in production

DATABASE = 'testing.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db_connection()
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
        )
    ''')
    conn.commit()
    conn.close()

with app.app_context():
    if not path.exists('DBProject/instance/' + DATABASE):
        create_table()


### **Step 2: Define Routes for Registration and Login**

# Home Page
@app.route('/')
def home():
    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE UserID = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()

    return render_template('base.html', user=user)



# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        zip_code = request.form['zip_code']
        phone_number = request.form['phone_number']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO users (FirstName, LastName, Address, ZipCode, PhoneNumber, Password, Role, Status, CreatedAt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, address, zip_code, phone_number, password, role, 'available' if role == 'courier' else None, datetime.now()))
        conn.commit()
        conn.close()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    user = None  # Default value for user

    if request.method == 'POST':
        phone_number = request.form['phone_number']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE PhoneNumber = ?', (phone_number,))
        user = cursor.fetchone()  # Fetch user data from database
        conn.close()

        if user and check_password_hash(user['Password'], password):
            session['user_id'] = user['UserID']
            session['role'] = user['Role']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to home or another page
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html', user=user)  # Pass user to template


# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Protected route that requires login
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for('login'))
    
    # Get user details (if needed)
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE UserID = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    return render_template('dashboard.html', user=user)

# Prevent caching of protected pages
@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
    
if __name__ == '__main__':
    app.run(debug=True)
