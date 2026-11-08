from ventanas.estilos import COLOR_ACENTO, COLOR_TARJETA, colocar, crear_boton, crear_boton_kraft, crear_lienzo, placa

# Botones del menú lateral: texto y nombre de la pantalla
MENU = [
    ("Inicio", "portada"),
    ("Accesos", "accesos"),
    ("Ubicaciones", "ubicaciones"),
    ("Evidencias", "evidencias"),
    ("Sospechosos", "sospechosos"),
    ("Resolver Caso", "resolver"),
]

raiz = None
pantallas = {}

"""
* Objetivo: Guarda la ventana principal y las pantallas del programa.
* Entradas: Ventana y diccionario con el nombre y la función de cada pantalla.
* Salidas: Ninguna.
* Restricciones: Debe llamarse antes de usar ir_a.
"""
def iniciar(ventana, lista_pantallas):
    global raiz
    raiz = ventana
    pantallas.update(lista_pantallas)

"""
* Objetivo: Cambia a otra pantalla.
* Entradas: Nombre de la pantalla.
* Salidas: Ninguna.
* Restricciones: La pantalla debe estar registrada en iniciar.
"""
def ir_a(nombre):
    for widget in raiz.winfo_children(): # Limpia la pantalla anterior
        widget.destroy()
    pantallas[nombre](raiz)

"""
* Objetivo: Crea la base de una sección: fondo, título y menú lateral.
* Entradas: Contenedor, título y nombre de la pantalla activa.
* Salidas: El lienzo para agregar los controles de la sección.
* Restricciones: El nombre debe coincidir con uno de MENU.
"""
def pantalla_seccion(padre, titulo, activa):
    lienzo = crear_lienzo(padre, "fondo_seccion.png")

    # Placa oscura para que el título se lea sobre la tarjeta
    placa(lienzo, 254, 44, 184, 92)
    lienzo.create_text(346, 90, text=titulo, width=168, justify="center", font=("Segoe UI", 13, "bold"), fill=COLOR_TARJETA)

    y = 30
    for texto, nombre in MENU:
        if nombre == activa:
            boton = crear_boton(lienzo, texto, lambda: None, COLOR_ACENTO, "white", COLOR_ACENTO)
        else:
            boton = crear_boton_kraft(lienzo, texto, lambda n=nombre: ir_a(n))
        colocar(lienzo, boton, 16, y, 164, 40)
        y += 54

    colocar(lienzo, crear_boton(lienzo, "Salir", padre.destroy), 16, 640, 164, 40)
    return lienzo