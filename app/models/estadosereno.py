from .db import db

class EstadoSereno(db.Model):
    __tablename__ = 'estado_sereno'

    id_estado = db.Column(db.Integer, primary_key=True)
    tipo_estado = db.Column(db.String(50), nullable=False)
