"""Módulo principal: menú interactivo de la Mesa de Partes Digital-Sismo (Ate)."""
from datetime import datetime
import validaciones as val
import expedientes as exp
import archivos as arc


def pedir_dato(mensaje, tipo, error):
    """Solicita un dato por consola y repite hasta cumplir su regla de validación."""
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
            # Mejora de usabilidad: Enter toma automáticamente la fecha actual
            if dato == "":
                return datetime.now().strftime("%d/%m/%Y")
            correcto = val.validar_fecha(dato)

        if correcto:
            return dato
        print(" [!] " + error)


def mostrar(datos, i):
    """Muestra en una línea legible los datos principales del expediente en la posición i."""
    print(
        f" [{datos['prioridades'][i]}] {datos['codigos'][i]} | "
        f"{datos['nombres'][i]} | {datos['distritos'][i]} | "
        f"{datos['tipos'][i]} | {datos['personas'][i]} personas | "
        f"{datos['descripciones'][i]}"
    )


def mostrar_grafico_resumen(conteo_prioridad, conteo_tipo):
    """Genera un panel doble de barras (prioridad y tipo de solicitud) usando matplotlib."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print(" [Aviso] matplotlib no está instalado; se muestra solo el resumen en texto.")
        return

    niveles = list(conteo_prioridad.keys())
    valores_prio = list(conteo_prioridad.values())
    colores_prio = ["#D32F2F", "#F57C00", "#FBC02D", "#388E3C"]

    tipos = list(conteo_tipo.keys())
    valores_tipo = list(conteo_tipo.values())
    colores_tipo = ["#1565C0", "#6A1B9A", "#00838F"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    # Gráfico 1: Expedientes por nivel de prioridad
    barras1 = ax1.bar(niveles, valores_prio, color=colores_prio)
    ax1.set_title("Expedientes por Nivel de Prioridad")
    ax1.set_xlabel("Prioridad")
    ax1.set_ylabel("Cantidad de expedientes")
    ax1.set_ylim(0, max(valores_prio + [1]) + 1)
    for barra in barras1:
        alto = int(barra.get_height())
        ax1.text(barra.get_x() + barra.get_width() / 2, alto + 0.1, str(alto), ha="center")

    # Gráfico 2: Expedientes por tipo de solicitud
    barras2 = ax2.bar(tipos, valores_tipo, color=colores_tipo)
    ax2.set_title("Expedientes por Tipo de Solicitud")
    ax2.set_xlabel("Tipo")
    ax2.set_ylabel("Cantidad de expedientes")
    ax2.set_ylim(0, max(valores_tipo + [1]) + 1)
    for barra in barras2:
        alto = int(barra.get_height())
        ax2.text(barra.get_x() + barra.get_width() / 2, alto + 0.1, str(alto), ha="center")

    fig.suptitle("Resumen Operativo — Mesa de Partes Digital-Sismo (Ate)", fontweight="bold")
    plt.tight_layout()
    plt.show()
    plt.close(fig)


def menu():
    """Bucle principal del sistema: carga los expedientes y gestiona las 6 opciones."""
    datos = arc.cargar()
    anio = datetime.now().year
    opcion = ""

    while opcion != "6":
        print("\n=== MESA DE PARTES DIGITAL-SISMO (ATE) ===")
        print("1. Registrar     2. Buscar por código     3. Ordenar por prioridad")
        print("4. Listar        5. Resumen               6. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            hoy = datetime.now().strftime("%d/%m/%Y")
            dni = pedir_dato("DNI (8 dígitos): ", "dni", "DNI inválido.")
            nombre = pedir_dato("Nombre completo: ", "nombre", "Nombre inválido.")
            distrito = pedir_dato("Distrito: ", "distrito", "Por ahora solo se registra ATE.")
            tipo = pedir_dato("Tipo (1 Daño, 2 Ayuda, 3 Atención): ", "reporte", "Elija 1, 2 o 3.")
            desc = pedir_dato("Descripción (10-150 caracteres): ", "descripcion", "Descripción inválida.")
            personas = pedir_dato("Personas afectadas: ", "personas", "Número de 0 a 500.")
            heridos = pedir_dato("¿Hay heridos? (S/N): ", "heridos", "Responda S o N.")
            fecha = pedir_dato(
                f"Fecha (dd/mm/aaaa, Enter para hoy {hoy}): ",
                "fecha",
                "Fecha inválida.",
            )
            codigo, prioridad = exp.registrar(
                datos, dni, nombre, distrito, tipo, desc, personas, heridos, fecha, anio
            )
            arc.guardar(datos)
            print(f" Registrado: {codigo} | Prioridad: {prioridad} | Fecha: {fecha}")

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
            conteo_tipos = exp.contar_por_tipo(datos["tipos"])
            total_afectados = exp.sumar_afectados_recursivo(datos["personas"])

            print("\n--- Resumen por Prioridad ---")
            for nivel in conteo:
                print(f" {nivel}: {conteo[nivel]}")
            print("\n--- Resumen por Tipo de Solicitud ---")
            for tipo_nombre in conteo_tipos:
                print(f" {tipo_nombre}: {conteo_tipos[tipo_nombre]}")
            print(f"\n Total de personas afectadas: {total_afectados}")

            if datos["codigos"]:
                mostrar_grafico_resumen(conteo, conteo_tipos)
            else:
                print(" No hay expedientes suficientes para generar gráficos.")

        elif opcion != "6":
            print(" Opción no válida.")


if __name__ == "__main__":
    menu()
