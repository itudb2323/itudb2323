from daos.DocumentDAO import DocumentDAO


# Service class providing an abstraction layer for business logic related to documents
class DocumentService:
    # Method to retrieve all documents
    @staticmethod
    def findAllDocuments():
        return DocumentDAO.findAllDocuments()

    # Method to retrieve owner details by owner_id
    @staticmethod
    def findOwnerDetailsById(owner_id):
        return DocumentDAO.findOwnerDetailsById(owner_id)

    # Method to retrieve a document by document_node
    @staticmethod
    def findDocumentByNode(document_node):
        return DocumentDAO.findDocumentByNode(document_node)

    # Method to search documents by title
    @staticmethod
    def findDocumentByTitle(search_title):
        return DocumentDAO.findDocumentByTitle(search_title)

    # Method to retrieve file content and filename by document_node
    @staticmethod
    def findFileContentByNode(document_node):
        return DocumentDAO.findFileContentByNode(document_node)

    # Method to add a new document to the database
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

    # Method to delete a document from the database
    @staticmethod
    def deleteDocument(documentnode):
        return DocumentDAO.deleteDocument(documentnode)

    # Method to update a document in the database
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

    # Method to retrieve details of all employees
    @staticmethod
    def getAllEmployees():
        return DocumentDAO.getAllEmployees()

    # Method to retrieve existing document nodes
    @staticmethod
    def getExistingDocumentNodes():
        return DocumentDAO.getExistingDocumentNodes()
