# Modulo que conecta el frontend con la base de conocimiento de Prolog.

# Importa la interfaz que permite ejecutar consultas de Prolog desde Python.
from pyswip import Prolog

# Crea la instancia de Prolog que se usara para realizar las consultas.
prolog = Prolog()
prolog.consult("../backend/predicados.pl")

# Consulta los lugares a los que tiene acceso una persona.
def consultar_accesos(persona):
    resultados =[]
    # Busca en Prolog los lugares a los que tiene acceso la persona.
    for resultado in prolog.query(f"tiene_acceso({persona}, Lugar)"):
        resultados.append(resultado["Lugar"]) # Agrega a la lista el lugar del resultado actual.
    return resultados