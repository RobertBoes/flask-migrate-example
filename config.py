from os import environ

SQLALCHEMY_TRACK_MODIFICATIONS = False

DB_DRIVER = environ.get('DB_DRIVER', 'mysql+pymysql')
DB_USER = environ.get('DB_USER', '')
DB_PASSWORD = environ.get('DB_PASSWORD', '')
DB_HOST = environ.get('DB_HOST', '127.0.0.1')
DB_PORT = environ.get('DB_PORT', 3306)
DB_NAME = environ.get('DB_NAME', 'flask-migrate-test')
