import uuid
import os
from flask import request
from werkzeug.utils import secure_filename
from flask_restful import Resource
from .app import app, api, db
from .models import Product, MediaFile
from .config import BASE_MEDIA_DIR

class HelloWorld(Resource):
    def get(self):
        return {'class': 'user',
        'first': 'john',
        'last': 'doe',
        }
api.add_resource(HelloWorld, '/')

class UploadThumbnail(Resource):
    """Upload either a video or an image file to be used as the product thumbnail"""
    
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'mp4'])
    
    def post(self, product_id):
        file = request.files['file']
        if file and self.allowed_file(file.filename):
            try:
                filename = secure_filename("{}.{}".format(str(uuid.uuid4())[:8], self.file_type(file.filename)))
                file_path = os.path.join(BASE_MEDIA_DIR, filename)
                file.save(file_path)
                self.update_filepath(product_id, file_path)
                return "File uploaded"
            except Exception as e:
                #TODO log this, and add better handler
                return "Error. {}".format(e)
        else:
            #TODO log this and better error handling
            return 'File not allowed'
    
    def file_type(self, filename):
        return filename.rsplit('.', 1)[1].lower()

    def allowed_file(self, filename):
        return '.' in filename and self.file_type(filename) in self.ALLOWED_EXTENSIONS

    def update_filepath(self, product_id, file_path):
        """Updates the path in the DB. If a file was already uploaded, the function will
        first add they new path and update it and then remove the old file"""
        product = Product.query.get(product_id)
        old_path = product.thumbnail_path
        product.thumbnail_path = file_path
        db.session.add(product)
        db.session.commit()
        #TODO add an event to tell the UI to look for a new thumbnail
        if old_path is not None:
            os.remove(old_path)
api.add_resource(UploadThumbnail, '/upload/thumbnail/<string:product_id>')
