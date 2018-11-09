import os

MAX_PRODUCTS = 10
MAX_STORED_MEDIA_FILES = 3
BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
BASE_MEDIA_DIR = os.path.join(BASEDIR, 'media')
ALLOWED_FILE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'mp4'])

class Config:
    """Base configuration"""
    DEBUG = False

class Dev(Config):
    """Configuration to be used in Dev environments"""
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:mysecretpassword@localhost/cime"
    SECRET_KEY = 'S@MpLe9SeCrEt#KeY'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Prod(Config):
    """Configuration to be used in production"""
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:' #TODO os.environ['DATABASE_URL']

class Test(Dev):
    """Configuration to be used in testing environments"""
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True
