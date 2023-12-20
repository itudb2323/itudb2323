from math import ceil
from sqlalchemy import text
from models.Product import Product
from models.ProductDetails import ProductDetails
from db import db


class ProductDAO:
    @staticmethod
    def findAll():
        result = db.session.execute(text("SELECT * FROM production.product"))
        column_names = result.keys()
        products = [
            Product(**dict(zip(column_names, row))) for row in result.fetchall()
        ]
        return products

    @staticmethod
    def findAllPaginated(page, per_page, sort_by="modifieddate", order="desc"):
        result = db.session.execute(
            text(
                f"""SELECT * 
                   FROM production.product
                   ORDER BY {sort_by} {order}
                   LIMIT :limit
                   OFFSET :offset;"""
            ),
            {
                "limit": per_page,
                "offset": (page - 1) * per_page,
            },
        )
        column_names = result.keys()
        products = [
            Product(**dict(zip(column_names, row))) for row in result.fetchall()
        ]

        total_records = db.session.execute(
            text(
                """SELECT COUNT(*) 
                   FROM production.product;"""
            )
        ).scalar()
        pagination = {
            "page": page,
            "per_page": per_page,
            "total_pages": ceil(total_records / per_page),
            "total_records": total_records,
        }
        return pagination, products

    @staticmethod
    def findDetailsById(id):
        result = db.session.execute(
            text(
                """SELECT 
                p.ProductID,
                p.Name,
                p.ProductNumber,
                p.Color,
                p.StandardCost,
                p.ListPrice,
                pr.ReviewID,
                pr.ReviewerName,
                pr.ReviewDate,
                pr.Rating,
                pph.ProductPhotoID,
                th.Quantity,
                th.TransactionDate
            FROM Production.Product p
                LEFT JOIN Production.ProductReview pr ON p.ProductID = pr.ProductID
                LEFT JOIN Production.ProductProductPhoto ppp ON p.ProductID = ppp.ProductID
                LEFT JOIN Production.ProductPhoto pph ON ppp.ProductPhotoID = pph.ProductPhotoID
                LEFT JOIN Production.TransactionHistory th ON p.ProductID = th.ProductID
            WHERE 
                p.ProductID = :id;"""
            ),
            {"id": id},
        )
        column_names = result.keys()
        productDetails = ProductDetails(**dict(zip(column_names, result.fetchone())))
        return productDetails
