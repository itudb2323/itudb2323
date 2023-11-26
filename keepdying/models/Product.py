from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, CHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from models.BaseEntity import BaseEntity
from dataclasses import dataclass


@dataclass
class Person(BaseEntity):
    __tablename__ = "product"
    __table_args__ = {"schema": "product"}
    # TODO: Add your columns here

    
