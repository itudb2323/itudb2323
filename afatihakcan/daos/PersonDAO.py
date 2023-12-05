from math import ceil
from sqlalchemy import text
from models.Person import Person
from models.PersonDetails import PersonDetails
from db import db


class PersonDAO:
    @staticmethod
    def findAllPaginated(page, per_page):
        result = db.session.execute(
            text(
                """SELECT * 
                    FROM person.person 
                    limit :limit 
                    offset :offset;"""
            ),
            {"limit": per_page, "offset": (page - 1) * per_page},
        )
        column_names = result.keys()
        persons = [Person(**dict(zip(column_names, row))) for row in result.fetchall()]

        total_records = db.session.execute(
            text(
                """SELECT count(*) 
                    FROM person.person;"""
            )
        ).scalar()
        pagination = {
            "page": page,
            "per_page": per_page,
            "total_pages": ceil(total_records / per_page),
            "total_records": total_records,
        }
        return pagination,persons

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
