# Modulo que conecta el frontend con la base de conocimiento de Prolog.

# Importa la interfaz que permite ejecutar consultas de Prolog desde Python.
from pyswip import Prolog

# Crea la instancia de Prolog que se usara para realizar las consultas.
prolog = Prolog()
prolog.consult("../backend/predicados.pl")

"""
* Objetivo: Consulta los lugares a los que tiene acceso una persona, sin repetidos.
"""
def consultar_accesos(persona):
    # setof devuelve la lista sin repetidos y falla si no hay lugares
    resultado = list(prolog.query(f"setof(Lugar, tiene_acceso({persona}, Lugar), Lugares)", maxresult=1))
    if resultado:
        return resultado[0]["Lugares"]
    return []

"""
* Objetivo: Consulta las evidencias relacionadas con una persona.
"""
def consultar_evidencias(persona):
    resultado = list(prolog.query(f"evidencias_de({persona}, Evidencias)", maxresult=1))
    if resultado:
        return resultado[0]["Evidencias"]
    return []

"""
* Objetivo:Consulta los movimientos de una persona en un lugar durante un periodo de tiempo.
"""
def consultar_movimientos(persona, lugar, inicio, fin):
    consulta = list(prolog.query(f"estuvo_en_intervalo({persona}, {lugar}, {inicio}, {fin})")) # Convierte el resultado de la consulta en una lista.
    if consulta: 
        return f"{persona} estuvo en {lugar} entre {inicio} y {fin}." # Retorna un mensaje indicando que la persona estuvo en el lugar durante el periodo especificado.
    else:
        return f"{persona} no estuvo en {lugar} entre {inicio} y {fin}." # Retorna un mensaje indicando que la persona no estuvo en el lugar durante el periodo especificado.


# Interfaz de sospechosos

"""
* Objetivo: Indica si una consulta de Prolog tiene al menos una solución.
"""
def se_cumple(consulta):
    return len(list(prolog.query(consulta, maxresult=1))) > 0

"""
* Objetivo: Consulta las personas definidas en la base de conocimiento.
"""
def consultar_personas():
    personas = []
    for resultado in prolog.query("persona(Persona)"):
        personas.append(resultado["Persona"])
    return personas

"""
* Objetivo: Consulta el evento central del caso y el intervalo que se analiza.
"""
def consultar_evento():
    resultado = list(prolog.query("evento(Nombre, Lugar, Hora), intervalo_evento(Inicio, Fin)", maxresult=1))
    if resultado:
        r = resultado[0]
        return (r["Nombre"], r["Lugar"], r["Hora"], r["Inicio"], r["Fin"])
    return None

"""
* Objetivo: Consulta las personas que el sistema infiere como posibles sospechosos.
"""
def consultar_sospechosos():
    resultados = []
    for resultado in prolog.query("posible_sospechoso(Persona)"):
        resultados.append(resultado["Persona"])
    return resultados

"""
* Objetivo: Consulta las contradicciones entre los testimonios de una persona y sus registros.
"""
def consultar_contradicciones(persona):
    resultados = []
    for r in prolog.query(f"contradiccion({persona}, LugarDicho, HoraDicha, LugarRegistro, HoraRegistro)"):
        resultados.append((r["LugarDicho"], r["HoraDicha"], r["LugarRegistro"], r["HoraRegistro"]))
    return resultados

"""
* Objetivo: Consulta todas las contradicciones encontradas en el caso.
"""
def consultar_todas_contradicciones():
    resultados = []
    for r in prolog.query("contradiccion(Persona, LugarDicho, HoraDicha, LugarRegistro, HoraRegistro)"):
        resultados.append((r["Persona"], r["LugarDicho"], r["HoraDicha"], r["LugarRegistro"], r["HoraRegistro"]))
    return resultados

"""
* Objetivo: Consulta la coartada válida de una persona, si existe.
"""
def consultar_coartada(persona):
    resultado = list(prolog.query(f"coartada({persona}, Lugar, Hora)", maxresult=1))
    if resultado:
        return (resultado[0]["Lugar"], resultado[0]["Hora"])
    return None

"""
* Objetivo: Consulta los resultados de inferencia que justifican si una persona es posible sospechosa.
"""
def consultar_inferencia(persona):
    evidencias = []
    for resultado in prolog.query(f"evidencia_en_escena({persona}, Evidencia)"):
        evidencias.append(resultado["Evidencia"])
    return {
        "sospechoso": se_cumple(f"posible_sospechoso({persona})"),
        "en_escena": se_cumple(f"estuvo_en_escena({persona})"),
        "acceso": se_cumple(f"acceso_a_escena({persona})"),
        "evidencias": evidencias,
        "contradiccion_evento": se_cumple(f"contradiccion_en_evento({persona})"),
    }

    
