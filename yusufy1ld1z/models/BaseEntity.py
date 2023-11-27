from db import db


class BaseEntity(db.Model):
    __abstract__ = True
