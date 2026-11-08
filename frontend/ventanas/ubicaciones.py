from consultas import (consultar_estuvo, consultar_movimientos, consultar_personas, consultar_lugares)
from ventanas.estilos import (colocar, crear_area_resultado, crear_boton, crear_boton_kraft, crear_entrada, crear_lista,
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
def mostrar_ubicaciones(ubicacion):
    lienzo = pantalla_seccion(ubicacion, "CONSULTA DE UBICACIONES", "ubicaciones")
    etiqueta(lienzo, 600, 180, "Persona")
    combo_persona = crear_lista(lienzo, consultar_personas())
    colocar(lienzo, combo_persona, 520, 205, 220, 32)
    # Columan izquierda
    etiqueta(lienzo, 350, 280, "Ubicación exacta")
    
    etiqueta(lienzo, 350, 315, "Lugar")
    combo_lugar_1 = crear_lista(lienzo, consultar_lugares())
    colocar(lienzo, combo_lugar_1, 350, 335, 200, 32)

    etiqueta(lienzo, 380, 395, "Hora (HHMM)")
    entrada_hora = crear_entrada(lienzo)
    colocar(lienzo, entrada_hora, 380, 410, 110, 32)
    
    
    #Columna derecha
    etiqueta(lienzo, 720, 280, "Movimientos en un intervalo")
    
    etiqueta(lienzo, 720, 315, "Lugar")
    combo_lugar_2 = crear_lista(lienzo, consultar_lugares())
    colocar(lienzo, combo_lugar_2, 720, 335, 200, 32)
    
    etiqueta(lienzo, 720, 395, "Inicio (HHMM)")
    entrada_inicio = crear_entrada(lienzo)
    colocar(lienzo, entrada_inicio, 720, 410, 90, 32)
    
    etiqueta(lienzo, 840, 395, "Fin (HHMM)")
    entrada_fin = crear_entrada(lienzo)
    colocar(lienzo, entrada_fin, 840, 410, 90, 32)
    
    # Resultados
    area = crear_area_resultado(lienzo, 290, 460, 935, 220)
    colocar(lienzo, crear_boton(lienzo, "Consultar", lambda: consultar(combo_persona, combo_lugar_1, entrada_hora, combo_lugar_2, entrada_inicio, entrada_fin, area)), 1040, 240, 150, 40)
    colocar(lienzo, crear_boton_kraft(lienzo, "Limpiar", lambda: limpiar(area)), 1040, 300, 150, 40)