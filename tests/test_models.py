import pytest

from run import create_items
from cime_mirror_engine.app import app, db
from cime_mirror_engine.utils import MAX_PRODUCTS
from cime_mirror_engine.config import Test
from cime_mirror_engine.models import Product, MediaFile

#Configuration is changed for testing
app.config.from_object(Test)
db.create_all()

def test_db_connection():
    """Making sure we are not messing around with the actual db"""
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite://'

def test_create_items():
    """Tests functions that creates initial Product objects"""
    create_items()
    assert len(Product.query.all()) == MAX_PRODUCTS

def test_Product():
    """Testing creation of Product objects"""
    with pytest.raises(ValueError):
        # Tests no duplicate product will be made
        newprod = Product(1)
    with pytest.raises(ValueError):
        # Tests products ids stay between intervals
        anotherprod = Product(MAX_PRODUCTS+1)
    assert Product.query.get(MAX_PRODUCTS).name == "Item {}".format(MAX_PRODUCTS)

def test_Product_add_thumbnail_filename():
    """Tests adding a thumbnail filename"""
    prod = Product.query.get(1)
    prod.add_thumbnail_filename('file.png')
    assert prod.thumbnail == 'file.png'
    with pytest.raises(ValueError):
        prod.add_thumbnail_filename('file')

def test_product_exists():
    for i in range(MAX_PRODUCTS):
        product_id = i + 1
        assert Product.product_exists(product_id)
    assert not Product.product_exists(MAX_PRODUCTS+1)

def test_MediaFiles():
    product_id = 1
    filename = 'file.jpg'
    newfile = MediaFile(product_id, filename)
    db.session.add(newfile)
    db.session.commit()
    medfile = MediaFile.query.get(filename)
    prod = Product.query.get(product_id)
    assert medfile.filename == filename
    assert medfile.product == prod
    assert prod.media_files == [medfile]
