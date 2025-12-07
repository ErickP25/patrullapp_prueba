from .db import db
from .zona import Zona

class Ruta(db.Model):
    __tablename__ = 'ruta'

    id_ruta = db.Column(db.Integer, primary_key=True)
    id_zona = db.Column(db.Integer, db.ForeignKey('zona.id_zona'))
    latitud_inicio = db.Column(db.Float)
    longitud_inicio = db.Column(db.Float)
    latitud_fin = db.Column(db.Float)
    longitud_fin = db.Column(db.Float)

    zona = db.relationship('Zona', backref='rutas')
