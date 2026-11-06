# Modulo que conecta el frontend con la base de conocimiento de Prolog.

# Importa la interfaz que permite ejecutar consultas de Prolog desde Python.
from pyswip import Prolog

# Crea la instancia de Prolog que se usara para realizar las consultas.
prolog = Prolog()
prolog.consult("../backend/predicados.pl")

"""
* Objetivo: Consulta los lugares a los que tiene acceso una persona, sin repetidos.
* Entradas: Nombre de la persona.
* Salidas: Lista de lugares accesibles, o una lista vacia si no hay resultados.
* Restricciones: La persona debe ser un termino valido para la consulta de Prolog.
"""
def consultar_accesos(persona):
    # setof devuelve la lista sin repetidos y falla si no hay lugares
    resultado = list(prolog.query(f"setof(Lugar, tiene_acceso({persona}, Lugar), Lugares)", maxresult=1))
    if resultado:
        return resultado[0]["Lugares"]
    return []

"""
* Objetivo: Consulta las evidencias relacionadas con una persona.
* Entradas: Nombre de la persona.
* Salidas: Lista de evidencias, o una lista vacia si no hay resultados.
* Restricciones: La persona debe existir en la base de conocimiento.
"""
def consultar_evidencias(persona):
    resultado = list(prolog.query(f"evidencias_de({persona}, Evidencias)", maxresult=1))
    if resultado:
        return resultado[0]["Evidencias"]
    return []

"""
* Objetivo: Consulta si una persona estuvo en un lugar durante un periodo de tiempo.
* Entradas: Persona, lugar y horas de inicio y fin del periodo.
* Salidas: Mensaje que indica si la persona estuvo en ese lugar durante el periodo.
* Restricciones: Los valores deben ser compatibles con la consulta del predicado de Prolog.
"""
def consultar_movimientos(persona, lugar, inicio, fin):
    consulta = list(prolog.query(f"estuvo_en_intervalo({persona}, {lugar}, {inicio}, {fin})")) # Convierte el resultado de la consulta en una lista.
    if consulta: 
        return f"{persona} estuvo en {lugar} entre {inicio} y {fin}." # Retorna un mensaje indicando que la persona estuvo en el lugar durante el periodo especificado.
    else:
        return f"{persona} no estuvo en {lugar} entre {inicio} y {fin}." # Retorna un mensaje indicando que la persona no estuvo en el lugar durante el periodo especificado.


# Interfaz de sospechosos

"""
* Objetivo: Indica si una consulta de Prolog tiene al menos una solucion.
* Entradas: Consulta escrita en sintaxis de Prolog.
* Salidas: Verdadero si existe al menos una solucion; falso en caso contrario.
* Restricciones: La consulta debe ser valida en Prolog.
"""
def se_cumple(consulta):
    return len(list(prolog.query(consulta, maxresult=1))) > 0

"""
* Objetivo: Consulta las personas definidas en la base de conocimiento.
* Entradas: Ninguna.
* Salidas: Lista de personas obtenidas de los hechos persona/1.
* Restricciones: La base de conocimiento debe contener el predicado persona/1.
"""
def consultar_personas():
    personas = []
    for resultado in prolog.query("persona(Persona)"):
        personas.append(resultado["Persona"])
    return personas

"""
* Objetivo: Consulta el evento central del caso y el intervalo que se analiza.
* Entradas: Ninguna.
* Salidas: Tupla con el nombre, lugar y hora del evento, y el inicio y fin del intervalo; None si no hay resultados.
* Restricciones: La base de conocimiento debe definir evento/3 e intervalo_evento/2.
"""
def consultar_evento():
    resultado = list(prolog.query("evento(Nombre, Lugar, Hora), intervalo_evento(Inicio, Fin)", maxresult=1))
    if resultado:
        r = resultado[0]
        return (r["Nombre"], r["Lugar"], r["Hora"], r["Inicio"], r["Fin"])
    return None

"""
* Objetivo: Consulta las personas que el sistema infiere como posibles sospechosos.
* Entradas: Ninguna.
* Salidas: Lista de personas que cumplen posible_sospechoso/1.
* Restricciones: La base de conocimiento debe definir el predicado posible_sospechoso/1.
"""
def consultar_sospechosos():
    resultados = []
    for resultado in prolog.query("posible_sospechoso(Persona)"):
        resultados.append(resultado["Persona"])
    return resultados

"""
* Objetivo: Consulta las contradicciones entre los testimonios de una persona y sus registros.
* Entradas: Nombre de la persona.
* Salidas: Lista de tuplas con el lugar y hora declarados, y el lugar y hora registrados.
* Restricciones: La persona debe ser un termino valido para la consulta de Prolog.
"""
def consultar_contradicciones(persona):
    resultados = []
    for r in prolog.query(f"contradiccion({persona}, LugarDicho, HoraDicha, LugarRegistro, HoraRegistro)"):
        resultados.append((r["LugarDicho"], r["HoraDicha"], r["LugarRegistro"], r["HoraRegistro"]))
    return resultados

"""
* Objetivo: Consulta todas las contradicciones encontradas en el caso.
* Entradas: Ninguna.
* Salidas: Lista de tuplas con la persona, el lugar y hora declarados, y el lugar y hora registrados.
* Restricciones: La base de conocimiento debe definir el predicado contradiccion/5.
"""
def consultar_todas_contradicciones():
    resultados = []
    for r in prolog.query("contradiccion(Persona, LugarDicho, HoraDicha, LugarRegistro, HoraRegistro)"):
        resultados.append((r["Persona"], r["LugarDicho"], r["HoraDicha"], r["LugarRegistro"], r["HoraRegistro"]))
    return resultados

"""
* Objetivo: Consulta la coartada valida de una persona, si existe.
* Entradas: Nombre de la persona.
* Salidas: Tupla con el lugar y la hora de la coartada, o None si no se encuentra.
* Restricciones: La persona debe ser un termino valido para la consulta de Prolog.
"""
def consultar_coartada(persona):
    resultado = list(prolog.query(f"coartada({persona}, Lugar, Hora)", maxresult=1))
    if resultado:
        return (resultado[0]["Lugar"], resultado[0]["Hora"])
    return None

"""
* Objetivo: Consulta los resultados de inferencia que justifican si una persona es posible sospechosa.
* Entradas: Nombre de la persona.
* Salidas: Diccionario con el estado de sospechoso, presencia en escena, acceso, evidencias en escena y contradiccion con el evento.
* Restricciones: La persona debe ser un termino valido para las consultas de Prolog.
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
* Salidas: El informe, o None si resolver_caso todavia no existe.
* Restricciones: El informe lo arma Prolog; Python solo lo recibe.
"""
def consultar_resolucion():
    if not se_cumple("current_predicate(resolver_caso/0)"):
        return None
    resultado = list(prolog.query("with_output_to(atom(Texto), resolver_caso)", maxresult=1))
    if resultado:
        return resultado[0]["Texto"]
    return "No se pudo resolver el caso con la información disponible."