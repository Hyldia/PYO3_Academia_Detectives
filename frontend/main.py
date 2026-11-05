# Ventana principal del proyecto

import tkinter as tk
import traceback
from tkinter import messagebox

# Si Prolog o pyswip fallan al cargar, se avisa en vez de cerrarse sin explicación
try:
    from ventanas.acceso import mostrar_accesos
    from ventanas.estilos import ALTO_VENTANA, ANCHO_VENTANA, aplicar_estilos, mostrar_error
    from ventanas.evidencias import mostrar_evidencias
    from ventanas.navegacion import iniciar, ir_a
    from ventanas.portada import mostrar_portada
    from ventanas.resolver import mostrar_resolver
    from ventanas.sospechosos import mostrar_sospechosos
except Exception as error:
    raiz = tk.Tk()
    raiz.withdraw()
    messagebox.showerror("Academia de Detectives", f"No se pudo iniciar el programa.\n\n{error}")
    raise SystemExit(1)

"""
* Objetivo: Muestra una ventana cuando algo falla durante el uso del programa.
* Entradas: Tipo, valor y traza del error, que entrega tkinter.
* Salidas: Ninguna.
* Restricciones: También imprime el detalle en la consola para poder revisarlo.
"""
def manejar_error(tipo, valor, traza):
    traceback.print_exception(tipo, valor, traza)
    mostrar_error(f"No se pudo completar la operación.\n\n{str(valor)[:220]}")

ventana = tk.Tk()
ventana.title("Academia de Detectives")

# Ventana de tamaño fijo y centrada en la pantalla
ventana.resizable(False, False)
x = (ventana.winfo_screenwidth() - ANCHO_VENTANA) // 2
y = max((ventana.winfo_screenheight() - ALTO_VENTANA) // 2 - 30, 0)
ventana.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}+{x}+{y}")

aplicar_estilos(ventana)
ventana.report_callback_exception = manejar_error

iniciar(ventana, {
    "portada": mostrar_portada,
    "accesos": mostrar_accesos,
    "evidencias": mostrar_evidencias,
    "sospechosos": mostrar_sospechosos,
    "resolver": mostrar_resolver,
})

ventana.after(0, lambda: ir_a("portada"))
ventana.mainloop()