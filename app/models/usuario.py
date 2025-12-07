from .db import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    dni = db.Column(db.String(20))
    telefono = db.Column(db.String(20))
    contraseña = db.Column(db.Text)
    direccion = db.Column(db.Text)
    tipo_usuario = db.Column(db.Boolean)
    uid_firebase = db.Column(db.Text)


    def set_password(self, password):
        self.contraseña = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contraseña, password)