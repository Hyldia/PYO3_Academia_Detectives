from consultas import (consultar_clasificacion, consultar_coartada, consultar_contradicciones, consultar_declaraciones,
                       consultar_decision, consultar_detalle_evidencias, consultar_evento, consultar_explicaciones,
                       consultar_investigacion, consultar_motivos_acceso, consultar_personas, consultar_recorrido)
from ventanas.estilos import colocar, crear_area_resultado, crear_boton, crear_boton_kraft, crear_lista, escribir, etiqueta, mostrar_aviso
from ventanas.navegacion import ir_a, pantalla_seccion

TARJETA_DECISION = 5
TARJETA_RESULTADO = 6
TARJETA_INFORME = 7

NOMBRES_RESULTADO = {
    "responsable": "posible responsable",
    "descartada": "descartada",
    "en_investigacion": "sigue en investigación",
}

# La persona abierta, la tarjeta actual y la decisión del jugador
estado = {"persona": None, "tarjeta": 0, "decision": None}

"""
* Objetivo: Abre el expediente de la persona seleccionada.
* Entradas: Lista de personas.
* Salidas: Ninguna; muestra la primera tarjeta.
* Restricciones: Debe haber una persona seleccionada.
"""
def abrir_expediente(combo_persona):
    persona = combo_persona.get()
    if not persona:
        mostrar_aviso("Seleccione una persona para abrir su expediente.")
        return
    estado.update(persona=persona, tarjeta=0, decision=None)
    ir_a("sospechosos")

"""
* Objetivo: Cambia a otra tarjeta del expediente.
* Entradas: Número de la tarjeta.
* Salidas: Ninguna.
* Restricciones: Debe haber un expediente abierto.
"""
def cambiar_tarjeta(numero):
    estado["tarjeta"] = numero
    ir_a("sospechosos")

"""
* Objetivo: Guarda la decisión del jugador y muestra el resultado.
* Entradas: Decisión (responsable, descartada o en_investigacion).
* Salidas: Ninguna.
* Restricciones: Debe haber un expediente abierto.
"""
def decidir(decision):
    estado["decision"] = decision
    cambiar_tarjeta(TARJETA_RESULTADO)

"""
* Objetivo: Muestra el recorrido registrado de la persona.
* Entradas: Área y persona.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def tarjeta_recorrido(area, persona):
    escribir(area, f"Recorrido de {persona}\n", "titulo")
    recorrido = consultar_recorrido(persona)
    for hora, lugar in recorrido:
        escribir(area, f"• A las {hora} estuvo en {lugar}.\n", "item")
    if not recorrido:
        escribir(area, "• No hay movimientos registrados.\n", "item")

"""
* Objetivo: Muestra los accesos de la persona.
* Entradas: Área y persona.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def tarjeta_accesos(area, persona):
    escribir(area, f"Accesos de {persona}\n", "titulo")
    motivos = consultar_motivos_acceso(persona)
    for motivo in motivos:
        escribir(area, f"• {motivo}.\n", "item")
    if not motivos:
        escribir(area, "• No tiene acceso a ningún lugar.\n", "item")

"""
* Objetivo: Muestra las evidencias relacionadas con la persona.
* Entradas: Área y persona.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def tarjeta_evidencias(area, persona):
    escribir(area, f"Evidencias de {persona}\n", "titulo")
    evidencias = consultar_detalle_evidencias(persona)
    for evidencia, lugar, hora in evidencias:
        escribir(area, f"• {evidencia}: hallada en {lugar} a las {hora}.\n", "item")
    if not evidencias:
        escribir(area, "• No hay evidencias relacionadas.\n", "item")

"""
* Objetivo: Muestra lo que declaró la persona y si tiene coartada.
* Entradas: Área y persona.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def tarjeta_testimonio(area, persona):
    escribir(area, f"Testimonio de {persona}\n", "titulo")
    declaraciones = consultar_declaraciones(persona)
    for lugar, hora in declaraciones:
        escribir(area, f"• Declaró estar en {lugar} a las {hora}.\n", "item")
    if not declaraciones:
        escribir(area, "• No dio ningún testimonio.\n", "item")

    escribir(area, "Coartada\n", "titulo")
    coartada = consultar_coartada(persona)
    if coartada:
        lugar, hora = coartada
        escribir(area, f"• Su declaración en {lugar} a las {hora} está respaldada por el registro.\n", "item")
    else:
        escribir(area, "• No tiene una coartada válida.\n", "item")

