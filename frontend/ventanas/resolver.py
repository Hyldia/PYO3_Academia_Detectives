from consultas import consultar_resolucion
from ventanas.estilos import COLOR_TARJETA, colocar, crear_area_resultado, crear_boton, crear_boton_kraft, crear_lienzo, escribir, limpiar, mostrar_aviso
from ventanas.navegacion import ir_a

"""
* Objetivo: Ejecuta resolver_caso en Prolog y muestra su informe.
* Entradas: Área de resultados.
* Salidas: Ninguna; escribe el informe en el área.
* Restricciones: El predicado resolver_caso debe existir en Prolog.
"""
def resolver(area):
    informe = consultar_resolucion()
    if informe is None:
        mostrar_aviso("Esta opción estará disponible cuando resolver_caso esté listo en Prolog.", "EN CONSTRUCCIÓN")
        return
    limpiar(area)
    escribir(area, informe)

"""
* Objetivo: Muestra la pantalla para resolver el caso.
* Entradas: Contenedor.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def mostrar_resolver(padre):
    lienzo = crear_lienzo(padre, "fondo_resolver.png")
    lienzo.create_text(633, 130, text="RESOLVER CASO", font=("Impact", 30), fill=COLOR_TARJETA)

    area = crear_area_resultado(lienzo, 318, 205, 577, 355, COLOR_TARJETA, 0)
    escribir(area, 'Presione "Resolver caso" para ver la conclusión del sistema.')
    colocar(lienzo, crear_boton(lienzo, "Resolver caso", lambda: resolver(area)), 420, 575, 200, 40)
    colocar(lienzo, crear_boton_kraft(lienzo, "Volver al inicio", lambda: ir_a("portada")), 640, 575, 200, 40)