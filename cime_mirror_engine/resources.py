import os, uuid

from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename

from .app import app, api, db
from .models import Product, MediaFile
from .config import (
    BASE_MEDIA_DIR,
    ALLOWED_FILE_EXTENSIONS,
    MAX_STORED_MEDIA_FILES,
)
from .utils import (
    file_type,
    allowed_file,
)

class UploadThumbnail(Resource):
    """Upload either a video or an image file to be used as the product thumbnail"""
        
    def post(self, product_id):
        """API endpoint to upload a product's thumbnail"""

        #TODO log this and better error handling

        file = request.files['file']

        if file and allowed_file(file.filename, ALLOWED_FILE_EXTENSIONS):
            product = Product.query.get(product_id)
            old_filename = product.thumbnail
            filename = secure_filename("{}.{}".format(str(uuid.uuid4())[:8], file_type(file.filename)))
            file.save(os.path.join(BASE_MEDIA_DIR, filename))
            product.add_thumbnail_filename(filename)
            db.session.add(product)
            db.session.commit()
            #TODO add an event to tell the UI to look for a new thumbnail, so that the command above is
            #executed only when the UI sends an event indicating it is now aware of the change
            if old_filename is not None:
                os.remove(os.path.join(BASE_MEDIA_DIR, old_filename))
            return "File Uploaded"
        else:
            #TODO add bad status codes to this type of responses
            return 'File not allowed. Upload only {} files'.format(
                [ftype for ftype in ALLOWED_FILE_EXTENSIONS]
            )
api.add_resource(UploadThumbnail, '/api/thumbnail/<string:product_id>')

class MediaFiles(Resource):
    """Upload or delete media files to be shown in the product's description"""

    def post(self, product_id):
        """Upload a mediafile"""
        file = request.files['file']
        if file and allowed_file(file.filename, ALLOWED_FILE_EXTENSIONS) and MediaFile.query.filter_by(product_id=product_id).count() < MAX_STORED_MEDIA_FILES and Product.product_exists(product_id):
            # file must be allowed, product_id must exist and media files should be less than max allowed
            #TODO log this and better error handling
            filename = secure_filename("{}.{}".format(str(uuid.uuid4())[:8], file_type(file.filename)))
            file_path = os.path.join(BASE_MEDIA_DIR, filename)
            file.save(file_path)
            new_file = MediaFile(product_id, filename)
            db.session.add(new_file)
            db.session.commit()
            return "File Uploaded"
        elif not allowed_file(file.filename, ALLOWED_FILE_EXTENSIONS):
            return "File not allowed, must be of format {}".format([filetype for filetype in ALLOWED_FILE_EXTENSIONS])
        elif not MediaFile.query.filter_by(product_id=product_id).count() < MAX_STORED_MEDIA_FILES:
            return "Product reached max number of mediafiles: {}".format(MAX_STORED_MEDIA_FILES)
        elif not Product.product_exists(product_id):
            return "Product ID is invalid."
api.add_resource(MediaFiles, '/api/mediafile/<string:product_id>')

class DeleteMediaFiles(Resource):
    """Deletes Media files based on their filename"""

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
api.add_resource(DeleteMediaFiles, '/api/mediafile/<string:filename>')
