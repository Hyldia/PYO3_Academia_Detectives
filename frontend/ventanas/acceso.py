from consultas import consultar_accesos, consultar_personas
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
    if accesos:
        escribir(area, f"{persona} tiene acceso a\n", "titulo")
        for lugar in accesos:
            escribir(area, f"• {lugar}\n", "item")
    else:
        escribir(area, f"{persona} no tiene acceso a ningún lugar.")

"""
* Objetivo: Muestra la sección de consulta de accesos.
* Entradas: Contenedor.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def mostrar_accesos(padre):
    lienzo = pantalla_seccion(padre, "CONSULTA DE ACCESOS", "accesos")

    etiqueta(lienzo, 290, 172, "Persona")
    combo_persona = crear_lista(lienzo, consultar_personas())
    colocar(lienzo, combo_persona, 290, 186, 230, 32)

    area = crear_area_resultado(lienzo, 290, 228, 935, 454)
    colocar(lienzo, crear_boton(lienzo, "Consultar", lambda: consultar(combo_persona, area)), 535, 186, 140, 32)
    colocar(lienzo, crear_boton_kraft(lienzo, "Limpiar", lambda: limpiar(area)), 690, 186, 110, 32)