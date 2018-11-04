import os
import uuid

from werkzeug.utils import secure_filename

from .config import MAX_PRODUCTS, MAX_STORED_MEDIA_FILES, BASE_MEDIA_DIR
from .app import db
from .utils import (
    file_type,
    allowed_product_id,
)

class Product(db.Model):
    """Products to be showcased by the UI"""
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True) # Only from 1 - MAX_PRODUCTS
    name = db.Column(db.String(80), nullable=False)
    description_txt = db.Column(db.Text)
    media_files = db.relationship('MediaFile', backref='product', lazy=True)
    thumbnail = db.Column(db.Text, default=None) # Name of thumbnail file
    is_displayed = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, product_id):
        if allowed_product_id(product_id, MAX_PRODUCTS) and not Product.product_exists(product_id):
            self.product_id = product_id
            self.name = "Item {}".format(product_id)
        elif Product.product_exists(product_id):
            #TODO test this
            raise ValueError('Item {} already exists'.format(product_id))
        else:
            raise ValueError('Invalid item number', product_id)

    def add_thumbnail(self, file):
        """Updates the name of the file. If a file was already uploaded, the function will
        first add they new path and update it and then remove the old file"""
        filename = secure_filename("{}.{}".format(str(uuid.uuid4())[:8], file_type(file.filename)))
        file_path = os.path.join(BASE_MEDIA_DIR, filename)
        old_filename = self.thumbnail
        file.save(file_path)
        self.thumbnail = filename
        #TODO add an event to tell the UI to look for a new thumbnail
        if old_filename is not None:
            os.remove(os.path.join(BASE_MEDIA_DIR, old_filename))

    def product_exists(product_id):
        """Checks if the item already exists based on the item number"""
        exists = Product.query.filter_by(product_id=product_id).scalar() is not None
        return exists

    def __repr__(self):
        return "{}".format(self.name)

class MediaFile(db.Model):
    """Paths to media files to be displayed in the product's description"""
    __tablename__ = 'media_files'
    
    filename = db.Column(db.Text, primary_key=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)

    def __init__(self, product_id, file):
        #TODO add file validation in the resources file...
        if MediaFile.query.filter_by(product_id=product_id).count() < MAX_STORED_MEDIA_FILES:
            filename = secure_filename("{}.{}".format(str(uuid.uuid4())[:8], file_type(file.filename)))
            file_path = os.path.join(BASE_MEDIA_DIR, filename)
            file.save(file_path)
            self.product_id = product_id
            self.filename = filename
        else:
            raise ValueError('Reached Max Number of Media files for this product')
    
    def __repr__(self):
        return "{}".format(self.filename)
    