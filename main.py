"""Mesa de Partes Digital-Sismo, caso Ate."""
from datetime import datetime
import validaciones as val
import expedientes as exp
import archivos as arc

def pedir_dato(mensaje, tipo, error):
    """Pide un dato hasta que pase la validación correspondiente."""
    while True:
        dato = input(mensaje).strip()
        correcto = False

        if tipo == "dni":
            correcto = val.validar_dni(dato)
        elif tipo == "nombre":
            correcto = val.validar_nombre(dato)
        elif tipo == "distrito":
            correcto = val.validar_distrito(dato)
        elif tipo == "reporte":
            correcto = val.validar_tipo(dato)
        elif tipo == "descripcion":
            correcto = val.validar_descripcion(dato)
        elif tipo == "personas":
            correcto = val.validar_personas(dato)
        elif tipo == "heridos":
            correcto = val.validar_si_no(dato)
        elif tipo == "fecha":
            correcto = val.validar_fecha(dato)

        if correcto:
            return dato
        print(" [!] " + error)

def mostrar(datos, i):
    print(f" [{datos['prioridades'][i]}] {datos['codigos'][i]} | "
          f"{datos['nombres'][i]} | {datos['distritos'][i]} | "
          f"{datos['tipos'][i]} | {datos['personas'][i]} personas | "
          f"{datos['descripciones'][i]}")

def menu():
    datos = arc.cargar()
    anio = datetime.now().year
    opcion = ""
    while opcion != "6":
        print("\n=== MESA DE PARTES DIGITAL-SISMO (ATE) ===")
        print("1. Registrar     2. Buscar por código     3. Ordenar por prioridad")
        print("4. Listar       5. Resumen               6. Salir")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            dni = pedir_dato("DNI (8 dígitos): ", "dni", "DNI inválido.")
            nombre = pedir_dato("Nombre completo: ", "nombre", "Nombre inválido.")
            distrito = pedir_dato("Distrito: ", "distrito", "Por ahora solo se registra ATE.")
            tipo = pedir_dato("Tipo (1 Daño, 2 Ayuda, 3 Atención): ", "reporte", "Elija 1, 2 o 3.")
            desc = pedir_dato("Descripción (10-150 caracteres): ", "descripcion", "Descripción inválida.")
            personas = pedir_dato("Personas afectadas: ", "personas", "Número de 0 a 500.")
            heridos = pedir_dato("¿Hay heridos? (S/N): ", "heridos", "Responda S o N.")
            fecha = pedir_dato("Fecha (dd/mm/aaaa): ", "fecha", "Fecha inválida.")
            codigo, prioridad = exp.registrar(datos, dni, nombre, distrito, tipo, desc, personas, heridos, fecha, anio)
            arc.guardar(datos)
            print(f" Registrado: {codigo} | Prioridad: {prioridad}")
        elif opcion == "2":
            i = exp.buscar_por_codigo(datos["codigos"], input("Código: "))
            if i == -1:
                print(" Expediente no encontrado.")
            else:
                mostrar(datos, i)
        elif opcion == "3":
            exp.ordenar_por_prioridad(datos)
            arc.guardar(datos)
            print(" Ordenado: casos críticos primero.")
        elif opcion == "4":
            if not datos["codigos"]:
                print(" No hay expedientes.")
            for i in range(len(datos["codigos"])):
                mostrar(datos, i)
        elif opcion == "5":
            conteo = exp.contar_por_prioridad(datos["prioridades"])
            for nivel in conteo:
                print(f" {nivel}: {conteo[nivel]}")
        elif opcion != "6":
            print(" Opción no válida.")

if __name__ == "__main__":
    menu()
