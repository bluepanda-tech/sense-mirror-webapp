from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .config import Dev, Prod, create_mediafiles_folder

create_mediafiles_folder()
app = Flask(__name__)
app.config.from_object(Dev) #TODO change for Prod
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import resources
