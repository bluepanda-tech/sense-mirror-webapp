"""TESTING RESOURCES AND THEIR METHODS"""
import os
from tests import client
from cime_mirror_engine.app import app, db
from cime_mirror_engine.config import BASE_MEDIA_DIR
from cime_mirror_engine.models import Product, MediaFile

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
        response = client.post(
            '/api/thumbnail/{}'.format(product_id),
            data={'file' : file},
            content_type='multipart/form-data',
        )
    assert not os.path.exists(os.path.join(BASE_MEDIA_DIR, tn_filename))
    # Remove image
    filename = Product.query.get(product_id).thumbnail
    os.remove(os.path.join(BASE_MEDIA_DIR, filename))

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
    # Check response
    assert response.data == b'"File Deleted"\n' 
    # Check MediaFile object no longer exists
    assert MediaFile.query.get(m_filename) is None
    # Check product does still exists (wasn't deleted in cascade)
    assert Product.query.get(1) is not None
    # Check file got deleted from path
    assert not os.path.exists(os.path.join(BASE_MEDIA_DIR, m_filename))
