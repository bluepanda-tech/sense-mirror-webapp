from flask_restful import Resource
from .app import api
from .models import Product

class HelloWorld(Resource):
    def get(self):
        return {'class': 'user',
        'first': 'john',
        'last': 'doe',
        }
api.add_resource(HelloWorld, '/')
