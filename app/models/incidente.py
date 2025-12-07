from .db import db

class Incidente(db.Model):
    __tablename__ = 'incidente'

    id_incidente = db.Column(db.Integer, primary_key=True)
    tipo_incidente = db.Column(db.String(100), nullable=False)
    prioridad = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Incidente {self.id_incidente} - {self.tipo_incidente}>"

