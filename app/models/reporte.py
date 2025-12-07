from .db import db
from .vecino import Vecino
from .sereno import Sereno
from .incidente import Incidente
from .zona import Zona
from .estadoreporte import EstadoReporte

class Reporte(db.Model):
    __tablename__ = 'reporte'

    id_reporte = db.Column(db.Integer, primary_key=True)
    id_vecino = db.Column(db.Integer, db.ForeignKey('vecino.id_usuario'))
    id_sereno = db.Column(db.Integer, db.ForeignKey('sereno.id_usuario'))
    id_incidente = db.Column(db.Integer, db.ForeignKey('incidente.id_incidente'))
    id_zona = db.Column(db.Integer, db.ForeignKey('zona.id_zona'))
    id_estado = db.Column(db.Integer, db.ForeignKey('estado_reporte.id_estado'))

    fecha = db.Column(db.Date)
    hora = db.Column(db.Time)
    direccion = db.Column(db.Text)
    longitud = db.Column(db.Float)
    latitud = db.Column(db.Float)
    descripcion = db.Column(db.Text)
    evidencia = db.Column(db.Boolean)
    emergencia = db.Column(db.Boolean)

    vecino = db.relationship('Vecino', backref='reportes')
    sereno = db.relationship('Sereno', backref='reportes')
    incidente = db.relationship('Incidente', backref='reportes')
    zona = db.relationship('Zona', backref='reportes')
    estadoreporte = db.relationship('EstadoReporte', backref='reportes')
