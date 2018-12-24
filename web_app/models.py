"""Database Models using Flask SQLAlchemy as ORM"""
import os

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from .config import ALLOWED_FILE_EXTENSIONS, BASE_MEDIA_DIR
from .app import db
from .utils import allowed_file, allowed_product_id

class User(db.Model):
    """User that will have access to the mirror's webapp
    only need to provide passwords, no usernames, as this
    application will be served on a local net.

    We will only create one superuser"""
    __tablename__ = 'app_user'

    user_id = db.Column(db.Integer, primary_key=True)
    pw_hash = db.Column(db.String(200))

    def __init__(self, password):
        # Only one PIN will be available to access the app.
        # This PIN is given right at the beginning and needs to
        # be written down.
        #TODO set up an email client for changing the password
        if User.query.count() == 0 and len(password) == 4 and password.isdigit():
            self.set_password(str(password))
        elif User.query.count() != 0:
            raise ValueError("A user and a password were already set")
        else:
            raise ValueError("Invalid PIN. Must be a 4-digit number")

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)

    def reset_password(self):
        #TODO finish this
        pass

    def __repr__(self):
        return str(self.user_id)

class Product(db.Model):
    """Products to be showcased by the UI"""
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True) # Only from 1 - MAX_PRODUCTS
    name = db.Column(db.String(80), nullable=False)
    description_txt = db.Column(db.Text)
    media_files = db.relationship(
        'MediaFile',
        backref='product',
        lazy=True,
        cascade="all, delete-orphan",
    )
    thumbnail = db.Column(db.Text, default='default-thumbnail.jpg') # Name of thumbnail file
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

    @staticmethod
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

class DeletedFile(db.Model):
    """Files to be deleted by the GUI once it updates"""
    __tablename__ = 'deleted_files'

    filename = db.Column(db.Text, primary_key=True, nullable=False)
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, filename):
        if filename is not None and 'default-thumbnail' not in filename:
            if os.path.exists(os.path.join(BASE_MEDIA_DIR, filename)):
                self.filename = filename
                self.deleted = False
        else:
            # Exception handled by AddThumbnail Resource class API
            raise ValueError("Cannot delete the default-thumbnail file")

    @staticmethod
    def delete_files():
        """Deletes files from disk"""
        files_to_delete = DeletedFile.query.filter_by(deleted=False).all()
        for file in files_to_delete:
            if file is not None and 'default-thumbnail' not in file:
                try:
                    os.remove((os.path.join(BASE_MEDIA_DIR, file.filename)))
                except:
                    print("File doesn't exist")
                    #TODO better handling of this thing
                    return "File Doesn't Exist"
                file.deleted = True
                db.session.add(file)
        db.session.commit()

class ProductEdit(db.Model):
    """Registers any database transaction and/or edition of a
    product alongside a column to check if the GUI already
    applied this changes. This is helpful because the GUI will be
    constantly looking for unapplied changes. If they are found,
    the whole Tkinter Window will be updated"""
    __tablename__ = 'product_edits'

    edition_id = db.Column(db.Integer, primary_key=True)
    edition_descr = db.Column(db.Text)
    was_applied = db.Column(db.Boolean, default=False)

    def __init__(self, event_descr):
        self.edition_descr = event_descr
        self.was_applied = False

#TODO create event from webapp to UI instead of this table
class ProductToDisplayInfo(db.Model):
    """This registers a product which info is going to be
    displayed by the UI. Will have only one row. This is
    done in the meantime, while an event is created later on"""
    __tablename__ = 'info_to_display'
    
    info_id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer)
    was_showed = db.Column(db.Boolean, default=True)
    is_showing = db.Column(db.Boolean, default=False)

    def __init__(self):
        if ProductToDisplayInfo.query.count() >= 1:
            raise ValueError("Only one row may exist")
