import os

MAX_PRODUCTS = 10
MAX_STORED_MEDIA_FILES = 3
BASE_MEDIA_DIR = '/home/hacknoob/Desktop/media/items'
ALLOWED_FILE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'mp4'])

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False

class Dev(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:mysecretpassword@localhost/cime"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Prod(Config):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class Test(Dev):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True
