import os

SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL',
    'postgresql://myuser:mypassword@localhost:5432/mydatabase'
)
SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
SQLALCHEMY_TRACK_MODIFICATIONS = False

