import os

MAX_PRODUCTS = 10
MAX_STORED_MEDIA_FILES = 3
BASE_MEDIA_DIR = '/home/hacknoob/Desktop/media/items'

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    UPLOAD_FOLDER = BASE_MEDIA_DIR

class Dev(Config):
    SQLALCHEMY_DATABASE_URI = postgres_local_base = "postgresql://postgres:mysecretpassword@localhost/cime"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Prod(Config):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
