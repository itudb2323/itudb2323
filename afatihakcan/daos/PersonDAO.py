from sqlalchemy import text
from models.Person import Person
from db import db


class PersonDAO:
    @staticmethod
    def findAll():
        result = db.session.execute(text("SELECT * FROM person.person"))
        column_names = result.keys()
        persons = [Person(**dict(zip(column_names, row))) for row in result.fetchall()]
        return persons
