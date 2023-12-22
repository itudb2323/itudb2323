from math import ceil
from sqlalchemy import text
from uuid import uuid1
from datetime import datetime
from models.Product import Product
from models.ProductDetails import ProductDetails
from db import db


class ProductDAO:
    @staticmethod
    def find_all():
        result = db.session.execute(text("SELECT * FROM production.product"))
        column_names = result.keys()
        products = [
            Product(**dict(zip(column_names, row))) for row in result.fetchall()
        ]
        return products

    @staticmethod
    def find_all_paginated(page, per_page, sort_by="modifieddate", order="desc"):
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
    def find_details_by_id(id):
        result = db.session.execute(
            text(
                """SELECT 
                p.*,
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

    @staticmethod
    def create(**kwargs):
        product = Product(**kwargs)
        product.rowguid = uuid1()
        product.modifieddate = datetime.now()
        db.session.execute(
            text(
                """INSERT INTO production.product (
                    Name,
                    ProductNumber,
                    MakeFlag,
                    FinishedGoodsFlag,
                    Color,
                    SafetyStockLevel,
                    ReorderPoint,
                    StandardCost,
                    ListPrice,
                    Size,
                    SizeUnitMeasureCode,
                    WeightUnitMeasureCode,
                    Weight,
                    DaysToManufacture,
                    ProductLine,
                    Class_,
                    Style,
                    ProductSubcategoryID,
                    ProductModelID,
                    SellStartDate,
                    SellEndDate,
                    DiscontinuedDate,
                    RowGuid,
                    ModifiedDate
                ) VALUES (
                    :Name,
                    :ProductNumber,
                    :MakeFlag,
                    :FinishedGoodsFlag,
                    :Color,
                    :SafetyStockLevel,
                    :ReorderPoint,
                    :StandardCost,
                    :ListPrice,
                    :Size,
                    :SizeUnitMeasureCode,
                    :WeightUnitMeasureCode,
                    :Weight,
                    :DaysToManufacture,
                    :ProductLine,
                    :Class,
                    :Style,
                    :ProductSubcategoryID,
                    :ProductModelID,
                    :SellStartDate,
                    :SellEndDate,
                    :DiscontinuedDate,
                    :RowGuid,
                    :ModifiedDate
                );"""
            ),
            {
                "Name": product.name,
                "ProductNumber": product.productnumber,
                "MakeFlag": product.makeflag,
                "FinishedGoodsFlag": product.finishedgoodsflag,
                "Color": product.color,
                "SafetyStockLevel": product.safetystocklevel,
                "ReorderPoint": product.reorderpoint,
                "StandardCost": product.standardcost,
                "ListPrice": product.listprice,
                "Size": product.size,
                "SizeUnitMeasureCode": product.sizeunitmeasurecode,
                "WeightUnitMeasureCode": product.weightunitmeasurecode,
                "Weight": product.weight,
                "DaysToManufacture": product.daystomanufacture,
                "ProductLine": product.productline,
                "Class": product.class_,
                "Style": product.style,
                "ProductSubcategoryID": product.productsubcategoryid,
                "ProductModelID": product.productmodelid,
                "SellStartDate": product.sellstartdate,
                "SellEndDate": product.sellenddate,
                "DiscontinuedDate": product.discontinueddate,
                "RowGuid": product.rowguid,
                "ModifiedDate": product.modifieddate,
            },
        )
        # Return product id
        product.productid = db.session.execute(
            text(
                """SELECT ProductID
                   FROM production.product
                   WHERE Name = :Name AND RowGuid = :RowGuid;"""
            ),
            {
                "Name": product.name,
                "RowGuid": product.rowguid,
            },
        ).scalar()
        db.session.commit()
        return product
