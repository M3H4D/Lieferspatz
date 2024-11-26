from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db_connection
from werkzeug.security import generate_password_hash
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from utils import allowed_file
from config import Config
import RDButil

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
    # Check if restaurant data exists in session
    if 'restaurant' not in session:
        return redirect(url_for('auth.login'))
    
    #Get items from Database and display
    conn = RDButil.connect_to_database()
    rows = RDButil.get_all_items_from_database(conn)

    # Access restaurant session data
    restaurant_data = session['restaurant']
    return render_template('dashboard_restaurant.html', user=restaurant_data, items = rows)


@restaurant_bp.route('/restaurant/additems', methods=['GET', 'POST'])
def restaurant_additems():
    conn = RDButil.connect_to_database()
    
    #Add item to database
    if request.method == 'POST':
        RDButil.add_item_to_database(conn,request.form['Name'], request.form['Price'], request.form['Description'], 0)
        flash('Item Added!', 'success')

    restaurant_data = session['restaurant']
    return render_template('add_item.html', user=restaurant_data)

@restaurant_bp.route('/delete_item', methods=['GET', 'POST'])
def restaurant_delete_item():
    conn = RDButil.connect_to_database()

    #delete item from database
    RDButil.delete_item_from_database(conn, request.form['ItemID'])
    return redirect(url_for('restaurant.restaurant_dashboard'))

@restaurant_bp.route('/edit_item_screen', methods=['GET', 'POST'])
def restaurant_edit_item_screen():
    conn = RDButil.connect_to_database()

    #Get item from database and display current values
    row = RDButil.get_item_from_database(conn, request.form['ItemID'])
    restaurant_data = session['restaurant']

    return render_template('edit_item.html', user=restaurant_data, item = row)

@restaurant_bp.route('/edit_item', methods=['GET', 'POST'])
def restaurant_edit_item():
    conn = RDButil.connect_to_database()

    #update new values to database
    if request.method == 'POST':
        RDButil.update_item_to_database(conn,request.form['Name'], request.form['Price'], request.form['Description'], 0, request.form['ItemID'])
        flash('Item Edited!', 'success')

    return redirect(url_for('restaurant.restaurant_dashboard'))