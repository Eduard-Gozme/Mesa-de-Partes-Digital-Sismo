"""Módulo de clasificación de expedientes en cuatro niveles de prioridad."""

# Palabras clave que indican riesgo inmediato en la descripción del reporte
PALABRAS_GRAVES = [
    "atrapado", "atrapada", "derrumbe", "colapso", "incendio",
    "fuga de gas", "herido", "sin respirar", "desaparecido",
]

# Rango numérico para ordenar de mayor gravedad (1) a menor gravedad (4)
RANGO = {"CRITICO": 1, "ALTO": 2, "MEDIO": 3, "BAJO": 4}


def contiene_palabra_grave(descripcion):
    """Retorna True si la descripción incluye alguna expresión de gravedad."""
    texto = descripcion.lower()
    for palabra in PALABRAS_GRAVES:
        if palabra in texto:
            return True
    return False


def calcular_puntaje(tipo, personas, heridos, descripcion):
    """Calcula el puntaje discreto de gravedad (entre 1 y 12 puntos)."""
    puntaje = 0

    # Puntos por tipo de solicitud (Ayuda=3, Daño=2, Atención=1)
    if tipo == "2":
        puntaje += 3
    elif tipo == "1":
        puntaje += 2
    else:
        puntaje += 1

    # Puntos por cantidad de personas afectadas
    if personas >= 10:
        puntaje += 3
    elif personas >= 4:
        puntaje += 2
    elif personas >= 1:
        puntaje += 1

    # Puntos adicionales por heridos confirmados y palabras de gravedad
    if heridos == "S":
        puntaje += 3
    if contiene_palabra_grave(descripcion):
        puntaje += 3

    return puntaje


def clasificar(puntaje):
    """Asigna el nivel de prioridad según intervalos disjuntos del puntaje total."""
    if puntaje >= 8:
        return "CRITICO"
    if puntaje >= 5:
        return "ALTO"
    if puntaje >= 3:
        return "MEDIO"
    return "BAJO"
