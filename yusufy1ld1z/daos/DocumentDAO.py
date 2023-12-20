from sqlalchemy import text
from flask.json import dumps
from models.Document import Document
from models.DocumentOwner import DocumentOwner
from db import db


class DocumentDAO:
    # @staticmethod
    # def encodeDocumentNode(value):
    #     components = value.strip("/").split("/")
    #     if components == [""]:
    #         return -1
    #     else:
    #         return int("".join(components))

    # @staticmethod
    # def decodeDocumentNode(value):
    #     if value == -1:
    #         return "/"
    #     components = [str(int(char)) for char in str(value)]
    #     return "/" + "/".join(components) + "/"

    @staticmethod
    def findAllDocuments():
        result = db.session.execute(text("SELECT * FROM production.document"))
        column_names = result.keys()
        documents = [
            Document(
                **dict(zip(column_names, row)),
            )
            for row in result.fetchall()
        ]
        return documents

    @staticmethod
    def findOwnerDetailsById(owner_id):
        result = db.session.execute(
            text(
                """SELECT 
                    p.firstname,
                    p.middlename,
                    p.lastname,
                    e.nationalidnumber, 
                    e.jobtitle, 
                    e.birthdate, 
                    e.gender, 
                    e.hiredate
                    FROM production.document d
                        LEFT JOIN humanresources.employee e ON d.owner = e.businessentityid
                        LEFT JOIN person.person p ON e.businessentityid = p.businessentityid
                        WHERE d.owner = :owner_id;"""
            ),
            {"owner_id": owner_id},
        )
        column_names = result.keys()
        owner_details = DocumentOwner(**dict(zip(column_names, result.fetchone())))
        return owner_details

    @staticmethod
    def findFileContentByNode(document_node):
        result = db.session.execute(
            text(
                "SELECT document, filename FROM production.document WHERE documentnode = :document_node"
            ),
            {"document_node": "/" + document_node},
        )
        (
            file_content,
            filename,
        ) = result.fetchone()  # Assuming 'document' is a LargeBinary field
        return {"file_content": file_content, "filename": filename}

    @staticmethod
    def addDocument(
        title,
        owner,
        folderflag,
        filename,
        fileextension,
        revision,
        changenumber,
        status,
        documentsummary,
        document,
        documentnode,
    ):
        sql = """
            INSERT INTO production.document (
                title, owner, folderflag, filename, fileextension,
                revision, changenumber, status, documentsummary, document, documentnode
            )
            VALUES (
                :title, :owner, :folderflag, :filename, :fileextension,
                :revision, :changenumber, :status, :documentsummary, :document, :documentnode
            )
        """

        params = {
            "title": title,
            "owner": int(owner),
            "folderflag": folderflag,
            "filename": filename,
            "fileextension": fileextension,
            "revision": revision,
            "changenumber": int(changenumber),
            "status": int(status),
            "documentsummary": documentsummary,
            "document": document,
            "documentnode": documentnode,
        }

        if folderflag:
            params["document"] = None
            params["documentsummary"] = None
            params["fileextension"] = ""
            params["filename"] = params["title"]
        else:
            params["folderflag"] = False

        db.session.execute(text(sql), params)
        db.session.commit()

    @staticmethod
    def getAllEmployees():
        result = db.session.execute(
            text(
                "SELECT businessentityid, firstname, middlename, lastname FROM person.person"
            )
        )
        column_names = result.keys()
        employees = [dict(zip(column_names, row)) for row in result.fetchall()]
        return employees

    @staticmethod
    def getExistingDocumentNodes():
        result = db.session.execute(
            text("SELECT documentnode FROM production.document")
        )
        column_names = result.keys()
        document_nodes = [row[0] for row in result.fetchall()]
        document_nodes_json = dumps(document_nodes)
        return document_nodes_json
