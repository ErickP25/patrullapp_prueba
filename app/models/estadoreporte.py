from .db import db

class EstadoReporte(db.Model):
    __tablename__ = 'estado_reporte'

    id_estado = db.Column(db.Integer, primary_key=True)
    tipo_estado = db.Column(db.String(100), nullable=False)
