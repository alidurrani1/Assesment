from sqlalchemy.orm import declarative_base
from sqlalchemy import String, Column, Integer
from models.base import Base

class Car(Base):
    id = Column(String(30), primary_key=True)
    year = Column(Integer, nullable=False)
    make = Column(String(28), nullable=False)
    created_at = Column(String(60), nullable=False)
    updated_at = Column(String(60), nullable=False)
    __tablename__ = 'car'

    def __int__(self, id, year, make, created_at, updated_at):
        self.id = id
        self.year = year
        self.make = make
        self.created_at = created_at
        self.updated_at = updated_at
    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
