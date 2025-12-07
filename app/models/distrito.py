from .db import db

class Distrito(db.Model):
    __tablename__ = 'distrito'

    id_distrito = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)


