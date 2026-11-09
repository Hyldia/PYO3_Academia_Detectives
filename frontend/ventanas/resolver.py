from consultas import (consultar_clasificacion, consultar_coartada, consultar_descarte, consultar_explicaciones, consultar_inferencia,
                    consultar_personas, consultar_resolucion)
from ventanas.estilos import COLOR_TARJETA, COLOR_TEXTO, colocar, crear_area_resultado, crear_boton, crear_boton_kraft, crear_lienzo, escribir
from ventanas.navegacion import ir_a
from ventanas.sospechosos import NOMBRES_DECISION, decisiones

# Cómo se muestra la conclusión que deduce Prolog
NOMBRES_RESULTADO = {
    "responsable": "Posible responsable",
    "descartada": "Descartada",
    "en_investigacion": "Sigue en investigación",
}

# Tarjeta que se está viendo
estado = {"pagina": 0}

"""
* Objetivo: Arma la lista de tarjetas: dos por persona y el resumen al final.
* Entradas: Ninguna.
* Salidas: Lista de pares (tipo de tarjeta, persona).
* Restricciones: El resumen no tiene persona.
"""
def paginas():
    lista = []
    for persona in consultar_personas():
        lista.append(("jugador", str(persona)))
        lista.append(("sistema", str(persona)))
    lista.append(("resumen", None))
    return lista

"""
* Objetivo: Cambia a otra tarjeta de la resolución.
* Entradas: Número de la tarjeta.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def cambiar_pagina(numero):
    estado["pagina"] = numero
    ir_a("resolver")

"""
* Objetivo: Vuelve al inicio y deja la resolución lista para empezar desde la primera tarjeta.
* Entradas: Ninguna.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def volver_inicio():
    estado["pagina"] = 0
    ir_a("portada")

"""
* Objetivo: Convierte un valor verdadero o falso en texto.
* Entradas: Valor que devolvió Prolog.
* Salidas: "Sí" o "No".
* Restricciones: Solo da formato; no decide nada del caso.
"""
def si_no(valor):
    return "Sí" if valor else "No"

"""
* Objetivo: Muestra lo que marcó el jugador sobre una persona.
* Entradas: Área y persona.
* Salidas: Ninguna.
* Restricciones: No lo compara con el sistema.
"""
def tarjeta_jugador(area, persona):
    escribir(area, f"Su decisión sobre {persona}\n", "titulo")
    decision = decisiones.get(persona)
    if decision:
        escribir(area, "En el expediente, usted la marcó como:\n")
        escribir(area, f" {NOMBRES_DECISION[decision]} \n", "neutro")
    else:
        escribir(area, "No la marcó en el expediente.\n")
    escribir(area, "\nEn la siguiente tarjeta verá lo que deduce el sistema.\n")

"""
* Objetivo: Muestra lo que deduce Prolog sobre una persona.
* Entradas: Área y persona.
* Salidas: Ninguna.
* Restricciones: Todas las conclusiones vienen de Prolog; Python solo las muestra.
"""
def tarjeta_sistema(area, persona):
    inferencia = consultar_inferencia(persona)
    escribir(area, f"Deducción del sistema sobre {persona}\n", "titulo")

    escribir(area, "Oportunidad\n", "titulo")
    escribir(area, f"• Estuvo en la escena durante el evento: {si_no(inferencia['en_escena'])}\n", "item")
    escribir(area, f"• Tiene acceso al lugar del evento: {si_no(inferencia['acceso'])}\n", "item")

    escribir(area, "Indicios\n", "titulo")
    evidencias = ", ".join(str(evidencia) for evidencia in inferencia["evidencias"]) or "ninguna"
    escribir(area, f"• Evidencias halladas en la escena: {evidencias}\n", "item")
    escribir(area, f"• Se contradice durante el evento: {si_no(inferencia['contradiccion_evento'])}\n", "item")

    escribir(area, "Coartada\n", "titulo")
    coartada = consultar_coartada(persona)
    if coartada:
        lugar, hora = coartada
        escribir(area, f"• Declaró estar en {lugar} a las {hora} y el registro lo respalda.\n", "item")
    else:
        escribir(area, "• No tiene una coartada válida.\n", "item")

    escribir(area, "Conclusión\n", "titulo")
    escribir(area, f"• Cumple para ser posible sospechosa: {si_no(inferencia['sospechoso'])}\n", "item")
    escribir(area, f"• Se puede descartar: {si_no(consultar_descarte(persona))}\n", "item")
    resultado = str(consultar_clasificacion(persona))
    escribir(area, f" {NOMBRES_RESULTADO.get(resultado, resultado)} \n", "neutro")

    escribir(area, "Justificación\n", "titulo")
    for explicacion in consultar_explicaciones(persona):
        escribir(area, f"{explicacion}\n\n")

"""
* Objetivo: Muestra el resumen que arma resolver_caso en Prolog.
* Entradas: Área.
* Salidas: Ninguna.
* Restricciones: El predicado resolver_caso debe existir en Prolog.
"""
def tarjeta_resumen(area):
    informe = consultar_resolucion()
    if informe is None:
        escribir(area, "El predicado resolver_caso todavía no está disponible en Prolog.\n")
        return
    escribir(area, f"{str(informe).strip()}\n")

"""
* Objetivo: Muestra la resolución del caso por tarjetas.
* Entradas: Contenedor.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def mostrar_resolver(padre):
    lienzo = crear_lienzo(padre, "fondo_resolver.png")
    lienzo.create_text(633, 130, text="RESOLVER CASO", font=("Impact", 30), fill=COLOR_TARJETA)

    lista = paginas()
    numero = min(estado["pagina"], len(lista) - 1)
    tipo, persona = lista[numero]

    if tipo == "resumen":
        encabezado = "Resumen del caso"
    else:
        tarjeta = 1 if tipo == "jugador" else 2
        encabezado = f"{persona}  ·  persona {numero // 2 + 1} de {len(lista) // 2}  ·  tarjeta {tarjeta} de 2"
    lienzo.create_text(318, 212, text=encabezado, anchor="w", font=("Segoe UI", 11, "bold"), fill=COLOR_TEXTO)

    area = crear_area_resultado(lienzo, 318, 228, 577, 332, COLOR_TARJETA, 0)
    if tipo == "jugador":
        tarjeta_jugador(area, persona)
    elif tipo == "sistema":
        tarjeta_sistema(area, persona)
    else:
        tarjeta_resumen(area)

    if numero > 0:
        colocar(lienzo, crear_boton_kraft(lienzo, "Anterior", lambda: cambiar_pagina(numero - 1)), 318, 572, 130, 38)
    colocar(lienzo, crear_boton_kraft(lienzo, "Volver al inicio", volver_inicio), 532, 572, 150, 38)
    if numero < len(lista) - 1:
        colocar(lienzo, crear_boton(lienzo, "Siguiente", lambda: cambiar_pagina(numero + 1)), 765, 572, 130, 38)