# Modulo que conecta el frontend con la base de conocimiento de Prolog.

# Importa la interfaz que permite ejecutar consultas de Prolog desde Python.
from pyswip import Prolog

# Crea la instancia de Prolog que se usara para realizar las consultas.
prolog = Prolog()
prolog.consult("../backend/predicados.pl")

"""
* Objetivo:Consulta los lugares a los que tiene acceso una persona.
"""
def consultar_accesos(persona):
    resultados =[]
    # Busca en Prolog los lugares a los que tiene acceso la persona.
    for resultado in prolog.query(f"tiene_acceso({persona}, Lugar)"):
        resultados.append(resultado["Lugar"]) # Agrega a la lista el lugar del resultado actual.
    return resultados

"""
* Objetivo:Consulta las evidencias relacionadas con una persona.
"""
def consultar_evidencias(persona):
    resultado = []
    # Busca en Prolog las evidencias relacionadas con la persona.
    for evidencia in prolog.query(f"evidencias_de({persona}, Evidencia)"):
        resultado.append(evidencia["Evidencia"]) # Agrega a la lista la evidencia del resultado actual.
    return resultado

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