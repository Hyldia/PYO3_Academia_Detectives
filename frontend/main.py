# Ventana principla del proyecto

import tkinter as tk
from ventanas.acceso import mostrar_accesos
from ventanas.evidencias import mostar_evidencias

# Colores
COLOR_FONDO = "#F7E9E5"
COLOR_PANEL = "#FFF8F2"
COLOR_PRIMARIO = "#6B4366"
COLOR_SECUNDARIO = "#C592AD"
COLOR_ACCION = "#E49DA1"
COLOR_TEXTO = "#000000"

ventana = tk.Tk()
ventana.title("Academia de Detectives")
# Abrir maximizada
ventana.state("zoomed")
# Tamaño mínimo permitido
ventana.minsize(1200, 700)
ventana.configure(bg=COLOR_FONDO)

# Encabezado
titulo = tk.Label(ventana, text="Academia de detectives", font=("Arial", 22, "bold"), bg=COLOR_FONDO, fg=COLOR_PRIMARIO)
titulo.pack(pady=15)

# Contenedor principal
contenedor = tk.Frame(ventana, bg=COLOR_FONDO)
contenedor.pack(fill="both", expand=True, padx=20, pady=20)

# Menu lateral
marco_menu = tk.Frame(contenedor, bg=COLOR_PANEL, bd=2, relief="groove", width=200)
marco_menu.pack(side="left", fill="y", padx=(0, 15))

# Area dinamica
contenido = tk.Frame(contenedor, bg=COLOR_PANEL, bd= 2, relief= "groove")
contenido.pack(side="right", fill="both", expand=True)

# Titulo del menu lateral
titulo_menu = tk.Label(marco_menu, text="MENÚ", font=("Arial", 14, "bold"), bg=COLOR_PANEL, fg=COLOR_PRIMARIO)
titulo_menu.pack(pady=20)

# Botones
boton_acceso = tk.Button(marco_menu, text = "Consultar Accesos", width=18, bg=COLOR_PRIMARIO, fg="white", font=("Segoe UI", 11, "bold"), command=lambda: mostrar_accesos(contenido))
boton_acceso.pack(fill="x", pady=15, padx=5)

boton_evidencias = tk.Button(marco_menu, text="Consultar Evidencias", width=18, bg=COLOR_PRIMARIO, fg="white", font=("Segoe UI", 11, "bold"), command=lambda: mostar_evidencias(contenido))
boton_evidencias.pack(fill="x", pady=15, padx=5)

# Espaciador
tk.Label(marco_menu, bg=COLOR_PANEL).pack( expand=True, fill="both")

boton_salir = tk.Button(marco_menu, text="Salir", width=18, bg=COLOR_SECUNDARIO, fg="white", font=("Segoe UI", 11, "bold"), command=contenido.winfo_toplevel().destroy)
boton_salir.pack(fill="x", pady=15, padx=15)

ventana.mainloop()