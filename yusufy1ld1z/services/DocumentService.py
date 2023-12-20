from daos.DocumentDAO import DocumentDAO


class DocumentService:
    # @staticmethod
    # def encodeDocumentNode(value):
    #     return DocumentDAO.encodeDocumentNode(value)

    # @staticmethod
    # def decodeDocumentNode(value):
    #     return DocumentDAO.decodeDocumentNode(value)

    @staticmethod
    def findAllDocuments():
        return DocumentDAO.findAllDocuments()

    @staticmethod
    def findOwnerDetailsById(owner_id):
        return DocumentDAO.findOwnerDetailsById(owner_id)

    @staticmethod
    def findFileContentByNode(document_node):
        return DocumentDAO.findFileContentByNode(document_node)

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
        return DocumentDAO.addDocument(
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
        )

    @staticmethod
    def getAllEmployees():
        return DocumentDAO.getAllEmployees()

    @staticmethod
    def getExistingDocumentNodes():
        return DocumentDAO.getExistingDocumentNodes()
