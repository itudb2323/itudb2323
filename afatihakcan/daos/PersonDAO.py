from sqlalchemy import text
from models.Person import Person
from models.PersonDetails import PersonDetails
from db import db


class PersonDAO:
    @staticmethod
    def findAll():
        result = db.session.execute(text("SELECT * FROM person.person limit 10;"))
        column_names = result.keys()
        persons = [Person(**dict(zip(column_names, row))) for row in result.fetchall()]
        return persons

    @staticmethod
    def findDetailsById(id):
        result = db.session.execute(
            text(
                """select 
                    p.*,
                    ea.emailaddress as emailaddress, 
                    pp.phonenumber as phonenumber, 
                    concat(a.addressline1, ' ', a.addressline2) as address, 
                    a.city as city, 
                    a.postalcode as postalcode, 
                    sp.name as state
                    from person.person p 
                        left join person.personphone pp on p.businessentityid = pp.businessentityid
                        left join person.emailaddress ea on p.businessentityid = ea.businessentityid
                        left join person.businessentityaddress bea on p.businessentityid = bea.businessentityid
                        left join person.address a on bea.addressid = a.addressid
                        left join person.stateprovince sp on a.stateprovinceid = sp.stateprovinceid
                        where p.businessentityid = :id;"""
            ),
            {"id": id},
        )
        column_names = result.keys()
        personDetails = PersonDetails(**dict(zip(column_names, result.fetchone())))
        return personDetails
