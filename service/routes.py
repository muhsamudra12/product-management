from flask import jsonify, request, url_for, abort, render_template
from flask_api import status  # HTTP Status Codes
from service.models import Product
from . import app

######################################################################
# Health Check 
######################################################################
@app.route("/health", methods=["GET"])
def health():
    return jsonify(dict(status="OK")), status.HTTP_200_OK

######################################################################
# LIST ALL PRODUCTS & SEARCHING (Task 4 & 6)
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """Returns all Products or searches based on query string"""
    app.logger.info("Request to list products")
    products = []
    
    
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        products = Product.find_by_name(name)
    elif category:
        products = Product.find_by_category(category)
    elif available:
        
        is_available = available.lower() in ["true", "1", "yes"]
        products = Product.find_by_availability(is_available)
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK

######################################################################
# READ A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """Retrieve a single Product based on ID"""
    app.logger.info("Request to retrieve product with id: %s", product_id)
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    
    return jsonify(product.serialize()), status.HTTP_200_OK

######################################################################
# CREATE A NEW PRODUCT
######################################################################
@app.route("/products", methods=["POST"])
def create_products():
    """Creates a Product"""
    app.logger.info("Request to create a product")
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    message = product.serialize()
    location_url = url_for("get_products", product_id=product.id, _external=True)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}

######################################################################
# UPDATE AN EXISTING PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """Updates a Product"""
    app.logger.info("Request to update product with id: %s", product_id)
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    
    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    return jsonify(product.serialize()), status.HTTP_200_OK

######################################################################
# DELETE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """Deletes a Product"""
    app.logger.info("Request to delete product with id: %s", product_id)
    product = Product.find(product_id)
    if product:
        product.delete()
    return "", status.HTTP_204_NO_CONTENT


@app.route("/")
def index():
    """Displaying the main page (UI) for Testing"""
    return render_template("index.html"), status.HTTP_200_OK