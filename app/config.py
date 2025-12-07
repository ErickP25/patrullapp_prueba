class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost/PatrullAPP'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'clave-secreta'