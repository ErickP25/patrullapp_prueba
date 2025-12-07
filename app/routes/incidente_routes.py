import datetime
import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify
from sqlalchemy import null, desc

from ..models.incidente import Incidente
from ..models.db import db
from ..models.reporte import Reporte
from ..models.zona import Zona
from ..controllers.openai_utils import transcribir_audio, extraer_info_con_gpt
from .pantalla_tu_zona import obtenerZonaPorCoordendas

UPLOAD_AUDIO_FOLDER = 'uploads_audio'
os.makedirs(UPLOAD_AUDIO_FOLDER, exist_ok=True)

# Catálogo de incidentes y su prioridad
catalogo_incidentes = {
    "Homicidio doloso": 1,
    "Feminicidio": 1,
    "Sicariato": 1,
    "Secuestro": 1,
    "Robo agravado": 2,
    "Extorsión": 2,
    "Violencia sexual": 2,
    "Lesiones personales": 3,
    "Hurto agravado": 3,
    "Daños a la propiedad": 3,
    "Hurto simple": 3,
    "Tráfico ilícito de drogas": 4,
    "Conducción en estado de ebriedad": 4,
    "Corrupción pública": 4,
    "Manifestaciones o motines": 5,
    "Riñas": 5,
    "Exhibiciones u actos obscenos": 5
}
incidente_bp = Blueprint('incidente', __name__)


# --- ENDPOINT 1: Procesa el audio y devuelve datos ---

@incidente_bp.route('/api/procesar_audio', methods=['POST'])
def procesar_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No se envió el archivo de audio'}), 400

    audio_file = request.files['audio']
    direccion = request.form.get('direccion')
    latitud = request.form.get('latitud')
    longitud = request.form.get('longitud')

    if not direccion or not latitud or not longitud:
        return jsonify({'error': 'Faltan datos de ubicación'}), 400

    zona = obtenerZonaPorCoordendas(float(latitud), float(longitud))
    if not zona:
        return jsonify({'error': 'No se encontró una zona válida'}), 404

    filename = f"{uuid.uuid4()}.wav"
    filepath = os.path.join(UPLOAD_AUDIO_FOLDER, filename)
    audio_file.save(filepath)

    try:
        texto_transcrito = transcribir_audio(filepath)
        resultado_gpt = extraer_info_con_gpt(texto_transcrito)
        tipo_detectado = resultado_gpt.strip()

        if tipo_detectado not in catalogo_incidentes:
            return jsonify({'error': 'Tipo de incidente no reconocido'}), 422

        incidente = Incidente.query.filter_by(nombre=tipo_detectado).first()
        if not incidente:
            return jsonify({'error': 'Incidente no registrado en BD'}), 422

        return jsonify({
            'estado': 'ok',
            'tipo': tipo_detectado,
            'transcripcion': texto_transcrito,
            'referencia': direccion
        })

    except Exception as e:
        return jsonify({'error': 'Error al procesar el audio', 'detalle': str(e)}), 500

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)



UPLOAD_FOLDER = 'uploads'  # o ruta absoluta
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# --- ENDPOINT 2: Guarda el reporte ---

@incidente_bp.route('/api/guardar_reporte', methods=['POST'])
def guardar_reporte():
    try:
        id_vecino = request.form.get('id_vecino')
        id_incidente = request.form.get('id_incidente')
        id_zona = request.form.get('id_zona')
        direccion = request.form.get('direccion')
        latitud = request.form.get('latitud')
        longitud = request.form.get('longitud')
        descripcion = request.form.get('descripcion')
        evidencia = 'imagen' in request.files

        if not all([id_vecino, id_incidente, id_zona, direccion, latitud, longitud, descripcion]):
            return jsonify({'error': 'Faltan campos obligatorios'}), 400

        nuevo_reporte = Reporte(
            id_vecino=id_vecino,
            id_sereno=None,
            id_incidente=id_incidente,
            id_zona=id_zona,
            id_estado=1,
            fecha=datetime.date.today(),
            hora=datetime.datetime.now().time(),
            direccion=direccion,
            longitud=float(longitud),
            latitud=float(latitud),
            descripcion=descripcion,
            evidencia=evidencia,
            emergencia=False
        )
        db.session.add(nuevo_reporte)
        db.session.commit()

        zona = Zona.query.get(id_zona)
        if zona:
            zona.cant_incidentes = zona.cant_incidentes + 1
            db.session.commit()

        return jsonify({'estado': 'reporte guardado', 'id_reporte': nuevo_reporte.id_reporte})

    except Exception as e:
        return jsonify({'error': 'Error al guardar el reporte', 'detalle': str(e)}), 500

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@incidente_bp.route('/api/subir_evidencia', methods=['POST'])
def subir_evidencia():

    reporte_asociado = Reporte.query.filter_by(id_vecino = request.form.get('id_vecino')).order_by(desc(Reporte.fecha)).first()
    id_reporte = reporte_asociado.id_reporte

    if 'imagen' not in request.files:
        return jsonify({'error': 'No se envió archivo'}), 400

    archivo = request.files['imagen']

    if archivo.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400

    if archivo and allowed_file(archivo.filename):
        filename = secure_filename(f"reporte_{id_reporte}_" + archivo.filename)
        path_completo = os.path.join(UPLOAD_FOLDER, filename)
        archivo.save(path_completo)

        return jsonify({'mensaje': 'Evidencia subida correctamente'}), 200

    return jsonify({'error': 'Formato de archivo no permitido'}), 400
