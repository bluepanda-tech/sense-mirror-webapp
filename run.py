from cime_mirror_engine.app import app, db
from cime_mirror_engine import models
from cime_mirror_engine.utils import allowed_product_id
from cime_mirror_engine.config import MAX_PRODUCTS

def create_items():
    """Creates all products in the DB"""
    for product_id in range(MAX_PRODUCTS):
        if not models.Product.product_exists(product_id+1) and \
        allowed_product_id(product_id+1, MAX_PRODUCTS):
            new_product = models.Product(product_id+1)
            db.session.add(new_product)
        else:
            #TODO log this or something
            print("Product already exists")
    db.session.commit()

if __name__ == '__main__':
    db.create_all()
    create_items()
    app.run()