"""
* Objetivo: Muestra las contradicciones de la persona.
* Entradas: Área y persona.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def tarjeta_contradicciones(area, persona):
    escribir(area, f"Contradicciones de {persona}\n", "titulo")
    contradicciones = consultar_contradicciones(persona)
    for lugar_dicho, hora_dicha, lugar_registro, hora_registro in contradicciones:
        escribir(area, f"• Dijo estar en {lugar_dicho} a las {hora_dicha}, pero según el registro estuvo en {lugar_registro} a las {hora_registro}.\n", "item")
    if not contradicciones:
        escribir(area, "• No se encontraron contradicciones.\n", "item")

"""
* Objetivo: Pide al jugador su conclusión.
* Entradas: Área y persona.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def tarjeta_decision(area, persona):
    escribir(area, "Su conclusión\n", "titulo")
    escribir(area, f"Con lo que revisó, ¿qué concluye sobre {persona}?\n\n")
    escribir(area, "• Posible responsable: tuvo oportunidad y hay indicios en su contra.\n", "item")
    escribir(area, "• Descartar: la información demuestra que no pudo ser.\n", "item")
    escribir(area, "• Seguir investigando: la información no alcanza para decidir.\n", "item")

"""
* Objetivo: Compara la decisión del jugador con la conclusión de Prolog.
* Entradas: Área y persona.
* Salidas: Ninguna.
* Restricciones: El jugador ya debe haber decidido.
"""
def tarjeta_resultado(area, persona):
    if consultar_decision(persona, estado["decision"]):
        escribir(area, " ¡Correcto! Su conclusión coincide con la del sistema. \n", "neutro")
    else:
        escribir(area, " Su conclusión no coincide con la del sistema. \n", "alerta")

    conclusion = NOMBRES_RESULTADO[consultar_clasificacion(persona)]
    escribir(area, f"Conclusión del sistema: {conclusion}\n", "titulo")
    escribir(area, "Explicaciones\n", "titulo")
    for explicacion in consultar_explicaciones(persona):
        escribir(area, f"• {explicacion}\n", "item")

"""
* Objetivo: Muestra el informe completo que genera investigar en Prolog.
* Entradas: Área y persona.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def tarjeta_informe(area, persona):
    escribir(area, consultar_investigacion(persona).strip() + "\n")

TARJETAS = [tarjeta_recorrido, tarjeta_accesos, tarjeta_evidencias, tarjeta_testimonio, tarjeta_contradicciones,
            tarjeta_decision, tarjeta_resultado, tarjeta_informe]

"""
* Objetivo: Coloca los botones que corresponden a la tarjeta actual.
* Entradas: Lienzo y número de tarjeta.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def colocar_navegacion(lienzo, numero):
    if numero > 0:
        colocar(lienzo, crear_boton_kraft(lienzo, "Anterior", lambda: cambiar_tarjeta(numero - 1)), 290, 640, 130, 36)
    if numero < TARJETA_DECISION:
        colocar(lienzo, crear_boton(lienzo, "Siguiente", lambda: cambiar_tarjeta(numero + 1)), 1095, 640, 130, 36)
    if numero == TARJETA_DECISION:
        colocar(lienzo, crear_boton(lienzo, "Posible responsable", lambda: decidir("responsable")), 450, 640, 230, 36)
        colocar(lienzo, crear_boton(lienzo, "Descartar", lambda: decidir("descartada")), 700, 640, 230, 36)
        colocar(lienzo, crear_boton(lienzo, "Seguir investigando", lambda: decidir("en_investigacion")), 950, 640, 230, 36)
    if numero == TARJETA_RESULTADO:
        colocar(lienzo, crear_boton(lienzo, "Informe completo", lambda: cambiar_tarjeta(TARJETA_INFORME)), 1065, 640, 160, 36)

"""
* Objetivo: Muestra el expediente de investigación.
* Entradas: Contenedor.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def mostrar_sospechosos(padre):
    lienzo = pantalla_seccion(padre, "EXPEDIENTE DE INVESTIGACIÓN", "sospechosos")

    evento = consultar_evento()
    if evento:
        nombre, lugar, hora, _, _ = evento
        etiqueta(lienzo, 660, 202, f"Evento: {nombre} en {lugar} a las {hora}")

    etiqueta(lienzo, 290, 172, "Persona a investigar")
    combo_persona = crear_lista(lienzo, consultar_personas())
    if estado["persona"]:
        combo_persona.set(estado["persona"])
    colocar(lienzo, combo_persona, 290, 186, 190, 32)
    colocar(lienzo, crear_boton(lienzo, "Abrir expediente", lambda: abrir_expediente(combo_persona)), 490, 186, 150, 32)

    area = crear_area_resultado(lienzo, 290, 228, 935, 400)
    persona = estado["persona"]
    if not persona:
        escribir(area, "Cómo investigar\n", "titulo")
        escribir(area, "Elija una persona y abra su expediente. Revise cada tarjeta, relacione los datos con el evento y decida al final qué concluye. Después, el sistema le mostrará su propia conclusión.\n")
        return

    numero = estado["tarjeta"]
    if numero <= TARJETA_DECISION:
        etiqueta(lienzo, 660, 172, f"Tarjeta {numero + 1} de {TARJETA_DECISION + 1}")
    TARJETAS[numero](area, persona)
    colocar_navegacion(lienzo, numero)