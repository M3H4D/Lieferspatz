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
    
    # Access customer session data
    customer_data = session['customer']
    return render_template('dashboard_customer.html', user=customer_data)
