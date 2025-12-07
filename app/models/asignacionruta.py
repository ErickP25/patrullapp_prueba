from .db import db
from .ruta import Ruta
from .sereno import Sereno

class AsignacionRuta(db.Model):
    __tablename__ = 'asignacion_ruta'

    id_asignacion = db.Column(db.Integer, primary_key=True)
    id_ruta = db.Column(db.Integer, db.ForeignKey('ruta.id_ruta'))
    id_sereno = db.Column(db.Integer, db.ForeignKey('sereno.id_usuario'))
    fecha_asignacion = db.Column(db.Date)
    estado = db.Column(db.String(50))
    hora_inicio = db.Column(db.Time)
    hora_fin = db.Column(db.Time)
    cant_incidentes = db.Column(db.Integer)

    ruta = db.relationship('Ruta', backref='asignaciones')
    sereno = db.relationship('Sereno', backref='asignaciones')
