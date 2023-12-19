from sqlalchemy import text
from models.Document import Document
from models.DocumentOwner import DocumentOwner
from db import db


class DocumentDAO:
    @staticmethod
    def encodeDocumentNode(value):
        components = value.strip("/").split("/")
        if components == [""]:
            return -1
        else:
            return int("".join(components))

    @staticmethod
    def decodeDocumentNode(value):
        if value == -1:
            return "/"
        components = [str(int(char)) for char in str(value)]
        return "/" + "/".join(components) + "/"

    @staticmethod
    def findAllDocuments():
        result = db.session.execute(text("SELECT * FROM production.document"))
        column_names = result.keys()
        documents = [
            Document(
                **{
                    **dict(zip(column_names, row[:-1])),
                    "documentnode": DocumentDAO.encodeDocumentNode(row[-1]),
                }
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
            {"document_node": DocumentDAO.decodeDocumentNode(document_node)},
        )
        (
            file_content,
            filename,
        ) = result.fetchone()  # Assuming 'document' is a LargeBinary field
        return {"file_content": file_content, "filename": filename}
