from db import db


# Base class for database entities providing common functionality
class BaseEntity(db.Model):
    # Flag to indicate that this class is abstract and should not be mapped to a database table
    __abstract__ = True

    # Method to convert the entity to a dictionary representation
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
