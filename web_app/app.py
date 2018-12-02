from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from .config import Dev, Prod
from .utils import create_mediafiles_folder

create_mediafiles_folder()
app = Flask(__name__)
app.config.from_object(Dev) #TODO change for Prod
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from . import auth
from . import resources
from . import views
