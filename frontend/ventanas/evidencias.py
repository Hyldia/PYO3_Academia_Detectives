from consultas import consultar_evidencias, consultar_lugares, consultar_movimientos, consultar_personas
from ventanas.estilos import (colocar, crear_area_resultado, crear_boton, crear_boton_kraft, crear_entrada, crear_lista,
                              escribir, etiqueta, limpiar, mostrar_aviso, mostrar_error)
from ventanas.navegacion import pantalla_seccion

"""
* Objetivo: Revisa que una hora tenga el formato HHMM.
* Entradas: Texto escrito por la persona.
* Salidas: Verdadero si la hora es válida.
* Restricciones: Solo revisa el formato; no decide nada del caso.
"""
def hora_valida(texto):
    return len(texto) == 4 and texto.isdigit() and int(texto[:2]) < 24 and int(texto[2:]) < 60

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
* Objetivo: Consulta si una persona estuvo en un lugar durante un intervalo.
* Entradas: Listas de persona y lugar, campos de hora y área de resultados.
* Salidas: Ninguna; escribe la respuesta en el área.
* Restricciones: Las horas deben estar en formato HHMM y el inicio no puede ser mayor que el fin.
"""
def consultar_historial(combo_persona, combo_lugar, entrada_inicio, entrada_fin, area):
    persona = combo_persona.get()
    lugar = combo_lugar.get()
    inicio = entrada_inicio.get().strip()
    fin = entrada_fin.get().strip()
    if not persona or not lugar or not inicio or not fin:
        mostrar_aviso("Seleccione la persona y el lugar, y escriba las dos horas.")
        return
    if not hora_valida(inicio) or not hora_valida(fin):
        mostrar_error("Las horas deben tener formato HHMM, por ejemplo 1930.", "HORA INVÁLIDA")
        return
    if int(inicio) > int(fin):
        mostrar_error("La hora de inicio no puede ser mayor que la hora de fin.", "HORA INVÁLIDA")
        return
    escribir(area, "Movimientos\n", "titulo")
    escribir(area, f"• {consultar_movimientos(persona, lugar, int(inicio), int(fin))}\n", "item")

"""
* Objetivo: Muestra la sección de evidencias y movimientos.
* Entradas: Contenedor.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def mostrar_evidencias(padre):
    lienzo = pantalla_seccion(padre, "EVIDENCIAS Y MOVIMIENTOS", "evidencias")

    etiqueta(lienzo, 290, 172, "Persona")
    combo_persona = crear_lista(lienzo, consultar_personas())
    colocar(lienzo, combo_persona, 290, 186, 150, 32)

    etiqueta(lienzo, 600, 172, "Lugar")
    combo_lugar = crear_lista(lienzo, consultar_lugares())
    colocar(lienzo, combo_lugar, 600, 186, 160, 32)

    etiqueta(lienzo, 768, 172, "Inicio HHMM")
    entrada_inicio = crear_entrada(lienzo)
    colocar(lienzo, entrada_inicio, 768, 186, 62, 32)

    etiqueta(lienzo, 860, 172, "Fin HHMM")
    entrada_fin = crear_entrada(lienzo)
    colocar(lienzo, entrada_fin, 855, 186, 62, 32)

    area = crear_area_resultado(lienzo, 290, 228, 935, 454)
    colocar(lienzo, crear_boton(lienzo, "Ver evidencias", lambda: consultar(combo_persona, area)), 448, 186, 125, 32)
    colocar(lienzo, crear_boton(lienzo, "Ver movimientos", lambda: consultar_historial(combo_persona, combo_lugar, entrada_inicio, entrada_fin, area)), 930, 186, 150, 32)
    colocar(lienzo, crear_boton_kraft(lienzo, "Limpiar", lambda: limpiar(area)), 1088, 186, 90, 32)