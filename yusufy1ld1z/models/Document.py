from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    SmallInteger,
    Text,
    LargeBinary,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from models.BaseEntity import BaseEntity
from dataclasses import dataclass


# Define a data class 'Document' representing a database entity
@dataclass
class Document(BaseEntity):
    # Database table name and schema
    __tablename__ = "document"
    __table_args__ = {"schema": "production"}

    # Define columns with their respective data types and constraints
    title = Column(String(50), nullable=False)
    owner = Column(Integer, nullable=False)
    folderflag = Column(Boolean, nullable=False, default=False)
    filename = Column(String(400), nullable=False)
    fileextension = Column(String(8))
    revision = Column(String(5), nullable=False)
    changenumber = Column(Integer, nullable=False, default=0)
    status = Column(SmallInteger, nullable=False)
    documentsummary = Column(Text)
    document = Column(LargeBinary)
    rowguid = Column(
        UUID(as_uuid=True), default=func.uuid_generate_v1(), nullable=False
    )
    modifieddate = Column(DateTime, nullable=False, default=func.now())
    documentnode = Column(String(50), nullable=False, primary_key=True, default="/")
