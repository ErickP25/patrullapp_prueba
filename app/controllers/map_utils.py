from ..models.db import db
from ..models.incidente import Incidente
from shapely.geometry import Point, Polygon


"HOLA"

def obtener_incidentes_por_distrito(distrito):
    return Incidente.query.filter_by(distrito=distrito).all()


def contar_incidentes_por_zona(polygon_coords):
    poligono = Polygon(polygon_coords)
    incidentes = Incidente.query.all()
    total = 0
    incidentes_dentro = []
    for incidente in incidentes:
        if incidente.lat is not None and incidente.lon is not None:
            punto = Point(incidente.lon, incidente.lat)
        if poligono.contains(punto):
            total += 1
            incidentes_dentro.append(incidente)
    return total, incidentes_dentro
