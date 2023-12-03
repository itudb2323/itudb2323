from flask import Blueprint, jsonify
from services.ProductService import ProductService

product_bp = Blueprint(name="/product", import_name=__name__, url_prefix="/product")


@product_bp.route("/", methods=["GET"])
def findAll():
    products = ProductService.findAll()
    products_list = [product.to_dict() for product in products]
    return jsonify(products_list)
