from .app import db
from .config import MAX_PRODUCTS, BASE_MEDIA_DIR

class Product(db.Model):
    """Products to be showcased by the UI"""
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True)
    item_num = db.Column(db.Integer, unique=True, nullable=False) # From 1 - MAX_PRODUCTS
    name = db.Column(db.String(80), nullable=False)
    is_displayed = db.Column(db.Boolean, default=False)
    media_path = db.Column(db.String(80), unique=True, nullable=False)
    stored_media_files = db.Column(db.Integer, nullable=False, default=0) # Number of multimedia resources, must be < MAX_STORED_MEDIA_RESOURCES
    description_txt = db.Column(db.Text)

    def __init__(self, item_num):
        if self.item_num_is_valid(item_num) and not self.item_exists(item_num):
            self.item_num = item_num
            self.name = "Item {}".format(item_num)
            self.media_path = '{}/{}'.format(BASE_MEDIA_DIR, item_num) #TODO add test to assert base directory exists
        elif self.item_exists(item_num):
            #TODO test this
            raise ValueError('Item {} already exists'.format(item_num))
        else:
            raise ValueError('Invalid item number', item_num)

    def item_exists(self, item_num):
        """Checks if the item already exists based on the item number"""
        exists = Product.query.filter_by(item_num=item_num).scalar() is not None
        return exists

    def item_num_is_valid(self, item_num):
        """Checks if item_num is an int, positive and less than MAX_PRODUCTS"""
        is_valid = (isinstance(item_num, int)) and (item_num > 0) and (item_num <= MAX_PRODUCTS)
        return is_valid

    def __repr__(self):
        return "{}".format(self.name)
