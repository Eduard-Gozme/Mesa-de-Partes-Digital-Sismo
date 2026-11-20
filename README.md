# Mesa de Partes Digital–Sismo (Distrito de Ate, Lima)

Prototipo funcional en **Python** (ejecutable en **Google Colab** y en entorno local) desarrollado por el **Grupo 06** para el curso **Fundamentos de Programación (CIIN1205P)** — Universidad Privada del Norte (Sede Ate, Periodo 2026-II).

## Descripción

Simula la recepción, validación, clasificación por gravedad, búsqueda, ordenamiento y persistencia de solicitudes ciudadanas presentadas ante la Municipalidad Distrital de Ate tras un evento sísmico de gran magnitud, tomando como referencia la Ley N.° 31170 de mesas de partes digitales.

## Estructura modular (5 archivos Python)

| Archivo | Responsabilidad |
|---|---|
| `main.py` | Menú interactivo de 6 opciones, validación en bucle, fecha rápida con `Enter` y gráficos de resumen (`matplotlib`). |
| `validaciones.py` | Validación de DNI (8 dígitos), nombre, distrito (`ATE`), tipo (`1/2/3`), descripción (10–150 caracteres sin `\|`), personas (`0–500`), heridos (`S/N`) y fecha (`dd/mm/aaaa`). |
| `clasificacion.py` | Cálculo discreto del puntaje de gravedad (1 a 12 puntos) y asignación de prioridad (`CRITICO`, `ALTO`, `MEDIO`, `BAJO`). |
| `expedientes.py` | Registro sincronizado en 10 arreglos paralelos, búsqueda secuencial por código, ordenamiento burbuja por doble criterio (código + prioridad), conteos y suma recursiva de personas afectadas (`sumar_afectados_recursivo`). |
| `archivos.py` | Persistencia en archivo de texto plano UTF-8 (`reportes_sismo.txt`) delimitado por `\|`. |

## Novedades de la versión Evaluación Final (EF)

- **Buenas prácticas (Tema 6):** comentarios y docstrings claros en los 5 módulos.
- **Resumen visual con `matplotlib` (Tema 6):** la Opción 5 muestra dos gráficos de barras lado a lado (expedientes por prioridad y por tipo de solicitud), protegido con `try/except ImportError`.
- **Recursividad (Tema 7):** `sumar_afectados_recursivo(personas, indice=0)` calcula el total de personas afectadas en la Opción 5.
- **Usabilidad en registro:** en la Opción 1, presionar `Enter` en el campo fecha asigna automáticamente la fecha actual del sistema; si se escribe una fecha manual, se mantiene la validación estricta `dd/mm/aaaa`.

## Ejecución

### En entorno local
```bash
python main.py
```

### En Google Colab
1. Abrir `Mesa_Sismos.ipynb`.
2. Ejecutar las celdas 1 a 7 para generar los 5 módulos y cargar `casos_demo_sismo_10.txt`.
3. Ejecutar `%run main.py`.
4. Al finalizar, descargar `reportes_sismo.txt` si se desea conservar un respaldo.

## Integrantes — Grupo 06
- Evak Muñoz Contreras
- Daniel Anyelo Barzola Mendoza
- Jhon Anthony Curo Huamán
- Eduard David Gozme Flores
- Juan Andree Pinedo Aquino
