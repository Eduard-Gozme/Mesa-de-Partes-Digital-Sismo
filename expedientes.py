"""Operaciones de registro, consulta y ordenamiento."""
import clasificacion as cla

TIPOS = {"1": "Daño", "2": "Ayuda", "3": "Atención"}

def generar_codigo(codigos, anio):
    return f"SIS-{anio}-{len(codigos) + 1:04d}"

def registrar(datos, dni, nombre, distrito, tipo, descripcion, personas, heridos, fecha, anio):
    codigo = generar_codigo(datos["codigos"], anio)
    puntaje = cla.calcular_puntaje(tipo, int(personas), heridos.upper(), descripcion)
    prioridad = cla.clasificar(puntaje)
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
    for i in range(len(codigos)):
        if codigos[i] == codigo.strip().upper():
            return i
    return -1

def _burbuja(claves, datos):
    n = len(claves)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if claves[j] > claves[j+1]:
                claves[j], claves[j+1] = claves[j+1], claves[j]
                for campo in datos:
                    arreglo = datos[campo]
                    arreglo[j], arreglo[j+1] = arreglo[j+1], arreglo[j]

def ordenar_por_codigo(datos):
    _burbuja(list(datos["codigos"]), datos)

def ordenar_por_prioridad(datos):
    ordenar_por_codigo(datos)
    claves = []
    for prioridad in datos["prioridades"]:
        claves.append(cla.RANGO[prioridad])
    _burbuja(claves, datos)

def contar_por_prioridad(prioridades):
    conteo = {"CRITICO": 0, "ALTO": 0, "MEDIO": 0, "BAJO": 0}
    for p in prioridades:
        conteo[p] += 1
    return conteo
