import os

MAX_PRODUCTS = 10
MAX_STORED_MEDIA_FILES = 3
BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
BASE_MEDIA_DIR = os.path.join(BASEDIR, 'media')
ALLOWED_FILE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'mp4'])

def create_mediafiles_folder():
    """Creates folder where media will be stored if not exists"""
    if not os.path.exists(BASE_MEDIA_DIR):
        os.makedirs(BASE_MEDIA_DIR)

class Config:
    DEBUG = False

class Dev(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:mysecretpassword@localhost/cime"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Prod(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:' #TODO os.environ['DATABASE_URL']

class Test(Dev):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True
