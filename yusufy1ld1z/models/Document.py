from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, CHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from models.BaseEntity import BaseEntity
from db import db
from dataclasses import dataclass


@dataclass
class Document(BaseEntity):
    __tablename__ = "document"

    title = db.Column(db.String(50), nullable=False)
    owner = db.Column(db.Integer, nullable=False)
    folderflag = db.Column(db.Boolean, nullable=False, default=False)
    filename = db.Column(db.String(400), nullable=False)
    fileextension = db.Column(db.String(8))
    revision = db.Column(db.String(5), nullable=False)
    changenumber = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.SmallInteger, nullable=False)
    documentsummary = db.Column(db.Text)
    document = db.Column(db.LargeBinary)
    rowguid = db.Column(db.String(36), nullable=False, unique=True)
    modifieddate = db.Column(db.DateTime, nullable=False, default=db.func.now())
    documentnode = db.Column(
        db.String(255), nullable=False, primary_key=True, default="/"
    )

    def __init__(
        self,
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
        rowguid,
        modifieddate,
        documentnode,
    ):
        self.title = title
        self.owner = owner
        self.folderflag = folderflag
        self.filename = filename
        self.fileextension = fileextension
        self.revision = revision
        self.changenumber = changenumber
        self.status = status
        self.documentsummary = documentsummary
        self.document = document
        self.rowguid = rowguid
        self.modifieddate = modifieddate
        self.documentnode = documentnode
