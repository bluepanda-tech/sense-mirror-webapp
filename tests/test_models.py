"""Unit tests for models and their methods. The
create_superuser function is ran in the __init__ file,
since we need that for the APIs and Auth tests"""
import pytest

from run import create_items, create_superuser
from web_app.app import app, db
from web_app.models import Product, MediaFile, User
from web_app.config import MAX_PRODUCTS

def test_db_connection():
    """Making sure we are not messing around with the actual db"""
    try:
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite://'
        db.create_all()
    except AssertionError:
        pytest.exit("Database URI wasn't changed")

#######################################
#########  USER MODEL TESTS ###########
#######################################

def test_user():
    """Test the creation and validation of users. Also makes
    sure that only one user can exist at a time."""
    pin = '1234'
    invalid_pin_1 = '12345'
    invalid_pin_2 = 'O123' # Letter O
    if User.query.count() != 0:
        # Checks if another user was already created... Since we
        # want to test the whole process
        user = User.query.first()
        db.session.delete(user)
    with pytest.raises(ValueError):
        # Tries to create user PIN with >4 digits
        new_user = User(invalid_pin_1)
    with pytest.raises(ValueError):
        # Tries to create user PIN with letters
        new_user = User(invalid_pin_2)
    new_user = User(pin)
    db.session.add(new_user)
    db.session.commit()
    assert User.query.first() is not None
    assert User.query.count() == 1
    assert new_user.is_authenticated()
    assert new_user.is_active()
    assert not new_user.is_anonymous()
    with pytest.raises(ValueError):
        # Make sure not other user is created
        another_user = User(pin)
    assert new_user.check_password(pin)

########################################
#########  PRODUCT MODEL TESTS #########
########################################
def test_create_items():
    """Tests functions that creates initial Product objects"""
    create_items()
    assert len(Product.query.all()) == MAX_PRODUCTS

def test_product():
    """Testing creation of Product objects"""
    with pytest.raises(ValueError):
        # Tests no duplicate product will be made
        newprod = Product(1)
    with pytest.raises(ValueError):
        # Tests products ids stay between intervals
        anotherprod = Product(MAX_PRODUCTS+1)
    assert Product.query.get(MAX_PRODUCTS).name == "Item {}".format(MAX_PRODUCTS)

def test_product_add_thumbnail_filename():
    """Tests adding a thumbnail filename"""
    prod = Product.query.get(1)
    prod.add_thumbnail_filename('file.png')
    assert prod.thumbnail == 'file.png'
    with pytest.raises(ValueError):
        prod.add_thumbnail_filename('file')
    # Remove sample filename
    prod.thumbnail = None

def test_product_exists():
    for i in range(MAX_PRODUCTS):
        product_id = i + 1
        assert Product.product_exists(product_id)
    assert not Product.product_exists(MAX_PRODUCTS+1)
####### END PRODUCT MODEL TESTS ########

########################################
######## MEDIAFILES MODEL TESTS ########
########################################
def test_mediafiles():
    """Testing the creation of mediafile objects"""
    product_id = 1
    filename = 'file.jpg'
    # Adding new filename to db
    newfile = MediaFile(product_id, filename)
    db.session.add(newfile)
    db.session.commit()
    # Getting that new created file
    medfile = MediaFile.query.get(filename)
    prod = Product.query.get(product_id)
    assert medfile.filename == filename
    assert medfile.product == prod
    assert prod.media_files == [medfile]
    # Remove sample file
    db.session.delete(medfile)
    db.session.commit()
####### END MEDIAFILES MODEL TESTS ########
