from consultas import (consultar_coartada, consultar_contradicciones, consultar_descarte, consultar_evento, consultar_explicaciones,
                       consultar_inferencia, consultar_investigacion, consultar_personas, consultar_sospechosos,
                       consultar_todas_contradicciones)
from ventanas.estilos import colocar, crear_area_resultado, crear_boton, crear_boton_kraft, crear_lista, escribir, etiqueta, limpiar, mostrar_aviso
from ventanas.navegacion import pantalla_seccion

"""
* Objetivo: Convierte un valor booleano en el texto Sí o No.
* Entradas: Valor booleano.
* Salidas: El texto Sí o No.
* Restricciones: Ninguna.
"""
def si_no(valor):
    return "Sí" if valor else "No"

"""
* Objetivo: Muestra el análisis de inferencia de la persona seleccionada.
* Entradas: Lista de personas y área de resultados.
* Salidas: Ninguna; escribe el análisis en el área.
* Restricciones: Debe haber una persona seleccionada.
"""
def analizar(combo_persona, area):
    persona = combo_persona.get()
    if not persona:
        mostrar_aviso("Seleccione una persona para analizarla.")
        return
    limpiar(area)
    inferencia = consultar_inferencia(persona)
    escribir(area, f"Análisis de {persona}\n", "titulo")
    if inferencia["sospechoso"]:
        escribir(area, " Cumple las condiciones de posible sospechoso \n", "alerta")
    else:
        escribir(area, " No cumple las condiciones de posible sospechoso \n", "neutro")

    escribir(area, "Oportunidad\n", "titulo")
    escribir(area, f"• Estuvo en la escena durante el evento: {si_no(inferencia['en_escena'])}\n", "item")
    escribir(area, f"• Tiene acceso al lugar del evento: {si_no(inferencia['acceso'])}\n", "item")

    escribir(area, "Indicios\n", "titulo")
    evidencias = ", ".join(inferencia["evidencias"]) if inferencia["evidencias"] else "ninguna"
    escribir(area, f"• Evidencias en la escena: {evidencias}\n", "item")
    escribir(area, f"• Contradicción durante el evento: {si_no(inferencia['contradiccion_evento'])}\n", "item")

    escribir(area, "Coartada\n", "titulo")
    coartada = consultar_coartada(persona)
    if coartada:
        lugar, hora = coartada
        escribir(area, f"• Declaró estar en {lugar} a las {hora} y el registro de movimientos lo respalda.\n", "item")
    else:
        escribir(area, "• No tiene una coartada válida.\n", "item")

    escribir(area, "Contradicciones\n", "titulo")
    contradicciones = consultar_contradicciones(persona)
    if contradicciones:
        for lugar_dicho, hora_dicha, lugar_registro, hora_registro in contradicciones:
            escribir(area, f"• Dijo estar en {lugar_dicho} a las {hora_dicha}, pero según el registro estuvo en {lugar_registro} a las {hora_registro}.\n", "item")
    else:
        escribir(area, "• Ninguna.\n", "item")

    escribir(area, "Descarte\n", "titulo")
    if consultar_descarte(persona):
        escribir(area, "• Puede descartarse como responsable.\n", "item")
    else:
        escribir(area, "• No se puede descartar con la información disponible.\n", "item")

"""
* Objetivo: Muestra el informe de investigar para la persona seleccionada.
* Entradas: Lista de personas y área de resultados.
* Salidas: Ninguna; escribe el informe en el área.
* Restricciones: Debe haber una persona seleccionada.
"""
def investigar(combo_persona, area):
    persona = combo_persona.get()
    if not persona:
        mostrar_aviso("Seleccione una persona para investigarla.")
        return
    limpiar(area)
    escribir(area, consultar_investigacion(persona).strip() + "\n")

"""
* Objetivo: Muestra las explicaciones lógicas de la persona seleccionada.
* Entradas: Lista de personas y área de resultados.
* Salidas: Ninguna; escribe las explicaciones en el área.
* Restricciones: Debe haber una persona seleccionada.
"""
def ver_explicaciones(combo_persona, area):
    persona = combo_persona.get()
    if not persona:
        mostrar_aviso("Seleccione una persona para ver sus explicaciones.")
        return
    limpiar(area)
    escribir(area, f"Explicaciones sobre {persona}\n", "titulo")
    for explicacion in consultar_explicaciones(persona):
        escribir(area, f"• {explicacion}\n", "item")

"""
* Objetivo: Muestra la lista de posibles sospechosos inferida por Prolog.
* Entradas: Área de resultados.
* Salidas: Ninguna; escribe la lista en el área.
* Restricciones: Ninguna.
"""
def ver_sospechosos(area):
    limpiar(area)
    sospechosos = consultar_sospechosos()
    if sospechosos:
        escribir(area, "Posibles sospechosos\n", "titulo")
        for persona in sospechosos:
            escribir(area, f"• {persona}\n", "item")
    else:
        escribir(area, "No se encontraron posibles sospechosos.")

"""
* Objetivo: Muestra todas las contradicciones encontradas en el caso.
* Entradas: Área de resultados.
* Salidas: Ninguna; escribe las contradicciones en el área.
* Restricciones: Ninguna.
"""
def ver_contradicciones(area):
    limpiar(area)
    contradicciones = consultar_todas_contradicciones()
    if contradicciones:
        escribir(area, "Contradicciones encontradas en el caso\n", "titulo")
        for persona, lugar_dicho, hora_dicha, lugar_registro, hora_registro in contradicciones:
            escribir(area, f"• {persona}: dijo estar en {lugar_dicho} a las {hora_dicha}, pero según el registro estuvo en {lugar_registro} a las {hora_registro}.\n", "item")
    else:
        escribir(area, "No se encontraron contradicciones.")

"""
* Objetivo: Muestra la sección de análisis de sospechosos.
* Entradas: Contenedor.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def mostrar_sospechosos(padre):
    lienzo = pantalla_seccion(padre, "ANÁLISIS DE SOSPECHOSOS", "sospechosos")

    evento = consultar_evento()
    if evento:
        _, _, _, inicio, fin = evento
        etiqueta(lienzo, 1045, 172, f"Intervalo: {inicio} a {fin}")

    etiqueta(lienzo, 290, 172, "Persona")
    combo_persona = crear_lista(lienzo, consultar_personas())
    colocar(lienzo, combo_persona, 290, 186, 170, 32)

    area = crear_area_resultado(lienzo, 290, 228, 935, 454)
    colocar(lienzo, crear_boton(lienzo, "Analizar", lambda: analizar(combo_persona, area)), 470, 186, 95, 32)
    colocar(lienzo, crear_boton(lienzo, "Investigar", lambda: investigar(combo_persona, area)), 573, 186, 100, 32)
    colocar(lienzo, crear_boton(lienzo, "Explicaciones", lambda: ver_explicaciones(combo_persona, area)), 681, 186, 120, 32)
    colocar(lienzo, crear_boton_kraft(lienzo, "Sospechosos", lambda: ver_sospechosos(area)), 809, 186, 115, 32)
    colocar(lienzo, crear_boton_kraft(lienzo, "Contradicciones", lambda: ver_contradicciones(area)), 932, 186, 130, 32)
    colocar(lienzo, crear_boton_kraft(lienzo, "Limpiar", lambda: limpiar(area)), 1070, 186, 85, 32)