import os

class Config:
    SECRET_KEY = 'supersecretkey'
    DATABASE = 'lieferspatz.db'
    UPLOAD_FOLDER = 'static/images'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}