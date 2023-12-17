from sqlalchemy import Column, Integer, String, DateTime, Float
from models.Product import Product
from datetime import datetime
from dataclasses import dataclass

@dataclass
class ProductDetails(Product):
    # Fields from ProductReview
    ReviewID: int = Column(Integer, nullable=True)
    ReviewerName: str = Column(String, nullable=True)
    ReviewDate: datetime = Column(DateTime, nullable=True)
    Rating: int = Column(Integer, nullable=True)

    # Field from ProductPhoto (through ProductProductPhoto)
    ProductPhotoID: int = Column(Integer, nullable=True)

    # Fields from TransactionHistory
    Quantity: int = Column(Integer, nullable=True)
    TransactionDate: datetime = Column(DateTime, nullable=True)
