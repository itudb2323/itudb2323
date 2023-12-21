from daos.ProductDAO import ProductDAO


class ProductService:
    @staticmethod
    def find_all():
        return ProductDAO.find_all()

    @staticmethod
    def find_all_paginated(page, per_page, sort_by, order):
        return ProductDAO.find_all_paginated(page, per_page, sort_by, order)

    @staticmethod
    def find_details_by_id(id):
        return ProductDAO.find_details_by_id(id)
