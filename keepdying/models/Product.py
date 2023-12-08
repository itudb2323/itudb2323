from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, CHAR, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from models.BaseEntity import BaseEntity
from dataclasses import dataclass


@dataclass
class Product(BaseEntity):
    __tablename__ = "product"
    __table_args__ = {"schema": "product"}
    productid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    productnumber = Column(String, nullable=False)
    makeflag = Column(Boolean, default=False, nullable=False)
    finishedgoodsflag = Column(Boolean, default=False, nullable=False)
    color = Column(String)
    safetystocklevel = Column(Integer, nullable=False)
    reorderpoint = Column(Integer, nullable=False)
    standardcost = Column(Integer, nullable=False)
    listprice = Column(Integer, nullable=False)
    size = Column(String)
    sizeunitmeasurecode = Column(String)
    weightunitmeasurecode = Column(String)
    weight = Column(Integer)
    daystomanufacture = Column(Integer, nullable=False)
    productline = Column(String)
    class_ = Column(String)
    style = Column(String)
    productsubcategoryid = Column(Integer)
    productmodelid = Column(Integer)
    sellstartdate = Column(DateTime, nullable=False)
    sellenddate = Column(DateTime)
    discontinueddate = Column(DateTime)
    rowguid = Column(
        UUID(as_uuid=True), default=func.uuid_generate_v1(), nullable=False
    )
    modifieddate = Column(DateTime, default=func.now(), nullable=False)
