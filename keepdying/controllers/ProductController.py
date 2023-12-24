import traceback
from flask import Blueprint, jsonify, render_template, redirect, url_for, request, flash
from services.ProductService import ProductService
from models.Product import field_types as product_field_types

product_bp = Blueprint(name="product", import_name=__name__, url_prefix="/product")


@product_bp.route("/", methods=["GET"])
def show_base():
    return redirect(url_for("product.page", page=1))


@product_bp.route("/read", methods=["GET"])
def find_all():
    products = ProductService.find_all()
    products_list = [product.to_dict() for product in products]
    return jsonify(products_list)


@product_bp.route("/read/id/<int:id>", methods=["GET", "POST"])
def find_details_by_id(id):
    product_details = None
    try:
        product_details = ProductService.find_details_by_id(id)
        if request.method == "POST":
            return jsonify(product_details.to_dict())
    except Exception as e:
        print(repr(e))
        if request.method == "POST":
            return jsonify({"error": "Product not found!"}), 404
    return render_template(
        "product/read_by_id.html", id=id, product_details=product_details
    )


@product_bp.route("/read/<int:page>")
def page(page):
    # If page 0 redirect to page 1
    if page == 0:
        return redirect(url_for("product.page", page=1))
    sort_by = request.args.get("sort_by", default="productid")
    order = request.args.get("order", default="asc")
    per_page = 20  # Number of products per page
    pagination, products = ProductService.find_all_paginated(
        page, per_page, sort_by, order
    )
    if page > pagination["total_pages"] and pagination["total_pages"] != 0:
        return redirect(url_for("product.page", page=pagination["total_pages"]))
    return render_template(
        "product/read_paginated.html", products=products, pagination=pagination
    )


@product_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        try:
            # Extract data from form
            form_data = request.form.to_dict()
            # Convert data to appropriate types
            for key, value in form_data.items():
                if type(value) == str and (value == "" or value == "None"):
                    form_data[key] = None
                else:
                    form_data[key] = product_field_types[key](value)
            # Set default values for bools TODO: Handle this better
            form_data["makeflag"] = form_data.get("makeflag", False)
            form_data["finishedgoodsflag"] = form_data.get("finishedgoodsflag", False)
            # Create the product
            product = ProductService.create(**form_data)
            flash("Product created successfully!", "success")
            return redirect(url_for("product.find_details_by_id", id=product.productid))
        except Exception as e:
            print(repr(e))
            print(traceback.format_exc())
            flash(repr(e), "error")

    return render_template("product/create.html")


@product_bp.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    product_details = ProductService.find_details_by_id(id)
    try:
        if request.method == "POST":
            # Extract data from form
            form_data = request.form.to_dict()
            # Convert data to appropriate types
            for key, value in form_data.items():
                if type(value) == str and (value == "" or value == "None"):
                    form_data[key] = None
                else:
                    form_data[key] = product_field_types[key](value)
            # Set default values for bools TODO: Handle this better
            form_data["makeflag"] = form_data.get("makeflag", False)
            form_data["finishedgoodsflag"] = form_data.get("finishedgoodsflag", False)
            form_data["rowguid"] = product_details.rowguid
            # Update the product
            product = ProductService.update(id, **form_data)
            flash("Product updated successfully!", "success")
            return redirect(url_for("product.find_details_by_id", id=product.productid))
    except Exception as e:
        print(repr(e))
        if request.method == "POST":
            flash(repr(e), "error")

    return render_template(
        "product/update.html", id=id, product_details=product_details
    )


@product_bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    try:
        ProductService.delete(id)
        flash("Product deleted successfully!", "success")
    except Exception as e:
        print(repr(e))
        flash("Product not found!", "error")

    return redirect(url_for("product.page", page=1))
