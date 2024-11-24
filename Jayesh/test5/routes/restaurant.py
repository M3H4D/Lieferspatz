from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db_connection
from werkzeug.security import generate_password_hash
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from utils import allowed_file
from config import Config

restaurant_bp = Blueprint('restaurant', __name__)

@restaurant_bp.route('/register/restaurant', methods=['GET', 'POST'])
def register_restaurant():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']  # Unique email for login
        address = request.form['address']
        zip_code = request.form['zip_code']
        description = request.form['description']
        image = request.files['image_url']
        password = generate_password_hash(request.form['password'])
        open_time = request.form['open_time']
        close_time = request.form['close_time']
        delivery_zip_codes = request.form.getlist('delivery_zip_codes') # Get a list of delivery zip codes

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM restaurants WHERE Email = ?', (email,))
        existing_restaurant = cursor.fetchone()

        if existing_restaurant:
            flash('Emial is already in use, please choose a different one.', 'danger')
            conn.close()
            return render_template('register_restaurant.html')

        image_path = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            image.save(image_path)

        relative_image_path = image_path if image_path else None
        
        # Insert new restaurant into the database only if the username is unique - USE cursor here instead of conn
        cursor.execute('''
            INSERT INTO restaurants (Name, Email, Address, ZipCode, Description, ImageURL, Password, OpenTime, CloseTime, CreatedAt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, email, address, zip_code, description, relative_image_path, password, open_time, close_time, datetime.now()))

        restaurant_id = cursor.lastrowid # Gets the RestaurantID of the latest created restaurant

        for zip_code in delivery_zip_codes:
            cursor.execute('''
                INSERT INTO delivery_zip_codes (RestaurantID, ZipCode)
                VALUES (?, ?)
            ''', (restaurant_id, zip_code))

        conn.commit()
        conn.close()

        flash('Restaurant registration successful!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register_restaurant.html')

@restaurant_bp.route('/restaurant/dashboard')
def restaurant_dashboard():
    if 'user_id' not in session or session['role'] != 'restaurant':
        return redirect(url_for('auth.login'))
    return render_template('dashboard_restaurant.html', user=session['user'])