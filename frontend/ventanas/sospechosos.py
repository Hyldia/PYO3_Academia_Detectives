from consultas import (consultar_contradicciones, consultar_declaraciones, consultar_detalle_evidencias, consultar_evento,
                    consultar_motivos_acceso, consultar_personas, consultar_recorrido)
from ventanas.estilos import (COLOR_ACENTO, colocar, crear_area_resultado, crear_boton, crear_boton_kraft, crear_lista, escribir,
                            etiqueta, mostrar_aviso)
from ventanas.navegacion import ir_a, pantalla_seccion

TARJETA_DECISION = 5

# Opciones que tiene el jugador y cómo se muestran
NOMBRES_DECISION = {
    "responsable": "Posible responsable",
    "descartada": "Descartada",
    "en_investigacion": "Mantener en investigación",
}

# La persona abierta y la tarjeta actual
estado = {"persona": None, "tarjeta": 0}

# Lo que el jugador marcó para cada persona; Resolver caso lo muestra al final
decisiones = {}

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
    estado.update(persona=persona, tarjeta=0)
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
* Objetivo: Guarda la decisión del jugador sobre la persona abierta, sin decirle si acertó.
* Entradas: Decisión (responsable o descartada).
* Salidas: Ninguna.
* Restricciones: Debe haber un expediente abierto.
"""
def decidir(decision):
    decisiones[estado["persona"]] = decision
    ir_a("sospechosos")

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
* Objetivo: Muestra los accesos de la persona y cómo los obtiene.
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
* Objetivo: Muestra lo que declaró la persona.
* Entradas: Área y persona.
* Salidas: Ninguna.
* Restricciones: La coartada no se muestra aquí para no dar la respuesta; se ve en Resolver caso.
"""
def tarjeta_testimonio(area, persona):
    escribir(area, f"Testimonio de {persona}\n", "titulo")
    declaraciones = consultar_declaraciones(persona)
    for lugar, hora in declaraciones:
        escribir(area, f"• Declaró estar en {lugar} a las {hora}.\n", "item")
    if not declaraciones:
        escribir(area, "• No dio ningún testimonio.\n", "item")

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
* Objetivo: Pide al jugador su conclusión y muestra la que ya guardó.
* Entradas: Área y persona.
* Salidas: Ninguna.
* Restricciones: No compara con el sistema; eso se ve en Resolver caso.
"""
def tarjeta_decision(area, persona):
    escribir(area, "Su conclusión\n", "titulo")
    escribir(area, f"Con lo que revisó, ¿qué concluye sobre {persona}?\n\n")
    escribir(area, "• Posible responsable: tuvo oportunidad y hay indicios en su contra.\n", "item")
    escribir(area, "• Descartada: la información demuestra que no pudo participar.\n", "item")
    escribir(area, "• Mantener en investigación: no hay suficientes pruebas para responsabilizarla ni para descartarla.\n", "item")
    decision = decisiones.get(persona)
    if decision:
        escribir(area, "\n")
        escribir(area, f" Decisión guardada: {NOMBRES_DECISION[decision]} \n", "neutro")
        escribir(area, "Puede cambiarla cuando quiera. En Resolver caso verá lo que deduce el sistema.\n")

TARJETAS = [tarjeta_recorrido, tarjeta_accesos, tarjeta_evidencias, tarjeta_testimonio, tarjeta_contradicciones, tarjeta_decision]

"""
* Objetivo: Coloca los botones que corresponden a la tarjeta actual.
* Entradas: Lienzo, número de tarjeta y persona.
* Salidas: Ninguna.
* Restricciones: En la tarjeta de decisión, el botón elegido se resalta.
"""
def colocar_navegacion(lienzo, numero, persona):
    if numero > 0:
        colocar(lienzo, crear_boton_kraft(lienzo, "Anterior", lambda: cambiar_tarjeta(numero - 1)), 290, 640, 130, 36)
    if numero < TARJETA_DECISION:
        colocar(lienzo, crear_boton(lienzo, "Siguiente", lambda: cambiar_tarjeta(numero + 1)), 1095, 640, 130, 36)
        return
    x = 500
    for decision, texto in NOMBRES_DECISION.items():
        if decisiones.get(persona) == decision:
            boton = crear_boton(lienzo, texto, lambda d=decision: decidir(d), COLOR_ACENTO, "white", COLOR_ACENTO)
        else:
            boton = crear_boton(lienzo, texto, lambda d=decision: decidir(d))
        colocar(lienzo, boton, x, 640, 200, 36)
        x += 215

"""
* Objetivo: Muestra el expediente de investigación por tarjetas.
* Entradas: Contenedor.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def mostrar_sospechosos(padre):
    lienzo = pantalla_seccion(padre, "EXPEDIENTE DE INVESTIGACIÓN", "sospechosos")

    evento = consultar_evento()
    if evento:
        nombre, lugar, hora, inicio, fin = evento
        etiqueta(lienzo, 660, 202, f"Evento: {nombre} · {lugar} · {hora} · intervalo {inicio} a {fin}")

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
        escribir(area, "Elija una persona y abra su expediente. Revise cada tarjeta y relacione los datos con el evento. "
                    "En la última tarjeta marque si la considera posible responsable, si la descarta o si la mantiene en investigación. "
                    "Al final, en Resolver caso, verá lo que usted marcó junto con lo que deduce el sistema.\n")
        return

    numero = estado["tarjeta"]
    etiqueta(lienzo, 660, 172, f"Tarjeta {numero + 1} de {TARJETA_DECISION + 1}")
    TARJETAS[numero](area, persona)
    colocar_navegacion(lienzo, numero, persona)