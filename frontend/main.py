# Ventana principla del proyecto

import tkinter as tk
from ventanas.acceso import mostrar_accesos

# Colores
COLOR_FONDO = "#F7E9E5"
COLOR_PANEL = "#FFF8F2"
COLOR_PRIMARIO = "#6B4366"
COLOR_SECUNDARIO = "#C592AD"
COLOR_ACCION = "#E49DA1"
COLOR_TEXTO = "#000000"

ventana = tk.Tk()
ventana.title("Academia de Detectives")
ventana.geometry("900x600")
ventana.configure(bg=COLOR_FONDO)

# Encabezado
titulo = tk.Label(ventana, text="Academia de detectives", font=("Arial", 22, "bold"), bg=COLOR_FONDO, fg=COLOR_PRIMARIO)
titulo.pack(pady=15)

# Menu
marco_menu = tk.Frame(ventana, bg=COLOR_FONDO)
marco_menu.pack(pady=10)

# Area dinamica
contenido = tk.Frame(ventana, bg=COLOR_PANEL, bd= 2, relief= "groove", width= 800, height= 420)
contenido.pack(pady= 20)
contenido.pack_propagate(False)

# Botones
boton_acceso = tk.Button(marco_menu, text = "Consultar Accesos", width=20, bg=COLOR_PRIMARIO, fg="white", font=("Segoe UI", 12, "bold"), command=lambda: mostrar_accesos(contenido))
boton_acceso.grid(row= 0, column= 0, padx= 5)

boton_salir = tk.Button(marco_menu, text="Salir", width=20, bg=COLOR_SECUNDARIO, fg="white", font=("Segoe UI", 12, "bold"), command=contenido.winfo_toplevel().destroy)
boton_salir.grid(row=0, column=8, padx=5)

ventana.mainloop()