"""
* Objetivo: Consulta los lugares del caso.
* Entradas: Ninguna.
* Salidas: Lista de lugares.
* Restricciones: Acepta lugar/1 y lugar/2, porque hechos.pl puede usar cualquiera.
"""
def consultar_lugares():
    consulta = "findall(L, ((current_predicate(lugar/2), lugar(L, _)) ; (current_predicate(lugar/1), lugar(L))), Lugares)"
    resultado = list(prolog.query(consulta, maxresult=1))
    if resultado:
        return resultado[0]["Lugares"]
    return []

"""
* Objetivo: Ejecuta resolver_caso y devuelve el informe que imprime.
* Entradas: Ninguna.
* Salidas: El informe, o None si resolver_caso todavía no existe.
* Restricciones: El informe lo arma Prolog; Python solo lo recibe.
"""
def consultar_resolucion():
    if not se_cumple("current_predicate(resolver_caso/0)"):
        return None
    resultado = list(prolog.query("with_output_to(atom(Texto), resolver_caso)", maxresult=1))
    if resultado:
        return resultado[0]["Texto"]
    return "No se pudo resolver el caso con la información disponible."

    
"""
* Objetivo: Ejecuta investigar en Prolog y devuelve el informe que imprime.
* Entradas: Persona.
* Salidas: El informe de la persona.
* Restricciones: El informe lo arma Prolog; Python solo lo recibe.
"""
def consultar_investigacion(persona):
    resultado = list(prolog.query(f"with_output_to(atom(Texto), investigar({persona}))", maxresult=1))
    if resultado:
        return resultado[0]["Texto"]
    return f"No se encontró información de {persona}."

"""
* Objetivo: Consulta todas las explicaciones lógicas sobre una persona
* Entradas: Persona.
* Salidas: Lista de explicaciones
* Restricciones: Cada explicación la genera Prolog por backtracking
"""
def consultar_explicaciones(persona):
    explicaciones = []
    for resultado in prolog.query(f"explicaciones({persona}, Explicacion)"):
        explicaciones.append(resultado["Explicacion"])
    return explicaciones

"""
* Objetivo: Consulta si una persona puede descartarse
* Entradas: Persona
* Salidas: Verdadero si Prolog la descarta
* Restricciones: La decisión la toma Prolog
"""
def consultar_descarte(persona):
    return se_cumple(f"descartar({persona})")


"""
* Objetivo: Consulta el recorrido de una persona.
* Entradas: Persona.
* Salidas: Lista de pares (hora, lugar) ordenada por hora.
* Restricciones: Ninguna.
"""
def consultar_recorrido(persona):
    recorrido = []
    for r in prolog.query(f"estuvo({persona}, Lugar, Hora)"):
        recorrido.append((r["Hora"], r["Lugar"]))
    return sorted(recorrido)

"""
* Objetivo: Consulta cómo obtiene una persona acceso a cada lugar.
* Entradas: Persona.
* Salidas: Lista de motivos de acceso.
* Restricciones: Los motivos los arma Prolog.
"""
def consultar_motivos_acceso(persona):
    motivos = []
    for r in prolog.query(f"motivo_acceso({persona}, Lugar, Motivo)"):
        motivos.append(r["Motivo"])
    return motivos

"""
* Objetivo: Consulta las evidencias de una persona con su lugar y hora.
* Entradas: Persona.
* Salidas: Lista de tuplas (evidencia, lugar, hora).
* Restricciones: Ninguna.
"""
def consultar_detalle_evidencias(persona):
    evidencias = []
    for r in prolog.query(f"detalle_evidencia({persona}, Evidencia, Lugar, Hora)"):
        evidencias.append((r["Evidencia"], r["Lugar"], r["Hora"]))
    return evidencias

"""
* Objetivo: Consulta lo que una persona declaró.
* Entradas: Persona.
* Salidas: Lista de pares (lugar, hora).
* Restricciones: Ninguna.
"""
def consultar_declaraciones(persona):
    declaraciones = []
    for r in prolog.query(f"declaracion({persona}, Lugar, Hora)"):
        declaraciones.append((r["Lugar"], r["Hora"]))
    return declaraciones

"""
* Objetivo: Consulta la clasificación que Prolog infiere para una persona.
* Entradas: Persona.
* Salidas: responsable, descartada o en_investigacion.
* Restricciones: La decisión la toma Prolog.
"""
def consultar_clasificacion(persona):
    resultado = list(prolog.query(f"clasificacion({persona}, Resultado)", maxresult=1))
    if resultado:
        return resultado[0]["Resultado"]
    return "en_investigacion"

"""
* Objetivo: Consulta si la decisión del jugador coincide con la de Prolog.
* Entradas: Persona y decisión.
* Salidas: Verdadero si coincide.
* Restricciones: La comparación la hace Prolog.
"""
def consultar_decision(persona, decision):
    return se_cumple(f"decision_correcta({persona}, {decision})")