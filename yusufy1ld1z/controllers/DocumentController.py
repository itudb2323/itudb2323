from flask import Blueprint, jsonify
from services.DocumentService import DocumentService

document_bp = Blueprint(name="/document", import_name=__name__, url_prefix="/document")


@document_bp.route("/", methods=["GET"])
def findAll():
    documents = DocumentService.findAll()
    documents_list = [doc.to_dict() for doc in documents]
    return jsonify(documents_list)
