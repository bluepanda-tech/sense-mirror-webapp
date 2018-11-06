from .config import ALLOWED_FILE_EXTENSIONS, MAX_PRODUCTS

def file_type(filename):
    """Returns filetype of file"""
    return filename.rsplit('.', 1)[1].lower()

def allowed_file(filename, allowed_filetypes=ALLOWED_FILE_EXTENSIONS):
    """Returns Boolean. If file has a dot and is part of allowed filetypes"""
    return '.' in filename and file_type(filename) in allowed_filetypes

def allowed_product_id(product_id, max_products=MAX_PRODUCTS):
    """Checks if product_id is an int, positive and less than MAX_PRODUCTS"""
    is_valid = (isinstance(product_id, int)) and (product_id > 0) and (product_id <= max_products)
    return is_valid
