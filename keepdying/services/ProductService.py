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

    @staticmethod
    def create(**kwargs):
        return ProductDAO.create(**kwargs)
    
    @staticmethod
    def update(id, **kwargs):
        return ProductDAO.update(id, **kwargs)
    
    @staticmethod
    def delete(id):
        return ProductDAO.delete(id)