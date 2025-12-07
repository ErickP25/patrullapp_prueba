from .db import db
from .usuario import Usuario
class Vecino(db.Model):
    __tablename__ = 'vecino'

    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), primary_key=True)
    id_reputacion = db.Column(db.Integer)

    usuario = db.relationship('Usuario', backref=db.backref('vecino', uselist=False))
