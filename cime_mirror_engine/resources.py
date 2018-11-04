import os

from flask import request
from flask_restful import Resource

from .app import app, api, db
from .models import Product, MediaFile
from .config import BASE_MEDIA_DIR, ALLOWED_FILE_EXTENSIONS
from .utils import (
    file_type,
    allowed_file,
)

class UploadThumbnail(Resource):
    """Upload either a video or an image file to be used as the product thumbnail"""
        
    def post(self, product_id):
        file = request.files['file']
        if file and allowed_file(file.filename, ALLOWED_FILE_EXTENSIONS):
            product = Product.query.get(product_id)
            product.add_thumbnail(file)
            db.session.add(product)
            db.session.commit()
            return "File Uploaded"
        else:
            #TODO log this and better error handling
            return 'File not allowed'
api.add_resource(UploadThumbnail, '/api/upload/thumbnail/<string:product_id>')

class UploadMediaFile(Resource):
    """Upload media files to be shown in the product's description"""

    def post(self, product_id):
        """Upload a mediafile"""
        file = request.files['file']
        if file and allowed_file(file.filename, ALLOWED_FILE_EXTENSIONS):
            try:
                new_file = MediaFile(product_id, file)
                db.session.add(new_file)
                db.session.commit()
                return "File Uploaded"
            except Exception as e:
                return e
        else:
            #TODO log this and better error handling
            return 'File not allowed'
api.add_resource(UploadMediaFile, '/api/upload/mediafile/<string:product_id>')

class DeleteMediaFile(Resource):
    """Deletes mediafile"""

    def delete(self, filename):
        """Delete a media file"""
        mediafile = MediaFile.query.get(filename)
        if mediafile is not None:
            os.remove(os.path.join(BASE_MEDIA_DIR, filename))
            db.session.delete(mediafile)
            db.session.commit()
            return "File Deleted"
        else:
            return "File doesn't exist"
api.add_resource(DeleteMediaFile, '/api/delete/mediafile/<string:filename>')
