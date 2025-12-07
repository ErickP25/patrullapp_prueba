from datetime import datetime

from flask import Blueprint, request, jsonify
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy import func
from ..models.db import db
from ..models.zona import Zona
from ..models.reporte import Reporte
from ..models.incidente import Incidente
from ..models.estadoreporte import EstadoReporte

import json

verreportes_bp = Blueprint('verreportes', __name__)


@verreportes_bp.route('/api/ver_cantidad_incidentes', methods=['POST'])
def ver_reportes_filtros():
    filtros = request.get_json()

    tipo_incidente = filtros.get('tipo_incidente')
    estado_reporte = filtros.get('estado_reporte')
    fecha = filtros.get('fecha')

    query = db.session.query(
        Reporte,
        Incidente.tipo_incidente,
        EstadoReporte.tipo_estado
    ).join(Incidente, Reporte.id_incidente == Incidente.id_incidente
           ).join(EstadoReporte, Reporte.id_estado == EstadoReporte.id_estado)

    if tipo_incidente not in [None, ""]:
        query = query.filter(Incidente.tipo_incidente == tipo_incidente)

    if estado_reporte not in [None, ""]:
        query = query.filter(EstadoReporte.tipo_estado == estado_reporte)

    if fecha not in [None, ""]:
        try:
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            query = query.filter(Reporte.fecha == fecha_obj)
        except ValueError:
            return jsonify({'error': 'Formato de fecha inválido. Debe ser YYYY-MM-DD'}), 400

    reportes = query.all()
    ahora = datetime.now()

    resultados = []
    for reporte, tipo, estado in reportes:
        # Combinar fecha y hora para calcular antigüedad
        dt_reporte = datetime.combine(reporte.fecha, reporte.hora)
        diferencia = ahora - dt_reporte
        antiguedad_minutos = int(diferencia.total_seconds() // 60)

        resultados.append({
            'direccion': reporte.direccion,
            'tipo_incidente': tipo,
            'estado': estado,
            'antiguedad_minutos': antiguedad_minutos
        })

    return jsonify({'cantidad': len(resultados), 'reportes': resultados})
