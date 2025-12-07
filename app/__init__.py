from flask import Flask
from .config import Config
from .models.db import db
from .routes.auth_routes import auth_routes
from .routes.incidente_routes import incidente_bp
from .routes.pantalla_tu_zona import tuzona_bp
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Base de datos
    db.init_app(app)

    CORS(app)
    # Registro de rutas
    app.register_blueprint(auth_routes)
    app.register_blueprint(incidente_bp)
    app.register_blueprint(tuzona_bp)

    return app
