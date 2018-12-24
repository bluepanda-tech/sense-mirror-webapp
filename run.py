"""Script to be run on boot/startup"""
import time
from web_app.app import app, db
from web_app import models
from web_app.utils import allowed_product_id
from web_app.config import MAX_PRODUCTS

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

def create_product_info_event():
    """Creates row in ProductToDisplayInfo table that manages
    products which further info will be displayed if doesn't
    exists already"""
    if models.ProductToDisplayInfo.query.count() == 0:
        event = models.ProductToDisplayInfo()
        db.session.add(event)
        db.session.commit()
        print("Event to display prod.info created...")

def wait_for_postgres():
    try:
        db.engine.execute("SELECT 1")
        print("connected to db")
        return None
    except:
        time.sleep(1)
        wait_for_postgres()

wait_for_postgres()
db.create_all()
create_items()
create_superuser()
create_product_info_event()

if __name__ == '__main__':
    app.run()
