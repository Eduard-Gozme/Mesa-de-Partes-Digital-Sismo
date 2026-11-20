"""Módulo de persistencia para guardar y recuperar expedientes en archivo TXT."""
import os

# Ruta del archivo de texto plano y orden fijo de los 10 campos paralelos
RUTA = "reportes_sismo.txt"
CAMPOS = [
    "codigos", "dnis", "nombres", "distritos", "tipos",
    "descripciones", "personas", "heridos", "fechas", "prioridades",
]


def nuevo_almacen():
    """Inicializa el contenedor con 10 listas paralelas vacías (una por campo)."""
    datos = {}
    for campo in CAMPOS:
        datos[campo] = []
    return datos


def guardar(datos, ruta=RUTA):
    """Escribe todos los expedientes en formato texto plano delimitado por '|' (UTF-8)."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        for i in range(len(datos["codigos"])):
            campos_reporte = []
            for campo in CAMPOS:
                campos_reporte.append(datos[campo][i])
            archivo.write("|".join(campos_reporte) + "\n")


def cargar(ruta=RUTA):
    """Recupera los expedientes desde el archivo TXT; retorna listas vacías si no existe."""
    datos = nuevo_almacen()
    if not os.path.exists(ruta):
        return datos
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.rstrip("\n").split("|")
            if len(partes) == len(CAMPOS):
                for i in range(len(CAMPOS)):
                    datos[CAMPOS[i]].append(partes[i])
    return datos
