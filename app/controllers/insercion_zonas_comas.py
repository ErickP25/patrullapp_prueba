import json
from shapely.geometry import shape
import psycopg2

# Conexión a tu base de datos PostgreSQL
conn = psycopg2.connect(
    dbname="PatrullAPP",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Abrir el archivo GeoJSON
with open("ZONAS COMAS.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Recorrer las zonas del GeoJSON
for feature in data["features"]:
    nombre = feature["properties"]["name"]
    polygon = shape(feature["geometry"])  # shapely.geometry.Polygon
    wkt = polygon.wkt  # Formato WKT (Well-Known Text)

    # Insertar en la tabla zona con id_municipalidad = 9
    cur.execute("""
        INSERT INTO zona (id_municipalidad, nombre, geom)
        VALUES (%s, %s, ST_GeomFromText(%s, 4326));
    """, (9, nombre, wkt))

# Guardar cambios y cerrar conexión
conn.commit()
cur.close()
conn.close()

print("✅ Zonas insertadas correctamente.")