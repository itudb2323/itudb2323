from daos.ProductDAO import ProductDAO


class ProductService:
    @staticmethod
    def findAll():
        return ProductDAO.findAll()
    
    @staticmethod
    def findAllPaginated(page, per_page, sort_by, order):
        return ProductDAO.findAllPaginated(page, per_page, sort_by, order)
