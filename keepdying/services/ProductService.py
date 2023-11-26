from keepdying.daos.ProductDAO import ProductDAO


class ProductService:
    @staticmethod
    def findAll():
        return ProductDAO.findAll()
