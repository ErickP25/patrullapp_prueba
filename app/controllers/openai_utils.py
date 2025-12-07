import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribir_audio(file_path):
    with open(file_path, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)
    return transcript["text"]


def extraer_info_con_gpt(texto):
    catalogo = """
    Homicidio doloso, Feminicidio, Sicariato, Secuestro,
    Robo agravado, Extorsión, Violencia sexual,
    Lesiones personales, Hurto agravado, Daños a la propiedad,
    Hurto simple, Tráfico ilícito de drogas, Conducción en estado de ebriedad,
    Corrupción pública, Manifestaciones o motines, Riñas, Exhibiciones u actos obscenos
    """

    prompt = f"""
Eres un asistente que clasifica reportes de audio transcritos. 
Debes analizar el siguiente reporte de incidente y devolver exclusivamente el tipo de incidente según el siguiente catálogo:

{catalogo}

Si el reporte no corresponde exactamente a ninguno, intenta seleccionar el más cercano. 
Devuelve solamente el nombre exacto de uno de los incidentes de la lista.

Reporte:
\"\"\"{texto}\"\"\"
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return response.choices[0].message.content.strip()