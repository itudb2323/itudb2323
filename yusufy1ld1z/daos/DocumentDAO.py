from sqlalchemy import text
from models.Document import Document
from db import db


class DocumentDAO:
    # @staticmethod
    # def get_all_documents():
    #     return Document.query.all()

    # @staticmethod
    # def get_document_by_documentnode(documentnode):
    #     return Document.query.filter_by(documentnode=documentnode).first()

    # @staticmethod
    # def get_documents_by_status(status):
    #   return Document.query.filter_by(status=status).all()

    def findAll():
        result = db.session.execute(text("SELECT * FROM document.document"))
        column_names = result.keys()
        documents = [
            Document(**dict(zip(column_names, row))) for row in result.fetchall()
        ]
        return documents
