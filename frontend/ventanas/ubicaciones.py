from consultas import (consultar_estuvo, consultar_movimientos, consultar_personas, consultar_lugares)
from ventanas.estilos import (COLOR_CAFE, colocar, crear_area_resultado, crear_boton, crear_boton_kraft, crear_entrada, crear_lista,
                            escribir, etiqueta, limpiar, mostrar_aviso, mostrar_error)
from ventanas.navegacion import pantalla_seccion

"""
* Objetivo: Valida una hora en formato HHMM.
* Entradas: Texto.
* Salidas: Verdadero si la hora es válida.
* Restricciones: Debe ser una hora de 24 horas.
"""
def hora_valida(texto):
    if len(texto) == 4 and texto.isdigit() and int(texto[:2]) < 24 and int(texto[2:]) < 60:
        return True
    else:
        return False
    
"""
* Objetivo: Consulta una ubicación exacta.
* Entradas: Persona, lugar, hora y área de resultados.
* Salidas: Escribe el resultado en pantalla.
* Restricciones: Todos los campos deben estar completos.
"""
def consultar_por_hora(combo_persona, combo_lugar,  entrada_hora, area):
    persona = combo_persona.get()
    lugar = combo_lugar.get()
    hora = entrada_hora.get().strip()
    
    if not persona or not lugar or not hora:
        mostrar_aviso("Debe completar todos los campos.")
        return
    if not hora_valida(hora):
        mostrar_aviso("La hora debe estar en formato HHMM 24 horas.")
        return
    limpiar(area)
    escribir(area, consultar_estuvo(persona, lugar, int(hora)))
    
"""
* Objetivo: Consulta movimientos en un intervalo.
* Entradas: Persona, lugar, inicio, fin y área.
* Salidas: Escribe el resultado en pantalla.
* Restricciones: Inicio no puede ser mayor que fin.
"""
def consultar_por_intervalo(combo_persona, combo_lugar, entrada_inicio, entrada_fin, area):
    persona = combo_persona.get()
    lugar = combo_lugar.get()
    inicio = entrada_inicio.get().strip()
    fin = entrada_fin.get().strip()
    
    if not persona or not lugar or not inicio or not fin:
        mostrar_aviso("Debe completar todos los campos.")
        return
    if not hora_valida(inicio) or not hora_valida(fin):
        mostrar_aviso("Las horas deben estar en formato HHMM 24 horas.")
        return
    if int(inicio) > int(fin):
        mostrar_aviso("La hora de inicio no puede ser mayor que la hora de fin.")
        return
    limpiar(area)
    escribir(area, consultar_movimientos(persona, lugar, int(inicio), int(fin)))
    
"""
* Objetivo: Decide automáticamente qué consulta ejecutar.
* Entradas: Persona, lugares, horas y área de resultados.
* Salidas: Muestra el resultado correspondiente.
* Restricciones:
* - Si se llena Hora, usa estuvo_en/3.
* - Si se llenan Inicio y Fin, usa estuvo_en_intervalo/4.
"""
def consultar(combo_persona, combo_lugar_1, entrada_hora, combo_lugar_2, entrada_inicio, entrada_fin, area):
    hora = entrada_hora.get().strip()
    inicio = entrada_inicio.get().strip()
    fin = entrada_fin.get().strip()
    # Caso donde esten ambos
    if hora and (inicio or fin):
        mostrar_aviso("Use una consulta por hora o por intervalo, no ambas. Debe eliminar la o las horas de alguna de las opcines, hora exacta o intervalo")
        return
    # Consulta por hora exacta
    if hora:
        consultar_por_hora(combo_persona, combo_lugar_1, entrada_hora, area)
        return
    # Consulta por intervalo
    if inicio or fin:
        consultar_por_intervalo(combo_persona, combo_lugar_2, entrada_inicio, entrada_fin, area)
        return
    mostrar_aviso("Ingrese una hora o un intervalo para consultar.")

"""
* Objetivo: Muestra la pantalla de ubicaciones.
* Entradas: Contenedor padre.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def mostrar_ubicaciones(padre):
    lienzo = pantalla_seccion(padre, "CONSULTA DE UBICACIONES", "ubicaciones")

    etiqueta(lienzo, 290, 218, "Persona")
    combo_persona = crear_lista(lienzo, consultar_personas())
    colocar(lienzo, combo_persona, 290, 232, 230, 32)

    # Columna izquierda: ubicación a una hora exacta
    lienzo.create_text(290, 292, text="Ubicación a una hora exacta", anchor="w", font=("Segoe UI", 11, "bold"), fill=COLOR_CAFE)
    etiqueta(lienzo, 290, 318, "Lugar")
    combo_lugar_hora = crear_lista(lienzo, consultar_lugares())
    colocar(lienzo, combo_lugar_hora, 290, 332, 200, 32)
    etiqueta(lienzo, 505, 318, "Hora (HHMM)")
    entrada_hora = crear_entrada(lienzo)
    colocar(lienzo, entrada_hora, 505, 332, 110, 32)

    # Columna derecha: movimientos en un intervalo
    lienzo.create_text(700, 292, text="Movimientos en un intervalo", anchor="w", font=("Segoe UI", 11, "bold"), fill=COLOR_CAFE)
    etiqueta(lienzo, 700, 318, "Lugar")
    combo_lugar_intervalo = crear_lista(lienzo, consultar_lugares())
    colocar(lienzo, combo_lugar_intervalo, 700, 332, 200, 32)
    etiqueta(lienzo, 915, 318, "Inicio (HHMM)")
    entrada_inicio = crear_entrada(lienzo)
    colocar(lienzo, entrada_inicio, 915, 332, 100, 32)
    etiqueta(lienzo, 1030, 318, "Fin (HHMM)")
    entrada_fin = crear_entrada(lienzo)
    colocar(lienzo, entrada_fin, 1030, 332, 100, 32)

    area = crear_area_resultado(lienzo, 290, 380, 935, 302)
    colocar(lienzo, crear_boton(lienzo, "Consultar", lambda: consultar(combo_persona, combo_lugar_hora, entrada_hora, combo_lugar_intervalo, entrada_inicio, entrada_fin, area)), 535, 232, 140, 32)
    colocar(lienzo, crear_boton_kraft(lienzo, "Limpiar", lambda: limpiar(area)), 690, 232, 110, 32)