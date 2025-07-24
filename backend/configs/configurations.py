import os

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///database.db')
SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
SQLALCHEMY_TRACK_MODIFICATIONS = False

