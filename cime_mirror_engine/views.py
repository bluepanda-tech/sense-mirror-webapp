"""Routes for the UI routes"""
from flask_login import login_required
from flask import (
    render_template,
    redirect,
    flash,
)

from .app import app, login
from .models import Product

@login.unauthorized_handler
def unauthorized():
    """Default redirect when tries to acces url that needs auth, without one"""
    return redirect('/login/')

@app.route('/')
def index():
    """Main route. Redirects to dashboard"""
    return redirect('/dashboard')

@app.route('/login/')
def login_ui():
    """Route for user's login UI"""
    return render_template('login.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    """Route for official BluePanda Dahsboard"""
    products = [dict(
        name=product.name,
        description=product.description_txt,
        thumbnail=product.thumbnail,
        is_displayed=product.is_displayed,
        mediafiles=product.media_files
    ) for product in Product.query.all()]
    return render_template('dashboard.html', products=products)

@app.route('/dashboard/edit/<product_id>/')
@login_required
def edit_product(product_id):
    """View to edit individual products"""
    product_obj = Product.query.get(product_id)
    if product_obj is not None:
        product = {
            'name' : product_obj.name,
            'description' : product_obj.description_txt,
            'thumbnail' : product_obj.thumbnail,
            'mediafiles' : product_obj.media_files,
        }
        return render_template('edit_product.html', product=product)
    flash("Producto no encontrado. ID invalida.")
    return redirect('/dashboard/')
