from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from models.PersonDetails import PersonDetails
from services.PersonService import PersonService
from dtos.PersonCreateDTO import PersonCreateDto

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


@person_bp.route("/<int:id>/update", methods=["GET", "POST"])
def updateDetailsById(id):
    if request.method == "POST":
        new_data = {
            "firstname": request.form.get("firstname"),
            "middlename": request.form.get("middlename"),
            "lastname": request.form.get("lastname"),
            "phonenumber": request.form.get("phonenumber"),
            "emailaddress": request.form.get("emailaddress"),
        }
        print(new_data)
        personDetails = PersonDetails(**new_data) 
        
        PersonService.updateDetailsById(id, personDetails)
        return redirect(url_for("person.findDetailsById", id=id))

    personDetails = PersonService.findDetailsById(id)
    return render_template("person/update.html", personDetails=personDetails)


@person_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        new_data = {
            "persontype": request.form.get("persontype"),
            "firstname": request.form.get("firstname"),
            "middlename": request.form.get("middlename"),
            "lastname": request.form.get("lastname"),
            "emailaddress": request.form.get("emailaddress"),
            "phonenumber": request.form.get("phonenumber"),
            "phonenumbertypeid": request.form.get("phonenumbertypeid"),
        }
        personCreateDto = PersonCreateDto(**new_data) 
        PersonService.create(personCreateDto)
        return redirect(url_for("person.findAllPaginated"))

    return render_template("person/create.html")