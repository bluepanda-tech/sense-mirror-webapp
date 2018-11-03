import os

def test_testing_the_test():
    from cime_mirror_engine.app import app, db
    from cime_mirror_engine.models import Product

    assert Product.query.count() == 1