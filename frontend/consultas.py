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