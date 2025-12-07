from .db import db
class Turno(db.Model):
    _tablename_ = 'turno'
    id_turno = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)

