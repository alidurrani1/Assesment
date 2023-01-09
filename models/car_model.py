from app import db

class Car(db.Model):
    id = db.Column(db.String(30), primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    make = db.Column(db.String(28), nullable=False)
    created_at = db.Column(db.String(60), nullable=False)
    updated_at = db.Column(db.String(60), nullable=False)
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