from sqlalchemy import Column, String, DateTime, Date
from models.BaseEntity import BaseEntity
from dataclasses import dataclass


# Define a data class 'DocumentOwner' representing the owner of document's details
@dataclass
class DocumentOwner(BaseEntity):
    # Database table name
    __tablename__ = "document_owner"

    # Columns with their respective data types and constraints
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
