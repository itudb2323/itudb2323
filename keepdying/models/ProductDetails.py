from sqlalchemy import Column, Integer, String, DateTime, Float
from models.Product import Product
from datetime import datetime
from dataclasses import dataclass

@dataclass
class ProductDetails(Product):
    # Fields from ProductReview
    reviewid: int = Column(Integer, nullable=True)
    reviewername: str = Column(String, nullable=True)
    reviewdate: datetime = Column(DateTime, nullable=True)
    rating: int = Column(Integer, nullable=True)

    # Field from ProductPhoto (through ProductProductPhoto)
    productphotoid: int = Column(Integer, nullable=True)

    # Fields from TransactionHistory
    quantity: int = Column(Integer, nullable=True)
    transactiondate: datetime = Column(DateTime, nullable=True)
