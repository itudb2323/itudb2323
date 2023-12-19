from flask import Blueprint, render_template, url_for, send_file
from services.DocumentService import DocumentService
import io

document_bp = Blueprint(name="document", import_name=__name__, url_prefix="/document")


@document_bp.route("/", methods=["GET"])
def showBase():
    return render_template("base.html")


@document_bp.route("/download/<int:document_node>", methods=["GET"])
def downloadFile(document_node):
    # Fetch file content and filename from the database
    result = DocumentService.findFileContentByNode(document_node)
    file_content = result.get("file_content")
    filename = result.get("filename")

    file_bytes = bytes.fromhex(file_content.tobytes().decode("utf-8"))

    if file_content is None:
        # Handle the case where the file content is not found
        return "File not found", 404

    # Send the file in the response with appropriate headers
    return send_file(
        io.BytesIO(file_bytes),
        mimetype="application/octet-stream",
        as_attachment=True,
        download_name=filename,
    )


@document_bp.route("/all_documents", methods=["GET"])
def findAllDocuments():
    documents = DocumentService.findAllDocuments()
    return render_template("document/document.html", documents=documents)


@document_bp.route("/owner_details/<int:owner_id>", methods=["GET"])
def findOwnerDetailsById(owner_id):
    owner_details = DocumentService.findOwnerDetailsById(owner_id)
    return render_template("document/details.html", owner_details=owner_details)
