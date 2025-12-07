from .db import db
from geoalchemy2 import Geometry
from .municipalidad import Municipalidad

class Zona(db.Model):
    __tablename__ = 'zona'

    id_zona = db.Column(db.Integer, primary_key=True)
    id_municipalidad = db.Column(db.Integer, db.ForeignKey('municipalidad.id_municipalidad'))
    nombre = db.Column(db.String(100))
    cant_incidentes = db.Column(db.Integer)
    nivel_riesgo = db.Column(db.String(50))
    tipo_zona = db.Column(db.String(50))
    geom = db.Column(Geometry(geometry_type='POLYGON', srid=4326))

    municipalidad = db.relationship('Municipalidad', backref='zonas')

