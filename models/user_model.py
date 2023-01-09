from app import db


# Creating Database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(28), nullable=False, unique=True)
    password = db.Column(db.String(28), nullable=False)
    __tablename__ = 'user'

    def __int__(self, username, password):
        self.username = username
        self.password = password


# Creating Database for api


