from .app import db
from .config import MAX_PRODUCTS, MAX_STORED_MEDIA_FILES, BASE_MEDIA_DIR

class Product(db.Model):
    """Products to be showcased by the UI"""
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True) # Only from 1 - MAX_PRODUCTS
    name = db.Column(db.String(80), nullable=False)
    description_txt = db.Column(db.Text)
    media_files = db.relationship('MediaFile', backref='product', lazy=True)
    thumbnail_path = db.Column(db.Text, default=None)
    is_displayed = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, product_id):
        if self.allowed_product_id(product_id) and not self.item_exists(product_id):
            try:
                self.product_id = product_id
                self.name = "Item {}".format(product_id)
            except Exception as e:
                #TODO log this
                return e
        elif self.item_exists(product_id):
            #TODO test this
            raise ValueError('Item {} already exists'.format(product_id))
        else:
            raise ValueError('Invalid item number', product_id)

    def item_exists(self, product_id):
        """Checks if the item already exists based on the item number"""
        exists = Product.query.filter_by(product_id=product_id).scalar() is not None
        return exists

    def allowed_product_id(self, product_id):
        """Checks if product_id is an int, positive and less than MAX_PRODUCTS"""
        is_valid = (isinstance(product_id, int)) and (product_id > 0) and (product_id <= MAX_PRODUCTS)
        return is_valid

    def __repr__(self):
        return "{}".format(self.name)

class MediaFile(db.Model):
    """Paths to media files to be displayed in the product's description"""
    __tablename__ = 'media_files'
    
    file_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    file_path = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, product_id, file_path):
        if MediaFile.query.filter_by(product_id=product_id).count() < MAX_STORED_MEDIA_FILES and self.allowed_filepath(file_path):
            try:
                self.product_id = product_id
                self.file_path = file_path
            except Exception as e:
                #TODO log this
                return e
        elif MediaFile.query.filter_by(product_id=product_id).count() >= MAX_STORED_MEDIA_FILES:
            raise ValueError('Reached Max Number of Media files for this product')
        else:
            raise ValueError('File path not allowed')
    
    def allowed_filepath(self, file_path):
        """Checks if path is a string and inside the base media directory"""
        is_valid = (isinstance(file_path, str)) and BASE_MEDIA_DIR in file_path
        return is_valid
    
    def __repr__(self):
        return "{}".format(self.file_path)
    