"""Comprobaciones básicas para datos de las solicitudes de Ate."""
from datetime import datetime

DISTRITOS = ["ATE"]

def validar_dni(dni):
    return len(dni) == 8 and dni.isdigit()

def validar_nombre(nombre):
    limpio = nombre.strip()
    if len(limpio) < 3:
        return False
    for letra in limpio:
        if not (letra.isalpha() or letra == " "):
            return False
    return True

def validar_distrito(distrito):
    return distrito.strip().upper() in DISTRITOS

def validar_tipo(tipo):
    return tipo in ("1", "2", "3")

def validar_descripcion(texto):
    return 10 <= len(texto.strip()) <= 150 and "|" not in texto

def validar_personas(texto):
    return texto.isdigit() and 0 <= int(texto) <= 500

def validar_si_no(texto):
    return texto.strip().upper() in ("S", "N")

def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, "%d/%m/%Y")
        return True
    except ValueError:
        return False
