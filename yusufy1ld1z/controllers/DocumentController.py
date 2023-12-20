from flask import Blueprint, render_template, url_for, send_file, redirect, request
from services.DocumentService import DocumentService
import io

document_bp = Blueprint(name="document", import_name=__name__, url_prefix="/document")


@document_bp.route("/", methods=["GET"])
def showBase():
    return render_template("base.html")


@document_bp.route("/download/<path:document_node>", methods=["GET"])
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


@document_bp.route("/all_documents/add_new", methods=["GET", "POST"])
def showAddDocumentForm():
    if request.method == "GET":
        employees = DocumentService.getAllEmployees()
        existing_document_nodes = DocumentService.getExistingDocumentNodes()
        print(existing_document_nodes)
        return render_template(
            "document/addition.html",
            employees=employees,
            existing_document_nodes=existing_document_nodes,
        )
    elif request.method == "POST":
        # Get form data from the request
        title = request.form.get("title")
        owner = request.form.get("owner")
        folderflag = request.form.get("folderflag")
        filename = request.form.get("filename")
        fileextension = request.form.get("fileextension")
        revision = request.form.get("revision")
        changenumber = request.form.get("changenumber")
        status = request.form.get("status")
        documentsummary = request.form.get("documentsummary")
        document = request.form.get("document")
        documentnode = request.form.get("documentnode")

        # Call the addDocument function with the form data
        DocumentService.addDocument(
            title=title,
            owner=owner,
            folderflag=folderflag,
            filename=filename,
            fileextension=fileextension,
            revision=revision,
            changenumber=changenumber,
            status=status,
            documentsummary=documentsummary,
            document=document,
            documentnode=documentnode,
        )
        # Redirect to the document list page or another appropriate page
        return redirect(url_for("document.findAllDocuments"))
