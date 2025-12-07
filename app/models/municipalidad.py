from .db import db
from .distrito import Distrito
class Municipalidad(db.Model):
    __tablename__ = 'municipalidad'

    id_municipalidad = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    id_distrito = db.Column(db.Integer, db.ForeignKey('distrito.id_distrito'), nullable=False)

    distrito = db.relationship('Distrito', backref=db.backref('municipalidades', lazy=True))
