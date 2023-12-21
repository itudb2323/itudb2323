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
    def findDocumentByNode(document_node):
        return DocumentDAO.findDocumentByNode(document_node)

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
    def deleteDocument(documentnode):
        return DocumentDAO.deleteDocument(documentnode)

    @staticmethod
    def updateDocument(
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
        new_documentnode,
        old_documentnode,
        isfilechanged,
    ):
        return DocumentDAO.updateDocument(
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
            new_documentnode,
            old_documentnode,
            isfilechanged,
        )

    @staticmethod
    def getAllEmployees():
        return DocumentDAO.getAllEmployees()

    @staticmethod
    def getExistingDocumentNodes():
        return DocumentDAO.getExistingDocumentNodes()
