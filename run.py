from cime_mirror_engine.app import app, db
from cime_mirror_engine import models
from cime_mirror_engine.config import MAX_PRODUCTS

def create_items():
    for product in range(MAX_PRODUCTS):
        try:
            item_num = product + 1
            new_product = models.Product(item_num=item_num)
            db.session.add(new_product)
        except Exception as e:
            #TODO log this or something
            print(e)
    db.session.commit()

if __name__ == '__main__':
    db.create_all()
    create_items()
    app.run()