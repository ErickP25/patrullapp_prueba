from functools import wraps
from flask import Blueprint, request, jsonify
from ..models.vecino import Vecino
from ..models.db import db
from ..models.usuario import  Usuario
auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/api/registro', methods=['POST'])
def register_user():
    data = request.get_json()
    dni = data.get('dni')
    contraseña = data.get('contrasena')  # del front vendrá como 'contrasena'
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    telefono = data.get('telefono')
    direccion = data.get('direccion')

    if not dni or not contraseña:
        return jsonify({'error': 'DNI y contraseña son obligatorios'}), 400

    if Usuario.query.filter_by(dni=dni).first():
        return jsonify({'error': 'Ya existe un usuario con ese DNI'}), 409

    nuevo_usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        telefono=telefono,
        direccion=direccion,
        tipo_usuario=False
    )
    nuevo_usuario.set_password(contraseña)
    db.session.add(nuevo_usuario)
    usuario = Usuario.query.filter_by(dni=dni).first()
    nuevo_vecino = Vecino(
        id_usuario=usuario.id_usuario,
        id_reputacion=1
    )
    db.session.add(nuevo_vecino)
    db.session.commit()

    return jsonify({'mensaje': 'Usuario registrado con éxito'}), 201




@auth_routes.route('/api/login', methods=['POST'])
def logearse():
    data = request.get_json()

    dni = data.get('dni')
    contraseña = data.get('contrasena')

    if not dni or not contraseña:
        return jsonify({'error': 'Faltan credenciales'}), 400

    usuario = Usuario.query.filter_by(dni=dni).first()

    if not usuario or not usuario.check_password(contraseña):
        return jsonify({'error': 'DNI o contraseña incorrectos'}), 401

    return jsonify({
        'mensaje': 'Login exitoso',
        'id_usuario': usuario.id_usuario,
        'nombre': usuario.nombre,
        'apellido': usuario.apellido,
        'tipo_usuario': usuario.tipo_usuario
    }), 200