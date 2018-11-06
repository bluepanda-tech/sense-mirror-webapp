from cime_mirror_engine.utils import (
    file_type,
    allowed_file,
    allowed_product_id,
)

def test_file_type():
    sample_files = {
        'sample.png' : 'png',
        'sample2.JPG' : 'jpg',
        'sample5.mp4' : 'mp4',
        'sample4.MP4' : 'mp4',
    }
    for samplefile in sample_files:
        assert file_type(samplefile) == sample_files[samplefile]

def test_allowed_file():
    sample_files = {
        'sample.png' : True,
        'sample2.JPG' : True,
        'sample5.mp4' : True,
        'sample4.pdf' : False,
        'sample5pdf' : False,
    }
    for samplefile in sample_files:
        assert allowed_file(samplefile) == sample_files[samplefile]

def test_allowed_product_id():
    from cime_mirror_engine.config import MAX_PRODUCTS
    sample_ids = {
        0 : False,
        '1' : False,
    }
    for sample_id in sample_ids:
        assert allowed_product_id(sample_id) == sample_ids[sample_id]
    for allowed_id in range(MAX_PRODUCTS):
        assert allowed_product_id(allowed_id+1) == True
