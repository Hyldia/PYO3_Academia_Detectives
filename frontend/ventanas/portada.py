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
    lienzo.create_text(645, 256, text="ACADEMIA DE DETECTIVES", font=("Impact", 36), fill=COLOR_ROJO)

    evento = consultar_evento()
    if evento:
        nombre, lugar, hora, inicio, fin = evento
        lienzo.create_text(645, 298, text=f"Caso: {nombre}  ·  {lugar}  ·  {hora}", font=("Segoe UI", 12, "bold"), fill=COLOR_TEXTO)
        lienzo.create_text(645, 322, text=f"Intervalo que se analiza: {inicio} a {fin}", font=("Segoe UI", 10), fill=COLOR_TEXTO)

    colocar(lienzo, crear_boton(lienzo, "Consultas", lambda: ir_a("accesos")), 445, 385, 200, 50)
    colocar(lienzo, crear_boton(lienzo, "Expediente", lambda: ir_a("sospechosos")), 665, 385, 200, 50)
    colocar(lienzo, crear_boton(lienzo, "Resolver caso", lambda: ir_a("resolver")), 555, 450, 200, 50)
    colocar(lienzo, crear_boton_kraft(lienzo, "Salir", padre.destroy), 555, 515, 200, 40)