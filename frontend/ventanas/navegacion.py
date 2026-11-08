from ventanas.estilos import COLOR_ACENTO, COLOR_TARJETA, colocar, crear_boton, crear_boton_kraft, crear_lienzo, placa

# Botones del menú lateral, texto y pantallas que pertenecen a ese botón (la primera es la que abre)
MENU = [
    ("Inicio", ["portada"]),
    ("Consultas", ["accesos", "ubicaciones", "evidencias"]),
    ("Expediente", ["sospechosos"]),
    ("Resolver caso", ["resolver"]),
]

# Pestañas de la sección Consultas: texto y nombre de la pantalla
CONSULTAS = [
    ("Accesos", "accesos"),
    ("Ubicaciones", "ubicaciones"),
    ("Evidencias", "evidencias"),
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
* Objetivo: Crea un botón del menú o de las pestañas, resaltado si es la pantalla actual
* Entradas: Lienzo, texto, pantalla a la que lleva y si está activo
* Salidas: El botón creado, sin colocar.
* Restricciones: El botón activo no hace nada al presionarlo
"""
def boton_menu(lienzo, texto, nombre, activo):
    if activo:
        return crear_boton(lienzo, texto, lambda: None, COLOR_ACENTO, "white", COLOR_ACENTO)
    return crear_boton_kraft(lienzo, texto, lambda: ir_a(nombre))

"""
* Objetivo: Crea la base de una sección: fondo, título y menú lateral
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
    for texto, nombres in MENU:
        colocar(lienzo, boton_menu(lienzo, texto, nombres[0], activa in nombres), 16, y, 164, 40)
        y += 54
    colocar(lienzo, crear_boton(lienzo, "Salir", padre.destroy), 16, 640, 164, 40)

    # Las pantallas de consulta comparten pestañas para cambiar entre ellas
    if activa in [nombre for _, nombre in CONSULTAS]:
        x = 290
        for texto, nombre in CONSULTAS:
            colocar(lienzo, boton_menu(lienzo, texto, nombre, nombre == activa), x, 162, 140, 36)
            x += 150
    return lienzo