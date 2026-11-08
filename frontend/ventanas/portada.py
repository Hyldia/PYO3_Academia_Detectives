from consultas import consultar_evento
from ventanas.estilos import COLOR_ROJO, COLOR_TEXTO, colocar, crear_boton, crear_boton_kraft, crear_lienzo, placa
from ventanas.navegacion import ir_a

"""
* Objetivo: Muestra la pantalla de inicio con el menú principal.
* Entradas: Contenedor.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def mostrar_portada(padre):
    lienzo = crear_lienzo(padre, "fondo_portada.png")

    # Placa clara para que el título se lea sobre el papel manchado
    placa(lienzo, 345, 222, 600, 118, (246, 235, 210, 235))
    lienzo.create_text(645, 262, text="ACADEMIA DE DETECTIVES", font=("Impact", 36), fill=COLOR_ROJO)

    evento = consultar_evento()
    if evento:
        nombre, lugar, hora, _, _ = evento
        lienzo.create_text(645, 312, text=f"Caso: {nombre}  ·  {lugar}  ·  {hora}", font=("Segoe UI", 12, "bold"), fill=COLOR_TEXTO)

    colocar(lienzo, crear_boton(lienzo, "Consultar Accesos", lambda: ir_a("accesos")), 445, 380, 200, 50)
    colocar(lienzo, crear_boton(lienzo, "Consultar Ubicaciones", lambda: ir_a("ubicaciones")),  665, 380, 200, 50)
    colocar(lienzo, crear_boton(lienzo, "Consultar Evidencias", lambda: ir_a("evidencias")), 445, 445, 200, 50)
    colocar(lienzo, crear_boton(lienzo, "Consultar Sospechosos", lambda: ir_a("sospechosos")), 665, 445, 200, 50)
    colocar(lienzo, crear_boton(lienzo, "Resolver Caso", lambda: ir_a("resolver")), 555, 520, 200, 50)
    colocar(lienzo, crear_boton_kraft(lienzo, "Salir", padre.destroy), 555, 585, 200, 40)
    