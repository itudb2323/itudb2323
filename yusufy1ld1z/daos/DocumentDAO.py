from sqlalchemy import text
from flask.json import dumps, loads
from models.Document import Document
from models.DocumentOwner import DocumentOwner
from db import db


# Class for Data Access Object (DAO) handling database operations for documents
class DocumentDAO:
    # Method to retrieve all documents from the database
    @staticmethod
    def findAllDocuments():
        # Execute SQL query to select all documents, ordered by documentnode
        result = db.session.execute(
            text("SELECT * FROM production.document ORDER BY documentnode")
        )
        column_names = result.keys()
        # Convert result set to a list of Document objects
        documents = [
            Document(
                **dict(zip(column_names, row)),
            )
            for row in result.fetchall()
        ]
        return documents

    # Method to search documents by title
    @staticmethod
    def findDocumentByTitle(search_title):
        # Using ILIKE for case-insensitive search, you can adjust this based on your database engine
        query = text(
            "SELECT * FROM production.document WHERE title ILIKE :search_title"
        )
        result = db.session.execute(query, {"search_title": f"%{search_title}%"})

        column_names = result.keys()

        # Convert result set to a list of Document objects
        documents = [
            Document(
                **dict(zip(column_names, row)),
            )
            for row in result.fetchall()
        ]
        return documents

    # Method to retrieve owner details by owner_id
    @staticmethod
    def findOwnerDetailsById(owner_id):
        # Execute SQL query to select owner details based on owner_id
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
        # Convert result set to a DocumentOwner object
        owner_details = DocumentOwner(**dict(zip(column_names, result.fetchone())))
        return owner_details

    # Method to retrieve a document by document_node
    @staticmethod
    def findDocumentByNode(document_node):
        # Execute SQL query to select a document based on document_node
        result = db.session.execute(
            text(
                "SELECT * FROM production.document WHERE documentnode = :document_node"
            ),
            {"document_node": "/" + document_node},
        )
        column_names = result.keys()
        # Convert result set to a Document object
        document = Document(**dict(zip(column_names, result.fetchone())))
        return document

    # Method to retrieve file content and filename by document_node
    @staticmethod
    def findFileContentByNode(document_node):
        # Execute SQL query to select document content and filename based on document_node
        result = db.session.execute(
            text(
                "SELECT document, filename FROM production.document WHERE documentnode = :document_node"
            ),
            {"document_node": "/" + document_node},
        )
        (
            file_content,
            filename,
        ) = result.fetchone()
        return {"file_content": file_content, "filename": filename}

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
        try:
            # SQL query to insert a new document
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

            # Parameters for the SQL query
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

            # Adjust parameters based on folderflag
            if folderflag:
                params["document"] = None
                params["documentsummary"] = None
                params["fileextension"] = ""
                params["filename"] = params["title"]
            else:
                params["folderflag"] = False

            # Execute SQL query and commit changes to the database
            db.session.execute(text(sql), params)
            db.session.commit()

        except Exception as e:
            # Handle exceptions and rollback changes if necessary
            db.session.rollback()
            print(f"Error updating document: {e}")

    # Method to delete a document from the database
    @staticmethod
    def deleteDocument(documentnode, addslash=True):
        try:
            # SQL query to delete foreign keys from the productdocument table
            proddocsql = """
                DELETE FROM production.productdocument
                WHERE documentnode = :documentnode
            """
            # Adjust documentnode based on addslash
            if addslash:
                params = {"documentnode": "/" + documentnode}
            else:
                params = {"documentnode": documentnode}

            # Execute SQL query and commit changes to the database
            db.session.execute(text(proddocsql), params)
            db.session.commit()

            # SQL query to delete the document from the document table
            docsql = """
                DELETE FROM production.document
                WHERE documentnode = :documentnode
            """
            # Adjust documentnode based on addslash
            if addslash:
                params = {"documentnode": "/" + documentnode}
            else:
                params = {"documentnode": documentnode}

            # Execute SQL query and commit changes to the database
            db.session.execute(text(docsql), params)
            db.session.commit()

        except Exception as e:
            # Handle exceptions and rollback changes if necessary
            db.session.rollback()
            print(f"Error deleting document: {e}")

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
        existing_nodes_json = DocumentDAO.getExistingDocumentNodes()
        existing_nodes = loads(existing_nodes_json)

        if new_documentnode in existing_nodes:
            print("Node already exists, so just updating the nodes!")
            try:
                if new_documentnode != old_documentnode:
                    # Step 1: Update the referenced foreign key values in productdocument table
                    db.session.execute(
                        text(
                            """
                            UPDATE production.productdocument
                            SET documentnode = :new_document_node
                            WHERE documentnode = :old_document_node
                        """
                        ),
                        {
                            "new_document_node": new_documentnode,
                            "old_document_node": old_documentnode,
                        },
                    )

                    # Commit the changes to the database
                    db.session.commit()
                if isfilechanged == "True":
                    sql = """
                        UPDATE production.document
                        SET
                            title = :title,
                            owner = :owner,
                            folderflag = :folderflag,
                            filename = :filename,
                            fileextension = :fileextension,
                            revision = :revision,
                            changenumber = :changenumber,
                            status = :status,
                            documentsummary = :documentsummary,
                            document = :document,
                            documentnode = :new_documentnode
                        WHERE documentnode = :old_documentnode
                    """
                else:
                    sql = """
                        UPDATE production.document
                        SET
                            title = :title,
                            owner = :owner,
                            folderflag = :folderflag,
                            filename = :filename,
                            fileextension = :fileextension,
                            revision = :revision,
                            changenumber = :changenumber,
                            status = :status,
                            documentsummary = :documentsummary,
                            documentnode = :new_documentnode
                        WHERE documentnode = :old_documentnode
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
                    "new_documentnode": new_documentnode,
                    "old_documentnode": old_documentnode,
                }
                if isfilechanged == "False":
                    del params["document"]

                if folderflag:
                    params["document"] = None
                    params["documentsummary"] = None
                    params["fileextension"] = ""
                    params["filename"] = params["title"]
                else:
                    params["folderflag"] = False

                # Execute SQL query and commit changes to the database
                db.session.execute(text(sql), params)
                db.session.commit()

            except Exception as e:
                # Handle exceptions and rollback changes if necessary
                db.session.rollback()
                print(f"Error updating document: {e}")

        else:
            print("Node does not exist, so adding a new node and updating the nodes!")
            try:
                # Step 1: Add a new row in the document table
                sql = """
                    INSERT INTO production.document (
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
                        documentnode
                    )
                    SELECT
                        :title,
                        :owner,
                        :folderflag,
                        :filename,
                        :fileextension,
                        :revision,
                        :changenumber,
                        :status,
                        :documentsummary,
                        document,  -- Copy the 'document' column from the existing row
                        :new_documentnode
                    FROM production.document
                    WHERE documentnode = :old_documentnode
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
                    "new_documentnode": new_documentnode,
                    "old_documentnode": old_documentnode,
                }

                if folderflag:
                    params["document"] = None
                    params["documentsummary"] = None
                    params["fileextension"] = ""
                    params["filename"] = params["title"]
                else:
                    params["folderflag"] = False

                # Execute SQL query and commit changes to the database
                db.session.execute(text(sql), params)
                db.session.commit()

                # Step 2: Update the referenced foreign key values in productdocument table
                db.session.execute(
                    text(
                        """
                        UPDATE production.productdocument
                        SET documentnode = :new_document_node
                        WHERE documentnode = :old_document_node
                    """
                    ),
                    {
                        "new_document_node": new_documentnode,
                        "old_document_node": old_documentnode,
                    },
                )

                # Commit the changes to the database
                db.session.commit()

            except Exception as e:
                # Handle exceptions and rollback changes if necessary
                db.session.rollback()
                print(f"Error updating document: {e}")

            # Step 3: Delete the old row from the document table
            DocumentDAO.deleteDocument(old_documentnode, addslash=False)

    # Method to retrieve details of all employees
    @staticmethod
    def getAllEmployees():
        # Execute SQL query to select employee details
        result = db.session.execute(
            text(
                "SELECT businessentityid, firstname, middlename, lastname FROM person.person"
            )
        )
        column_names = result.keys()
        # Convert result set to a list of dictionaries
        employees = [dict(zip(column_names, row)) for row in result.fetchall()]
        return employees

    # Method to retrieve existing document nodes
    @staticmethod
    def getExistingDocumentNodes():
        # Execute SQL query to select existing document nodes
        result = db.session.execute(
            text("SELECT documentnode FROM production.document")
        )
        column_names = result.keys()
        # Convert result set to a JSON string
        document_nodes = [row[0] for row in result.fetchall()]
        document_nodes_json = dumps(document_nodes)
        return document_nodes_json
