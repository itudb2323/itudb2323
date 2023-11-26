from flask import Blueprint, jsonify
from services.ProductService import ProductService

product_bp = Blueprint(name="/product", import_name=__name__, url_prefix="/product")


@product_bp.route("/", methods=["GET"])
def findAll():
    persons = ProductService.findAll()
    persons_list = [person.to_dict() for person in persons]
    return jsonify(persons_list)
