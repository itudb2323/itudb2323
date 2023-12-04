from dataclasses import dataclass
from sqlalchemy import Column, String
from models.Person import Person


@dataclass
class PersonDetails(Person):
    emailaddress = Column(String, nullable=True)
    phonenumber = Column(String, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    postalcode = Column(String, nullable=True)
    state = Column(String, nullable=True)
