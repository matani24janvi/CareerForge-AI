from dotenv import load_dotenv
from os import getenv

load_dotenv()

SECRET_KEY = getenv('SECRET_KEY', "159357258456")
ENV = getenv('ENV', 'development')
DEBUG = getenv('DEBUG') == 'true'

DB_TYPE = getenv('DB_TYPE','mysql')
DB_DRIVER = getenv('DB_DRIVER','pymysql')
DB_USERNAME = getenv('DB_USERNAME','root')
DB_PASSWORD = getenv('DB_PASSWORD','')
DB_HOST = getenv('DB_HOST','localhost')
DB_NAME = getenv('DB_NAME','')

class Config:
    SECRET_KEY = SECRET_KEY
    ENV = ENV
    DEBUG = DEBUG
    SQLALCHEMY_DATABASE_URI = f"{DB_TYPE}+{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False