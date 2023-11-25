from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, CHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from models.BaseEntity import BaseEntity
from dataclasses import dataclass


@dataclass
class Person(BaseEntity):
    __tablename__ = "person"
    __table_args__ = {"schema": "person"}

    businessentityid = Column(Integer, primary_key=True)
    persontype = Column(CHAR(2), nullable=False)
    namestyle = Column(Boolean, default=False, nullable=False)
    title = Column(String(8))
    firstname = Column(String, nullable=False)
    middlename = Column(String)
    lastname = Column(String, nullable=False)
    suffix = Column(String(10))
    emailpromotion = Column(Integer, default=0, nullable=False)
    additionalcontactinfo = Column(Text)
    demographics = Column(Text)
    rowguid = Column(
        UUID(as_uuid=True), default=func.uuid_generate_v1(), nullable=False
    )
    modifieddate = Column(DateTime, default=func.now(), nullable=False)
