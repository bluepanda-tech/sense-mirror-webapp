from .config import ALLOWED_FILE_EXTENSIONS
from .app import db
from .utils import allowed_file, allowed_product_id

class Product(db.Model):
    """Products to be showcased by the UI"""
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True) # Only from 1 - MAX_PRODUCTS
    name = db.Column(db.String(80), nullable=False)
    description_txt = db.Column(db.Text)
    media_files = db.relationship('MediaFile', backref='product', lazy=True, cascade="all, delete-orphan")
    thumbnail = db.Column(db.Text, default=None) # Name of thumbnail file
    is_displayed = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, product_id):
        if allowed_product_id(product_id) and not Product.product_exists(product_id):
            self.product_id = product_id
            self.name = "Item {}".format(product_id)
        else:
            raise ValueError('Product id not allowed')

    def add_thumbnail_filename(self, filename):
        """Updates the name of the file"""
        if allowed_file(filename, ALLOWED_FILE_EXTENSIONS):
            self.thumbnail = filename
        else:
            raise ValueError('Thumbnail filename not allowed')

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

    def __init__(self, product_id, filename):
        if allowed_file(filename, ALLOWED_FILE_EXTENSIONS):
            self.product_id = product_id
            self.filename = filename
        else:
            raise ValueError('Filename not allowed: "{}"'.format(filename))
    
    def __repr__(self):
        return "{}".format(self.filename)
    