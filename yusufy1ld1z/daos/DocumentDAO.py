from sqlalchemy import text
from flask.json import dumps, loads
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
        result = db.session.execute(
            text("SELECT * FROM production.document ORDER BY documentnode")
        )
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
    def findDocumentByNode(document_node):
        result = db.session.execute(
            text(
                "SELECT * FROM production.document WHERE documentnode = :document_node"
            ),
            {"document_node": "/" + document_node},
        )
        column_names = result.keys()
        document = Document(**dict(zip(column_names, result.fetchone())))
        return document

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
        try:
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

        except Exception as e:
            # Handle exceptions and rollback changes if necessary
            db.session.rollback()
            print(f"Error updating document: {e}")

        # SQLAlchemy's session is typically managed by Flask, and it's a good practice to let Flask manage the session's lifecycle.

    @staticmethod
    def deleteDocument(documentnode, addslash=True):
        try:
            # first delete the foreign keys from productdocument table
            proddocsql = """
                DELETE FROM production.productdocument
                WHERE documentnode = :documentnode
            """
            if addslash:
                params = {"documentnode": "/" + documentnode}
            else:
                params = {"documentnode": documentnode}

            db.session.execute(text(proddocsql), params)

            db.session.commit()

            # then delete the document from document table
            docsql = """
                DELETE FROM production.document
                WHERE documentnode = :documentnode
            """
            if addslash:
                params = {"documentnode": "/" + documentnode}
            else:
                params = {"documentnode": documentnode}

            db.session.execute(text(docsql), params)

            db.session.commit()

        except Exception as e:
            # Handle exceptions and rollback changes if necessary
            db.session.rollback()
            print(f"Error deleting document: {e}")

        # SQLAlchemy's session is typically managed by Flask, and it's a good practice to let Flask manage the session's lifecycle.

    @staticmethod
    def updateDocument(  # TODO: Fix the document
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

                db.session.execute(text(sql), params)
                db.session.commit()

            except Exception as e:
                # Handle exceptions and rollback changes if necessary
                db.session.rollback()
                print(f"Error updating document: {e}")

            # SQLAlchemy's session is typically managed by Flask, and it's a good practice to let Flask manage the session's lifecycle.

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

            # SQLAlchemy's session is typically managed by Flask, and it's a good practice to let Flask manage the session's lifecycle.

            # Step 3: Delete the old row from the document table
            DocumentDAO.deleteDocument(old_documentnode, addslash=False)

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
