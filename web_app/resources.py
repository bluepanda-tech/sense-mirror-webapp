"""Contains main API resources"""
import os, uuid

from flask import request, flash, redirect
from flask_restful import Resource
from werkzeug.utils import secure_filename
from flask_login import login_required

from .app import (
    app,
    api,
    db,
)
from .models import (
    Product,
    MediaFile,
    DeletedFile,
    ProductEdit,
)
from .config import (
    BASE_MEDIA_DIR,
    ALLOWED_FILE_EXTENSIONS,
    MAX_STORED_MEDIA_FILES,
)
from .utils import (
    file_type,
    allowed_file,
)

class EditProductInfo(Resource):
    """API to edit a products name, description and is_displayed"""
    #TODO Add validation here
    def post(self, product_id):
        name = request.form['name']
        description = request.form['description']
        is_displayed = False
        if request.form.get('is_displayed') is not None:
            is_displayed = True
        product = Product.query.get(product_id)
        product.name = name
        product.description_txt = description
        product.is_displayed = is_displayed
        db.session.add(product)
        # Saving event in Database
        event = {
            "[EditProductInfo]" : {
                "id" : product_id,
                "name" : name,
                "description" : description,
                "is_displayed" : is_displayed,
            }
        }
        new_event = ProductEdit(event_descr=str(event))
        db.session.add(new_event)

        db.session.commit()
        flash("Producto editado exitosamente")
        return redirect('/dashboard/product/{}/'.format(product_id))
api.add_resource(EditProductInfo, '/api/product/<string:product_id>/')

class UploadThumbnail(Resource):
    """Upload either a video or an image file to be used as the product thumbnail"""
    method_decorators = [login_required]
    def post(self, product_id):
        """API endpoint to upload a product's thumbnail. The actual deletion
        of the file in the host's disk is performed by the UI container"""

        #TODO log this and better error handling

        file = request.files['file']

        if file and allowed_file(file.filename, ALLOWED_FILE_EXTENSIONS):
            product = Product.query.get(product_id)
            old_filename = product.thumbnail
            filename = secure_filename("{}.{}".format(
                str(uuid.uuid4())[:8], # Generates 8-digit uuid
                file_type(file.filename)
            )) # appends the file type to it
            file.save(os.path.join(BASE_MEDIA_DIR, filename))
            product.add_thumbnail_filename(filename)
            db.session.add(product)
            # Actual file is deleted only by the GUI
            try:
                file_to_delete = DeletedFile(old_filename)
                db.session.add(file_to_delete)
            except ValueError as e:
                print(e)
            # Saving event in Database
            event = {
                "[UploadThumbnail]" : {
                    "id" : product_id,
                    "filename" : filename,
                }
            }
            new_event = ProductEdit(event_descr=str(event))
            db.session.add(new_event)
            db.session.commit()
            flash("Archivo subido con éxito")
            return redirect('/dashboard/product/{}/'.format(product_id))
        else:
            #TODO add bad status codes to this type of responses
            flash('File not allowed. Upload only {} files'.format(
                [ftype for ftype in ALLOWED_FILE_EXTENSIONS]
            ))
            return redirect('/dashboard/product/{}/'.format(product_id))
api.add_resource(UploadThumbnail, '/api/thumbnail/<string:product_id>/')

class AddMediaFile(Resource):
    """Upload or delete media files to be shown in the product's description"""
    method_decorators = [login_required]
    def post(self, product_id):
        """Upload a mediafile"""
        file = request.files['file']
        if file and allowed_file(file.filename, ALLOWED_FILE_EXTENSIONS) and MediaFile.query.filter_by(product_id=product_id).count() < MAX_STORED_MEDIA_FILES and Product.product_exists(product_id):
            # file must be allowed, product_id must exist and
            # media files should be less than max allowed
            #TODO log this and better error handling
            filename = secure_filename("{}.{}".format(str(uuid.uuid4())[:8], file_type(file.filename)))
            file_path = os.path.join(BASE_MEDIA_DIR, filename)
            file.save(file_path)
            new_file = MediaFile(product_id, filename)
            db.session.add(new_file)
            # Saving event in Database
            event = {
                "[AddMediaFile]" : {
                    "id" : product_id,
                    "filename" : filename,
                }
            }
            new_event = ProductEdit(event_descr=str(event))
            db.session.add(new_event)
            db.session.commit()
            flash("Archivo guardado con éxito")
            return redirect('/dashboard/product/{}/'.format(product_id))
        elif not allowed_file(file.filename, ALLOWED_FILE_EXTENSIONS):
            flash("File not allowed, must be of format {}".format([filetype for filetype in ALLOWED_FILE_EXTENSIONS]))
            return redirect('/dashboard/product/{}/'.format(product_id))
        elif not MediaFile.query.filter_by(product_id=product_id).count() < MAX_STORED_MEDIA_FILES:
            flash("Product reached max number of mediafiles: {}".format(MAX_STORED_MEDIA_FILES))
            return redirect('/dashboard/product/{}/'.format(product_id))
        elif not Product.product_exists(product_id):
            flash("Producto invalido")
            return redirect('/dashboard/product/{}/'.format(product_id))
        else:
            flash("Seleccione un archivo")
            return redirect('/dashboard/product/{}/'.format(product_id))
api.add_resource(AddMediaFile, '/api/mediafile/<string:product_id>/')

#TODO Se puede undir el boton de guardar o anadir sin seleccionar archivo
# Make client disable button until archive is mounted
class DeleteMediaFile(Resource):
    """Deletes Media files based on their filename"""
    method_decorators = [login_required]
    def get(self, filename):
        """Delete a media file"""
        mediafile = MediaFile.query.get(filename)
        product_id = mediafile.product_id
        if mediafile is not None:
            file_to_delete = DeletedFile(filename)
            db.session.add(file_to_delete)
            db.session.delete(mediafile)
            # Saving event in Database
            event = {
                "[DeleteMediaFile]" : {
                    "id" : product_id,
                    "filename" : mediafile,
                }
            }
            new_event = ProductEdit(event_descr=str(event))
            db.session.add(new_event)
            db.session.commit()
            flash("Archivo eliminado con éxito")
            return redirect('/dashboard/product/{}/'.format(product_id))
        flash("Lo siento, no pudimos eliminar el archivo: Archivo inexistente.")
        return redirect('/dashboard/product/{}/'.format(product_id))
api.add_resource(DeleteMediaFile, '/api/mediafile/delete/<string:filename>/')
