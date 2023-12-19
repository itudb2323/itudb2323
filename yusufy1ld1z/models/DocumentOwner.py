from sqlalchemy import (
    Column,
    String,
    DateTime,
    Date,
)
from models.BaseEntity import BaseEntity
from dataclasses import dataclass


@dataclass
class DocumentOwner(BaseEntity):
    __tablename__ = "document_owner"

    # from humanresources.employee
    nationalidnumber = Column(String(15), nullable=False, primary_key=True)
    jobtitle = Column(String(50), nullable=False)
    birthdate = Column(Date, nullable=False)
    gender = Column(String(1), nullable=False)
    hiredate = Column(Date, nullable=False)

    # from person.person
    firstname = Column(String, nullable=False)
    middlename = Column(String)
    lastname = Column(String, nullable=False)
