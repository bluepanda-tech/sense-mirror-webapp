"""Script to be run on boot/startup"""
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

def create_superuser():
    """Creates a superuser the first time of initiating the program"""
    if models.User.query.count() == 0:
        su = models.User('1234') #TODO find better way to do this
        db.session.add(su)
        db.session.commit()

if __name__ == '__main__':
    db.create_all()
    create_items()
    create_superuser()
    app.run()
