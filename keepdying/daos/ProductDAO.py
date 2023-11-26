from sqlalchemy import text
from models.Product import Product
from db import db


class ProductDAO:
    @staticmethod
    def findAll():
        result = db.session.execute(text("SELECT * FROM product.product"))
        column_names = result.keys()
        products = [Product(**dict(zip(column_names, row))) for row in result.fetchall()]
        return products
