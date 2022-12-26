from app import db


# Creating Database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(28), nullable=False, unique=True)
    password = db.Column(db.String(28), nullable=False)


# Creating Database for api


class Car(db.Model):
    id = db.Column(db.String(30), primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    make = db.Column(db.String(28), nullable=False)
    created_at = db.Column(db.String(60), nullable=False)
    updated_at = db.Column(db.String(60), nullable=False)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
