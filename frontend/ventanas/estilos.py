import tkinter as tk
from pathlib import Path
from tkinter import ttk

from PIL import Image, ImageDraw, ImageTk

# Tamaño fijo de la ventana
ANCHO_VENTANA = 1280
ALTO_VENTANA = 720

# Curvatura de las esquinas
RADIO_BOTON = 14
RADIO_CAMPO = 10
RADIO_AREA = 18

# Colores
COLOR_CAFE = "#4A2F1B"
COLOR_CAFE_HOVER = "#5F3F27"
COLOR_KRAFT = "#C9A874"
COLOR_KRAFT_HOVER = "#D8BB8C"
COLOR_ACENTO = "#A5561A"
COLOR_ROJO = "#8E241E"
COLOR_HOJA = "#EBE2B6"
COLOR_TARJETA = "#F6EBD2"
COLOR_BORDE = "#CDBE8E"
COLOR_TEXTO = "#3A2A1C"

RUTA_IMAGENES = Path(__file__).resolve().parent.parent / "imagenes"

# Tkinter borra una imagen si nadie la guarda, por eso se conservan aquí
imagenes = {}
ventana_principal = None

"""
* Objetivo: Carga una imagen de fondo y la ajusta al tamaño de la ventana.
* Entradas: Nombre del archivo.
* Salidas: La imagen lista para usar en tkinter.
* Restricciones: Debe existir en la carpeta imagenes y ya debe existir la ventana principal.
"""
def cargar_imagen(nombre):
    if nombre not in imagenes:
        imagen = Image.open(RUTA_IMAGENES / nombre).convert("RGB")
        imagenes[nombre] = ImageTk.PhotoImage(imagen.resize((ANCHO_VENTANA, ALTO_VENTANA), Image.LANCZOS))
    return imagenes[nombre]

"""
* Objetivo: Crea un rectángulo con esquinas curvas y bordes suaves.
* Entradas: Ancho, alto, radio de la curva, color y, opcionalmente, color y grosor del borde.
* Salidas: La imagen lista para usar en tkinter.
* Restricciones: El color puede ser "#RRGGBB" o (rojo, verde, azul, transparencia).
"""
def forma_redondeada(ancho, alto, radio, color, borde=None, grosor=1):
    clave = (ancho, alto, radio, color, borde, grosor)
    if clave not in imagenes:
        # Se dibuja 4 veces más grande y se reduce para suavizar las curvas
        k = 4
        forma = Image.new("RGBA", (ancho * k, alto * k), (0, 0, 0, 0))
        dibujo = ImageDraw.Draw(forma)
        dibujo.rounded_rectangle((0, 0, ancho * k - 1, alto * k - 1), radius=radio * k, fill=color, outline=borde, width=grosor * k if borde else 0)
        imagenes[clave] = ImageTk.PhotoImage(forma.resize((ancho, alto), Image.LANCZOS))
    return imagenes[clave]

"""
* Objetivo: Aplica el estilo de las listas de selección.
* Entradas: Ventana principal.
* Salidas: Ninguna.
* Restricciones: Debe llamarse antes de mostrar cualquier pantalla.
"""
def aplicar_estilos(ventana):
    global ventana_principal
    ventana_principal = ventana
    estilo = ttk.Style()
    estilo.theme_use("clam")
    # La lista va sin borde porque la curva la da el fondo redondeado
    estilo.configure("TCombobox", padding=2, borderwidth=0, relief="flat", bordercolor=COLOR_TARJETA, lightcolor=COLOR_TARJETA, darkcolor=COLOR_TARJETA, arrowcolor=COLOR_CAFE, background=COLOR_TARJETA)
    estilo.map("TCombobox", fieldbackground=[("readonly", COLOR_TARJETA)], foreground=[("readonly", COLOR_TEXTO)], selectbackground=[("readonly", COLOR_TARJETA)], selectforeground=[("readonly", COLOR_TEXTO)], background=[("readonly", COLOR_TARJETA), ("active", COLOR_TARJETA)], bordercolor=[("focus", COLOR_TARJETA)], lightcolor=[("focus", COLOR_TARJETA)], darkcolor=[("focus", COLOR_TARJETA)])
    ventana.option_add("*TCombobox*Listbox.background", COLOR_TARJETA)
    ventana.option_add("*TCombobox*Listbox.foreground", COLOR_TEXTO)
    ventana.option_add("*TCombobox*Listbox.selectBackground", COLOR_CAFE)
    ventana.option_add("*TCombobox*Listbox.selectForeground", "white")
    ventana.option_add("*TCombobox*Listbox.font", ("Segoe UI", 10))

