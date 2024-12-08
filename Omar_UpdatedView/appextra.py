from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user # Gives Default Login Functions
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from sqlalchemy.sql import func # To help in Time of Creation
from os import path

# Ignore: < >
# Foreign Key -> user_ID = db.Column(db.Integer, db.ForeignKey('user.userID'))

db = SQLAlchemy()
DB_NAME = "databasetest.db" # Modify as Needed.
class User(db.Model, UserMixin):
    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    address = db.Column(db.String())
    zipcode = db.Column(db.String(20))
    phonenumber = db.Column(db.String(30))
    password = db.Column(db.String())
    role = db.Column(db.String(30))
    status = db.Column(db.String(30))
    createdAt = db.Column(db.DateTime(timezone=True), default=func.now())


#Initialising the App with DB Merge.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkeyforusprivate'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app) # Uses the URI Above

with app.app_context():
    if not path.exists('DBProject/instance/' + DB_NAME):
        db.create_all()
        print('Database Created.')

login_manager = LoginManager(app)
login_manager.login_view = 'templates/base.html'
login_manager.init_app(app)

@login_manager.user_loader 
def load_user(userID):
    return User.query.get(int(userID))

@app.route('/')
def home():
    return render_template('base.html') #Homepage

#Logging/Registering:
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        # Validate Password # Query.
        user = User.query.filter_by(phone_number = phone_number).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category='success')
                login_user(user, remember=True) # Stores Session, Counteracts Cache Misses.
                return redirect(url_for('home.html'))
            else:
                flash('Incorrect password, try again.', category='danger')   
        else:
            flash('Email does not exist.', category='danger')

    return render_template('login.html', boolean=True)

@app.route('/logout')
@login_required # Counteracts 'Protected Site'
def logout():
    logout_user() # Terminates Session
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        zip_code = request.form.get('zip_code')
        phone_number = request.form.get('phone_number')
        password1 = generate_password_hash(request.form.get('password'))
        role = request.form.get('role')
        # Check User is New.
        user = User.query.filter_by(phonenumber = phone_number).first()
        if user:
            flash('Email already exists.', category='danger')
        else:
        # Creating User:
            new_user = User(firstname=first_name, lastname=last_name, address=address, zipcode=zip_code, phonenumber=phone_number, password=password1, role=role, status='available' if role == 'Courier' else None, createdAt=datetime.now())
            db.session.add(new_user) # Add to Database
            db.session.commit() # Connection Estabilish
            flash('Registered Successfully!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('login.html'))
    return render_template('register.html', boolean=True)

# Prevent caching of protected pages
@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == "__main__":
    app.run(debug=True)