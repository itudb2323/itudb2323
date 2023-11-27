from daos.DocumentDAO import DocumentDAO


class DocumentService:
    @staticmethod
    def findAll():
        return DocumentDAO.get_all_documents()
