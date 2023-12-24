from daos.PersonDAO import PersonDAO


class PersonService:
    @staticmethod
    def findAllPaginated(page, per_page):
        return PersonDAO.findAllPaginated(page=page, per_page=per_page)

    @staticmethod
    def findDetailsById(id):
        return PersonDAO.findDetailsById(id)

    @staticmethod
    def updateDetailsById(id, personDetails):
        return PersonDAO.updateDetailsById(id, personDetails)

    @staticmethod
    def create(personCreateDto):
        return PersonDAO.create(personCreateDto)