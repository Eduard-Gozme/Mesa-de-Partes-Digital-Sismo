"""Módulo de validaciones para las solicitudes ciudadanas de Ate."""
from datetime import datetime

# Distritos habilitados en el prototipo (alcance acotado al distrito de Ate)
DISTRITOS = ["ATE"]


def validar_dni(dni):
    """Comprueba que el DNI tenga exactamente 8 dígitos numéricos."""
    return len(dni) == 8 and dni.isdigit()


def validar_nombre(nombre):
    """Comprueba que el nombre tenga al menos 3 caracteres, solo letras y espacios."""
    limpio = nombre.strip()
    if len(limpio) < 3:
        return False
    for letra in limpio:
        if not (letra.isalpha() or letra == " "):
            return False
    return True


def validar_distrito(distrito):
    """Comprueba que el distrito ingresado corresponda al alcance del prototipo (ATE)."""
    return distrito.strip().upper() in DISTRITOS


def validar_tipo(tipo):
    """Comprueba que el tipo de solicitud sea 1 (Daño), 2 (Ayuda) o 3 (Atención)."""
    return tipo in ("1", "2", "3")


def validar_descripcion(texto):
    """Comprueba longitud entre 10 y 150 caracteres y bloquea '|' para proteger el TXT."""
    return 10 <= len(texto.strip()) <= 150 and "|" not in texto


def validar_personas(texto):
    """Comprueba que la cantidad de personas afectadas sea un entero entre 0 y 500."""
    return texto.isdigit() and 0 <= int(texto) <= 500


def validar_si_no(texto):
    """Comprueba que la respuesta sea 'S' o 'N' sin importar mayúsculas o espacios."""
    return texto.strip().upper() in ("S", "N")


def validar_fecha(fecha):
    """Comprueba que la fecha exista en el calendario con formato dd/mm/aaaa."""
    try:
        datetime.strptime(fecha, "%d/%m/%Y")
        return True
    except ValueError:
        return False
