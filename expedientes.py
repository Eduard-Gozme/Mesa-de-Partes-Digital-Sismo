"""Módulo de operaciones sobre expedientes: registro, búsqueda, ordenamiento y resumen."""
import clasificacion as cla

# Mapa de códigos numéricos del menú a etiquetas legibles de tipo de solicitud
TIPOS = {"1": "Daño", "2": "Ayuda", "3": "Atención"}


def generar_codigo(codigos, anio):
    """Genera un código correlativo único con formato SIS-AAAA-NNNN."""
    return f"SIS-{anio}-{len(codigos) + 1:04d}"


def registrar(datos, dni, nombre, distrito, tipo, descripcion, personas, heridos, fecha, anio):
    """Clasifica un nuevo reporte y lo inserta sincronizado en las 10 listas paralelas."""
    codigo = generar_codigo(datos["codigos"], anio)
    puntaje = cla.calcular_puntaje(tipo, int(personas), heridos.upper(), descripcion)
    prioridad = cla.clasificar(puntaje)

    # Inserción sincronizada: el mismo índice i representa un único expediente
    datos["codigos"].append(codigo)
    datos["dnis"].append(dni)
    datos["nombres"].append(nombre.strip().title())
    datos["distritos"].append(distrito.strip().upper())
    datos["tipos"].append(TIPOS[tipo])
    datos["descripciones"].append(descripcion.strip())
    datos["personas"].append(str(int(personas)))
    datos["heridos"].append(heridos.upper())
    datos["fechas"].append(fecha)
    datos["prioridades"].append(prioridad)
    return codigo, prioridad


def buscar_por_codigo(codigos, codigo):
    """Realiza una búsqueda secuencial por código y retorna su índice o -1 si no existe."""
    objetivo = codigo.strip().upper()
    for i in range(len(codigos)):
        if codigos[i] == objetivo:
            return i
    return -1


def _burbuja(claves, datos):
    """Ordena usando método burbuja intercambiando en sincronía las 10 listas paralelas."""
    n = len(claves)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if claves[j] > claves[j + 1]:
                claves[j], claves[j + 1] = claves[j + 1], claves[j]
                for campo in datos:
                    arreglo = datos[campo]
                    arreglo[j], arreglo[j + 1] = arreglo[j + 1], arreglo[j]


def ordenar_por_codigo(datos):
    """Ordena los expedientes ascendentemente por su código identificador."""
    _burbuja(list(datos["codigos"]), datos)


def ordenar_por_prioridad(datos):
    """Ordena por doble criterio: primero por código y luego por nivel de prioridad."""
    ordenar_por_codigo(datos)
    claves = []
    for prioridad in datos["prioridades"]:
        claves.append(cla.RANGO[prioridad])
    _burbuja(claves, datos)


def contar_por_prioridad(prioridades):
    """Cuenta la cantidad de expedientes registrados por cada nivel de prioridad."""
    conteo = {"CRITICO": 0, "ALTO": 0, "MEDIO": 0, "BAJO": 0}
    for p in prioridades:
        if p in conteo:
            conteo[p] += 1
    return conteo


def contar_por_tipo(tipos):
    """Cuenta la cantidad de expedientes registrados por cada tipo de solicitud."""
    conteo = {"Ayuda": 0, "Daño": 0, "Atención": 0}
    for t in tipos:
        if t in conteo:
            conteo[t] += 1
    return conteo


def sumar_afectados_recursivo(personas, indice=0):
    """Suma de forma recursiva el total de personas afectadas en el arreglo paralelo."""
    if indice == len(personas):
        return 0
    return int(personas[indice]) + sumar_afectados_recursivo(personas, indice + 1)
