from sqlalchemy import String, Column, Integer

from models.base import Base


# Creating Database
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(28), nullable=False, unique=True)
    password = Column(String(28), nullable=False)

    def __int__(self, username, password):
        self.username = username
        self.password = password
