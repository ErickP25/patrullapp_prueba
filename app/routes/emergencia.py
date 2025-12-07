import os
import threading
import uuid
import datetime
from flask import Blueprint, request, jsonify
from sqlalchemy import desc
from time import sleep
from ..models.asignacionruta import AsignacionRuta
from ..models.incidente import Incidente
from ..models.reporte import Reporte
from ..models.db import db
from ..controllers.openai_utils import transcribir_audio, extraer_info_con_gpt
from .pantalla_tu_zona import obtenerZonaPorCoordendas
from ..models.sereno import Sereno
from ..models.asignacionruta import AsignacionRuta
from ..models.ruta import Ruta
from math import sqrt

def distancia_perpendicular(punto, inicio, fin):
    x0, y0 = punto
    x1, y1 = inicio
    x2, y2 = fin

    num = abs((x2 - x1)*(y1 - y0) - (x1 - x0)*(y2 - y1))
    den = sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return num / den if den != 0 else float('inf')

def obtenerSerenoMasCercano(latitud, longitud):
    serenosDisponibles = Sereno.query.filter_by(id_estado = 1).all()
    punto_emergencia = (longitud, latitud)
    menor_distancia = 9999
    for sereno in serenosDisponibles:
        id_sereno = sereno.id_usuario

        # Buscar asignación de ruta para el sereno
        asignacion = AsignacionRuta.query.filter_by(id_sereno = id_sereno).order_by(desc(AsignacionRuta.fecha_asignacion)).first()
        if not asignacion:
            continue

        # Buscar datos de la ruta
        ruta = Ruta.query.filter_by(id_ruta = asignacion.id_ruta).first()
        if not ruta:
            continue

        inicio = (ruta.longitud_incio, ruta.latitud_inicio)
        fin = (ruta.longitud_fin, ruta.latitud_fin)

        distancia = distancia_perpendicular(punto_emergencia, inicio, fin)

        if distancia < menor_distancia:
            menor_distancia = distancia
            sereno_mas_cercano = sereno

    return sereno_mas_cercano


def monitorear_reporte(id_reporte):
    sleep(60)
    reporte = Reporte.query.get(id_reporte)

    if not reporte or reporte.id_estado != 1:  # Si ya fue aceptado
        return

    nuevo_sereno = obtenerSerenoMasCercano(reporte.latitud, reporte.longitud)
    if nuevo_sereno and nuevo_sereno.id_usuario != reporte.id_sereno:
        reporte.id_sereno = nuevo_sereno.id_usuario
        reporte.id_estado = 1
        db.session.commit()
        threading.Thread(target=monitorear_reporte, args=(id_reporte,)).start()

emergencia_bp = Blueprint('emergencia', __name__)

@emergencia_bp.route('/api/emergencia', methods=['POST'])
def crear_emergencia():
    data = request.get_json()
    lat = data.get('latitud')
    lon = data.get('longitud')
    direccion = data.get('direccion')

    if not lat or not lon or not direccion:
        return jsonify({'error': 'Faltan datos de ubicación'}), 400

    sereno = obtenerSerenoMasCercano(lat, lon)
    if not sereno:
        return jsonify({'error': 'No hay serenos disponibles'}), 503

    zona = obtenerZonaPorCoordendas(lat, lon)

    nuevo_reporte = Reporte(
        id_vecino=None,
        id_sereno=sereno.id_usuario,
        id_incidente=None,  # ID fijo para emergencias anónimas
        id_zona=zona.id_zona if zona else None,
        id_estado=1,  # Reportado
        fecha=datetime.date.today(),
        hora=datetime.now().time(),
        direccion=direccion,
        latitud=lat,
        longitud=lon,
        descripcion='Emergencia anónima',
        evidencia=False,
        emergencia=True
    )

    db.session.add(nuevo_reporte)
    db.session.commit()

    # Lanza la función para esperar 1 minuto
    threading.Thread(target=monitorear_reporte, args=(nuevo_reporte.id_reporte,)).start()

    return jsonify({'estado': 'enviado', 'id_reporte': nuevo_reporte.id_reporte}), 200

@emergencia_bp.route('/api/emergencia/aceptar', methods=['POST'])
def aceptar_reporte():
    data = request.get_json()
    id_reporte = data.get('id_reporte')
    id_sereno = data.get('id_sereno')

    reporte = Reporte.query.get(id_reporte)

    if not reporte or reporte.id_sereno != int(id_sereno):
        return jsonify({'error': 'No autorizado para aceptar este reporte'}), 403

    if reporte.id_estado != 1:
        return jsonify({'mensaje': 'Este reporte ya fue gestionado'}), 200

    reporte.id_estado = 2  # Aceptado
    db.session.commit()

    return jsonify({'mensaje': 'Emergencia aceptada'}), 200

@emergencia_bp.route('/api/emergencia/estado/<int:id_reporte>', methods=['GET'])
def estado_reporte(id_reporte):
    reporte = Reporte.query.get(id_reporte)
    if not reporte:
        return jsonify({'error': 'Reporte no encontrado'}), 404

    return jsonify({
        'id_sereno': reporte.id_sereno,
        'estado': reporte.id_estado  # 1 = pendiente, 2 = aceptado, etc.
    }), 200




















