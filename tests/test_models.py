import os
import requests
import pytest

from run import create_items
from cime_mirror_engine.app import app, db
from cime_mirror_engine.models import Product, MediaFile
from cime_mirror_engine.config import (
    Test,
    BASE_MEDIA_DIR,
    MAX_PRODUCTS,
)

#Configuration is changed for testing
app.config.from_object(Test)
client = app.test_client()

##########################################
#### TESTING MODELS AND THEIR METHODS ####
##########################################

def test_db_connection():
    """Making sure we are not messing around with the actual db"""
    try:
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite://'
        db.create_all()
    except AssertionError:
        pytest.exit("Database URI wasn't changed")

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
    # Remove sample filename
    prod.thumbnail = None

def test_product_exists():
    for i in range(MAX_PRODUCTS):
        product_id = i + 1
        assert Product.product_exists(product_id)
    assert not Product.product_exists(MAX_PRODUCTS+1)

def test_MediaFiles():
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

#########################################
## TESTING RESOURCES AND THEIR METHODS ##
#########################################

def test_uploadthumbnail():
    """Tests the function that uploads a thumbnail"""
    product_id = 1
    with open('./tests/etc/sample.jpg', 'rb') as file:
        response = client.post(
            '/api/thumbnail/{}'.format(product_id),
            data={'file' : file},
            content_type='multipart/form-data'
        )
        # Check responses
        assert response.status_code == 200
        assert response.data == b'"File Uploaded"\n'
    prod = Product.query.get(1)
    tn_filename = prod.thumbnail
    # Check file gets saved
    assert os.path.exists(os.path.join(BASE_MEDIA_DIR, tn_filename))
    # Doing it again to check old file gets deleted
    with open('./tests/etc/sample.jpg', 'rb') as file:
        response = client.post('/api/thumbnail/1', data={'file' : file}, content_type='multipart/form-data')
    assert not os.path.exists(os.path.join(BASE_MEDIA_DIR, tn_filename))

def test_mediafiles_post():
    """Tests the function that uploads a thumbnail"""
    product_id = 1
    with open('./tests/etc/sample.jpg', 'rb') as file:
        response = client.post(
            '/api/mediafile/{}'.format(product_id),
            data={'file' : file},
            content_type='multipart/form-data'
        )
        # Check responses
        assert response.status_code == 200
        assert response.data == b'"File Uploaded"\n'
    mediafile = MediaFile.query.filter_by(product_id=1).one()
    m_filename = mediafile.filename
    # Check file gets saved
    assert os.path.exists(os.path.join(BASE_MEDIA_DIR, m_filename))

def test_mediafiles_delete():
    """Tests the deletion of media files"""
    mediafile = MediaFile.query.filter_by(product_id=1).one()
    m_filename = mediafile.filename
    response = client.delete('/api/mediafile/{}'.format(
        m_filename,
    ))
    # Check MediaFile object no longer exists
    assert MediaFile.query.get(m_filename) is None
    # Check product does still exists (wasn't deleted in cascade)
    assert Product.query.get(1) is not None
    # Check file got deleted from path
    assert not os.path.exists(os.path.join(BASE_MEDIA_DIR, m_filename))
