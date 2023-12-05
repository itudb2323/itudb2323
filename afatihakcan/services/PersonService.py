from daos.PersonDAO import PersonDAO


class PersonService:
    @staticmethod
    def findAllPaginated(page, per_page):
        return PersonDAO.findAllPaginated(page=page, per_page=per_page)

    @staticmethod
    def findDetailsById(id):
        return PersonDAO.findDetailsById(id)