"""
* Objetivo: Crea el lienzo de una pantalla con su imagen de fondo.
* Entradas: Contenedor y nombre de la imagen.
* Salidas: El lienzo, donde se dibuja el texto y se colocan los controles.
* Restricciones: Ninguna.
"""
def crear_lienzo(padre, imagen):
    lienzo = tk.Canvas(padre, width=ANCHO_VENTANA, height=ALTO_VENTANA, highlightthickness=0, bd=0)
    lienzo.place(x=0, y=0)
    lienzo.create_image(0, 0, image=cargar_imagen(imagen), anchor="nw")
    return lienzo

"""
* Objetivo: Dibuja una placa con esquinas curvas para que un título se lea bien.
* Entradas: Lienzo, posición, tamaño y color.
* Salidas: Ninguna.
* Restricciones: Debe dibujarse antes que el texto que va encima.
"""
def placa(lienzo, x, y, ancho, alto, color=COLOR_CAFE):
    lienzo.create_image(x, y, image=forma_redondeada(ancho, alto, 16, color), anchor="nw")

"""
* Objetivo: Representa un botón con esquinas curvas dibujado sobre un lienzo.
* Entradas: Texto, función a ejecutar y colores.
* Salidas: Se dibuja al llamar a colocar.
* Restricciones: Solo se puede colocar sobre un lienzo.
"""
class Boton:
    def __init__(self, texto, comando, color, color_texto, color_hover):
        self.texto = texto
        self.comando = comando
        self.color = color
        self.color_texto = color_texto
        self.color_hover = color_hover

    def dibujar(self, lienzo, x, y, ancho, alto):
        radio = min(alto // 2, RADIO_BOTON)
        normal = forma_redondeada(ancho, alto, radio, self.color)
        encima = forma_redondeada(ancho, alto, radio, self.color_hover)
        fondo = lienzo.create_image(x, y, image=normal, anchor="nw")
        letras = lienzo.create_text(x + ancho // 2, y + alto // 2, text=self.texto, font=("Segoe UI", 10, "bold"), fill=self.color_texto)

        def entrar(evento):
            lienzo.itemconfigure(fondo, image=encima)
            lienzo.configure(cursor="hand2")

        def salir(evento):
            lienzo.itemconfigure(fondo, image=normal)
            lienzo.configure(cursor="")

        for parte in (fondo, letras):
            lienzo.tag_bind(parte, "<Enter>", entrar)
            lienzo.tag_bind(parte, "<Leave>", salir)
            # Espera un instante para no borrar la pantalla mientras se procesa el clic
            lienzo.tag_bind(parte, "<ButtonRelease-1>", lambda evento: ventana_principal.after(10, self.comando))

"""
* Objetivo: Coloca un botón, una lista o un campo con esquinas curvas.
* Entradas: Lienzo, control, posición (x, y), ancho y alto en píxeles.
* Salidas: Ninguna.
* Restricciones: Las listas y los campos deben haberse creado dentro del lienzo.
"""
def colocar(lienzo, control, x, y, ancho, alto):
    if isinstance(control, Boton):
        control.dibujar(lienzo, x, y, ancho, alto)
        return
    fondo = forma_redondeada(ancho, alto, RADIO_CAMPO, COLOR_TARJETA, COLOR_BORDE)
    lienzo.create_image(x, y, image=fondo, anchor="nw")
    lienzo.create_window(x + 8, y + 3, window=control, anchor="nw", width=ancho - 15, height=alto - 6)

"""
* Objetivo: Crea un botón oscuro, o con los colores indicados.
* Entradas: Contenedor, texto, función a ejecutar y colores.
* Salidas: El botón creado, sin colocar.
* Restricciones: Se dibuja al llamar a colocar.
"""
def crear_boton(padre, texto, comando, color=COLOR_CAFE, color_texto="white", color_hover=COLOR_CAFE_HOVER):
    return Boton(texto, comando, color, color_texto, color_hover)

"""
* Objetivo: Crea un botón claro color cartón.
* Entradas: Contenedor, texto y función a ejecutar.
* Salidas: El botón creado, sin colocar.
* Restricciones: Se dibuja al llamar a colocar.
"""
def crear_boton_kraft(padre, texto, comando):
    return crear_boton(padre, texto, comando, COLOR_KRAFT, COLOR_TEXTO, COLOR_KRAFT_HOVER)

"""
* Objetivo: Crea una lista de selección de solo lectura.
* Entradas: Contenedor y valores de la lista.
* Salidas: La lista creada, sin colocar.
* Restricciones: Es de solo lectura para evitar nombres inválidos en Prolog.
"""
def crear_lista(padre, valores):
    return ttk.Combobox(padre, values=valores, state="readonly", font=("Segoe UI", 10))

"""
* Objetivo: Crea un campo de texto corto.
* Entradas: Contenedor.
* Salidas: El campo creado, sin colocar.
* Restricciones: Ninguna.
"""
def crear_entrada(padre):
    return tk.Entry(padre, bg=COLOR_TARJETA, fg=COLOR_TEXTO, relief="flat", bd=0, font=("Segoe UI", 10), justify="center", highlightthickness=0)

"""
* Objetivo: Dibuja una etiqueta pequeña sobre el lienzo.
* Entradas: Lienzo, posición (x, y) y texto.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def etiqueta(lienzo, x, y, texto):
    lienzo.create_text(x, y, text=texto, anchor="w", font=("Segoe UI", 10, "bold"), fill=COLOR_TEXTO)

"""
* Objetivo: Crea el área de resultados con esquinas curvas, scroll y estilos de texto.
* Entradas: Lienzo, posición, tamaño, color de fondo y grosor del borde.
* Salidas: El área de texto, de solo lectura.
* Restricciones: Para escribir en ella se usan escribir y limpiar.
"""
def crear_area_resultado(lienzo, x, y, ancho, alto, fondo=COLOR_HOJA, borde=1):
    color_borde = COLOR_BORDE if borde else None
    lienzo.create_image(x, y, image=forma_redondeada(ancho, alto, RADIO_AREA, fondo, color_borde), anchor="nw")

    marco = tk.Frame(lienzo, bg=fondo)
    nombre_estilo = f"{fondo[1:]}.Vertical.TScrollbar"
    ttk.Style().configure(nombre_estilo, background=COLOR_KRAFT, troughcolor=fondo, bordercolor=fondo, lightcolor=COLOR_KRAFT, darkcolor=COLOR_KRAFT, arrowcolor=COLOR_CAFE)
    barra = ttk.Scrollbar(marco, orient="vertical", style=nombre_estilo)
    barra.pack(side="right", fill="y")

    area = tk.Text(marco, bg=fondo, fg=COLOR_TEXTO, font=("Segoe UI", 11), wrap="word", relief="flat", bd=0, padx=12, pady=8, spacing1=3, spacing3=3, cursor="arrow", state="disabled", yscrollcommand=barra.set)
    area.pack(side="left", fill="both", expand=True)
    barra.configure(command=area.yview)

    area.tag_configure("titulo", font=("Segoe UI", 13, "bold"), foreground=COLOR_CAFE, spacing1=10, spacing3=4)
    area.tag_configure("alerta", font=("Segoe UI", 11, "bold"), foreground="#A3201C", background="#F7DEDA")
    area.tag_configure("neutro", font=("Segoe UI", 11, "bold"), foreground=COLOR_CAFE, background=COLOR_KRAFT_HOVER)
    area.tag_configure("item", lmargin1=12, lmargin2=26)

    lienzo.create_window(x + 10, y + 10, window=marco, anchor="nw", width=ancho - 20, height=alto - 20)
    return area

"""
* Objetivo: Agrega texto al área de resultados.
* Entradas: Área, texto y, opcionalmente, el nombre del estilo.
* Salidas: Ninguna.
* Restricciones: El estilo debe estar definido en crear_area_resultado.
"""
def escribir(area, texto, estilo=None):
    area.configure(state="normal")
    if estilo:
        area.insert(tk.END, texto, estilo)
    else:
        area.insert(tk.END, texto)
    area.configure(state="disabled")

"""
* Objetivo: Borra el contenido del área de resultados.
* Entradas: Área.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def limpiar(area):
    area.configure(state="normal")
    area.delete("1.0", tk.END)
    area.configure(state="disabled")

"""
* Objetivo: Muestra una ventana de mensaje con el estilo del expediente.
* Entradas: Título, mensaje y color del recuadro.
* Salidas: Ninguna; espera a que la persona la cierre.
* Restricciones: Bloquea la ventana principal mientras está abierta.
"""
def mostrar_mensaje(titulo, mensaje, color):
    ancho, alto = 460, 270
    dialogo = tk.Toplevel(ventana_principal)
    dialogo.title("Academia de Detectives")
    dialogo.resizable(False, False)
    dialogo.transient(ventana_principal)

    x = ventana_principal.winfo_rootx() + (ANCHO_VENTANA - ancho) // 2
    y = ventana_principal.winfo_rooty() + (ALTO_VENTANA - alto) // 2
    dialogo.geometry(f"{ancho}x{alto}+{x}+{y}")

    lienzo = tk.Canvas(dialogo, width=ancho, height=alto, bg=COLOR_CAFE, highlightthickness=0, bd=0)
    lienzo.pack()
    lienzo.create_image(10, 10, image=forma_redondeada(ancho - 20, alto - 20, 20, COLOR_TARJETA, color, 3), anchor="nw")
    lienzo.create_text(ancho // 2, 50, text=titulo, font=("Impact", 22), fill=color)
    lienzo.create_text(ancho // 2, 130, text=mensaje, width=390, justify="center", font=("Segoe UI", 11), fill=COLOR_TEXTO)
    colocar(lienzo, crear_boton(lienzo, "Entendido", dialogo.destroy), ancho // 2 - 70, alto - 62, 140, 36)

    dialogo.bind("<Return>", lambda evento: dialogo.destroy())
    dialogo.bind("<Escape>", lambda evento: dialogo.destroy())
    dialogo.grab_set()
    dialogo.focus_set()
    ventana_principal.wait_window(dialogo)

"""
* Objetivo: Muestra una ventana de error.
* Entradas: Mensaje y, opcionalmente, el título.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def mostrar_error(mensaje, titulo="ERROR"):
    mostrar_mensaje(titulo, mensaje, COLOR_ROJO)

"""
* Objetivo: Muestra un aviso, por ejemplo cuando falta un dato.
* Entradas: Mensaje y, opcionalmente, el título.
* Salidas: Ninguna.
* Restricciones: Ninguna.
"""
def mostrar_aviso(mensaje, titulo="ATENCIÓN"):
    mostrar_mensaje(titulo, mensaje, COLOR_ACENTO)