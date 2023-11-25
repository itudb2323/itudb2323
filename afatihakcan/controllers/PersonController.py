from flask import Blueprint, jsonify
from services.PersonService import PersonService

person_bp = Blueprint(name="/person", import_name=__name__, url_prefix="/person")


@person_bp.route("/", methods=["GET"])
def findAll():
    persons = PersonService.findAll()
    persons_list = [person.to_dict() for person in persons]
    return jsonify(persons_list)
