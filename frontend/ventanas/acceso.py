from consultas import consultar_accesos, consultar_personas, consultar_motivos_acceso
from ventanas.estilos import colocar, crear_area_resultado, crear_boton, crear_boton_kraft, crear_lista, escribir, etiqueta, limpiar, mostrar_aviso
from ventanas.navegacion import pantalla_seccion

"""
* Objetivo: Muestra los lugares a los que tiene acceso la persona seleccionada.
* Entradas: Lista de personas y área de resultados.
* Salidas: Ninguna; escribe los lugares en el área.
* Restricciones: Debe haber una persona seleccionada.
"""
def consultar(combo_persona, area):
    persona = combo_persona.get()
    if not persona:
        mostrar_aviso("Seleccione una persona para consultar sus accesos.")
        return
    limpiar(area)
    accesos = consultar_accesos(persona)
    if not accesos:
        escribir(area, f"{persona} no tiene acceso a ningún lugar.")
        return
    escribir(area, f"Lugares a los que {persona} tiene acceso\n", "titulo")
    for lugar in accesos:
        escribir(area, f"• {lugar}\n", "item")
    escribir(area, "Cómo obtiene cada acceso\n", "titulo")
    for motivo in consultar_motivos_acceso(persona):
        escribir(area, f"• {motivo}.\n", "item")

"""
* Objetivo: Muestra la sección de consulta de accesos.
* Entradas: Contenedor.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def mostrar_accesos(padre):
    lienzo = pantalla_seccion(padre, "CONSULTA DE ACCESOS", "accesos")

    etiqueta(lienzo, 290, 218, "Persona")
    combo_persona = crear_lista(lienzo, consultar_personas())
    colocar(lienzo, combo_persona, 290, 232, 230, 32)

    area = crear_area_resultado(lienzo, 290, 278, 935, 404)
    colocar(lienzo, crear_boton(lienzo, "Consultar", lambda: consultar(combo_persona, area)), 535, 232, 140, 32)
    colocar(lienzo, crear_boton_kraft(lienzo, "Limpiar", lambda: limpiar(area)), 690, 232, 110, 32)