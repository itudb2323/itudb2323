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
                    pp.phonenumber as phonenumber
                    from person.person p 
                        left join person.personphone pp on p.businessentityid = pp.businessentityid
                        left join person.emailaddress ea on p.businessentityid = ea.businessentityid
                        where p.businessentityid = :id;"""
            ),
            {"id": id},
        )
        column_names = result.keys()
        personDetails = PersonDetails(**dict(zip(column_names, result.fetchone())))
        return personDetails

    @staticmethod
    def updateDetailsById(id, personDetails):
        print(personDetails)
        try:
            with db.session.begin_nested():
                db.session.execute(
                    text(
                        """update person.person 
                            set firstname = :firstname, 
                                middlename = :middlename, 
                                lastname = :lastname, 
                                modifieddate = now() 
                            where businessentityid = :id;"""
                    ),
                    {
                        "id": id,
                        "firstname": personDetails.firstname,
                        "middlename": personDetails.middlename,
                        "lastname": personDetails.lastname,
                    },
                )
                db.session.execute(
                    text(
                        """update person.personphone 
                            set phonenumber = :phonenumber, 
                                modifieddate = now() 
                            where businessentityid = :id;"""
                    ),
                    {"id": id, "phonenumber": personDetails.phonenumber},
                )
                db.session.execute(
                    text(
                        """update person.emailaddress 
                            set emailaddress = :emailaddress, 
                                modifieddate = now() 
                            where businessentityid = :id;"""
                    ),
                    {"id": id, "emailaddress": personDetails.emailaddress},
                )
                db.session.commit()
        except:
            db.session.rollback()
            raise

    @staticmethod
    def create(personCreateDto):
        businessentityid = db.session.execute(
            text("""select max(businessentityid) + 1 from person.businessentity""")
        ).scalar()

        try:
            with db.session.begin_nested():
                db.session.execute(
                    text(
                        """insert into person.businessentity (businessentityid, rowguid, modifieddate)
                        values (:businessentityid, uuid_generate_v1(), now())"""
                    ),
                    {"businessentityid": businessentityid},
                )

                db.session.execute(
                    text(
                        """insert into person.person (businessentityid, persontype, firstname, middlename, lastname, modifieddate) 
                            values (:businessentityid, :persontype, :firstname, :middlename, :lastname, now());"""
                    ),
                    {
                        "businessentityid": businessentityid,
                        "persontype": personCreateDto.persontype,
                        "firstname": personCreateDto.firstname,
                        "middlename": personCreateDto.middlename,
                        "lastname": personCreateDto.lastname,
                    },
                )
                db.session.execute(
                    text(
                        """insert into person.personphone (businessentityid, phonenumber, phonenumbertypeid, modifieddate) 
                            values (:businessentityid, :phonenumber, :phonenumbertypeid, now());"""
                    ),
                    {
                        "businessentityid": businessentityid,
                        "phonenumbertypeid": personCreateDto.phonenumbertypeid,
                        "phonenumber": personCreateDto.phonenumber},
                )
                db.session.execute(
                    text(
                        """insert into person.emailaddress (businessentityid, emailaddress, modifieddate) 
                            values (:businessentityid, :emailaddress, now());"""
                    ),
                    {
                        "businessentityid": businessentityid,
                        "emailaddress": personCreateDto.emailaddress},
                )
                db.session.commit()
        except:
            db.session.rollback()
            raise
