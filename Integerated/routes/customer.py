from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db_connection
from werkzeug.security import generate_password_hash
from datetime import datetime

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/register/customer', methods=['GET', 'POST'])
def register_customer():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        zip_code = request.form['zip_code']
        phone_number = request.form['phone_number']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()

        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM customers WHERE PhoneNumber = ?', (phone_number,))
        existing_customer = cursor.fetchone()

        if existing_customer:
            flash('Phone Number is already in use, please choose a different one.', 'danger')
            conn.close()
            return render_template('register_customer.html')
        
        cursor.execute('''
            INSERT INTO customers (FirstName, LastName, Address, ZipCode, PhoneNumber, Password, CreatedAt)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, address, zip_code, phone_number, password, datetime.now()))
        conn.commit()
        conn.close()

        flash('Customer registration successful!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register_customer.html')

@customer_bp.route('/customer/dashboard')
def customer_dashboard():
    # Check if customer data exists in session
    if 'customer' not in session:
        return redirect(url_for('auth.login'))
    
    # Get user details (if needed)
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customers WHERE CustomerID = ?', (user_id,))
    user = cursor.fetchone()

    # Access customer session data
    customer_data = session['customer']
        
    # Newly Added Part! By Omar.
    cursor.execute('SELECT * FROM restaurants WHERE RestaurantID IN (SELECT RestaurantID FROM delivery_zip_codes WHERE ZipCode = ?)', (user['ZipCode'],))
    restaurantsclose = cursor.fetchall()
    conn.close()
    return render_template('dashboard_customer.html', user=customer_data, restaurantsclose=restaurantsclose)

@customer_bp.route('/customer/itemorder', methods=['GET', 'POST'])
def itemorder():
    customer_data = session['customer']

    if request.method == 'POST':
        user_id = session['user_id']
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM customers WHERE CustomerID = ?', (user_id,))
        user = cursor.fetchone()
        chosenID = request.form['selectedID'] # Receiving the ID From Clicking Restaurant Image/Alt.
        cursor.execute('SELECT * FROM restaurants WHERE RestaurantID = ?', (chosenID,))
        restaurantchosen = cursor.fetchone()

        cursor.execute('SELECT * FROM Items WHERE RestaurantID = ?', (chosenID,))
        itemschosen = cursor.fetchall()

        conn.close()
    return render_template('itemorder.html', user=customer_data, itemschosen=itemschosen, restaurantchosen=restaurantchosen)
# End of New Route

