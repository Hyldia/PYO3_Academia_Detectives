from consultas import consultar_evidencias, consultar_personas
from ventanas.estilos import (colocar, crear_area_resultado, crear_boton, crear_boton_kraft, crear_entrada, crear_lista,
                            escribir, etiqueta, limpiar, mostrar_aviso, mostrar_error)
from ventanas.navegacion import pantalla_seccion

"""
* Objetivo: Muestra las evidencias asociadas a la persona seleccionada.
* Entradas: Lista de personas y área de resultados.
* Salidas: Ninguna; escribe las evidencias en el área.
* Restricciones: Debe haber una persona seleccionada.
"""
def consultar(combo_persona, area):
    persona = combo_persona.get()
    if not persona:
        mostrar_aviso("Seleccione una persona para consultar sus evidencias.")
        return
    limpiar(area)
    evidencias = consultar_evidencias(persona)
    if evidencias:
        escribir(area, f"Evidencias asociadas a {persona}\n", "titulo")
        for evidencia in evidencias:
            escribir(area, f"• {evidencia}\n", "item")
    else:
        escribir(area, f"No se encontraron evidencias asociadas a {persona}.")

"""
* Objetivo: Muestra la sección de evidencias y movimientos.
* Entradas: Contenedor.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def mostrar_evidencias(padre):
    lienzo = pantalla_seccion(padre, "CONSULTA DE EVIDENCIAS", "evidencias")

    etiqueta(lienzo, 290, 172, "Persona")
    combo_persona = crear_lista(lienzo, consultar_personas())
    colocar(lienzo, combo_persona, 290, 186, 150, 32)

    area = crear_area_resultado(lienzo, 290, 228, 935, 454)
    colocar(lienzo, crear_boton(lienzo, "Ver evidencias", lambda: consultar(combo_persona, area)), 448, 186, 125, 32)
    colocar(lienzo, crear_boton_kraft(lienzo, "Limpiar", lambda: limpiar(area)), 600, 186, 90, 32)