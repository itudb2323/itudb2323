from daos.PersonDAO import PersonDAO


class PersonService:
    @staticmethod
    def findAll():
        return PersonDAO.findAll()
