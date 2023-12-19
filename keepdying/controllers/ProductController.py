from flask import Blueprint, jsonify, render_template, redirect, url_for
from services.ProductService import ProductService

product_bp = Blueprint(name="product", import_name=__name__, url_prefix="/product")


@product_bp.route("/", methods=["GET"])
def showBase():
    return render_template("base.html")


@product_bp.route("/read", methods=["GET"])
def findAll():
    products = ProductService.findAll()
    products_list = [product.to_dict() for product in products]
    return jsonify(products_list)

@product_bp.route('/read/<int:page>')
def page(page):
    # If page 0 redirect to page 1
    if page == 0:
        return redirect(url_for('product.page', page=1))
    per_page = 10  # Number of products per page
    pagination, products = ProductService.findAllPaginated(page, per_page)
    if page > pagination["total_pages"] and pagination["total_pages"] != 0:
        return redirect(url_for('product.page', page=pagination["total_pages"]))
    return render_template('products/read_paginated.html', products=products, pagination=pagination)
