from flask import Blueprint, jsonify, render_template, request, url_for
from services.PersonService import PersonService

person_bp = Blueprint(name="person", import_name=__name__, url_prefix="/person")


@person_bp.route("/", methods=["GET"])
def findAllPaginated():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    pagination, persons = PersonService.findAllPaginated(page=page, per_page=per_page)
    return render_template(
        "person/index.html",
        pagination=pagination,
        persons=persons,
    )


@person_bp.route("/<int:id>", methods=["GET"])
def findDetailsById(id):
    personDetails = PersonService.findDetailsById(id)
    return render_template("person/details.html", personDetails=personDetails)
