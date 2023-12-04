from daos.PersonDAO import PersonDAO


class PersonService:
    @staticmethod
    def findAll():
        return PersonDAO.findAll()

    @staticmethod
    def findDetailsById(id):
        return PersonDAO.findDetailsById(id)