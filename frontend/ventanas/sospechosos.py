import tkinter as tk
from tkinter import ttk
from consultas import (consultar_personas, consultar_evento, consultar_sospechosos, consultar_contradicciones,
                       consultar_todas_contradicciones, consultar_coartada, consultar_inferencia)

"""
* Objetivo: Convierte un valor booleano en el texto Sí o No
"""
def si_no(valor):
    return "Sí" if valor else "No"

"""
* Objetivo: Escribe el encabezado con los datos del evento del caso.
"""
def escribir_evento(resultado_texto):
    evento = consultar_evento()
    if evento:
        nombre, lugar, hora, inicio, fin = evento
        resultado_texto.insert(tk.END, f"Evento: {nombre} en {lugar} a las {hora} (se analiza de {inicio} a {fin})\n\n")

"""
* Objetivo: Muestra el análisis de inferencia de la persona seleccionada
"""
def analizar(combo_persona, resultado_texto):
    resultado_texto.delete("1.0", tk.END) # Limpiar el contenido anterior
    persona = combo_persona.get()
    if not persona:
        resultado_texto.insert(tk.END, "Seleccione una persona.")
        return
    escribir_evento(resultado_texto)
    inferencia = consultar_inferencia(persona)
    if inferencia["sospechoso"]:
        resultado_texto.insert(tk.END, f"Resultado: {persona} cumple las condiciones de posible sospechoso.\n\n")
    else:
        resultado_texto.insert(tk.END, f"Resultado: {persona} no cumple las condiciones de posible sospechoso.\n\n")

    resultado_texto.insert(tk.END, "Oportunidad:\n")
    resultado_texto.insert(tk.END, f"• Estuvo en la escena durante el evento: {si_no(inferencia['en_escena'])}\n")
    resultado_texto.insert(tk.END, f"• Tiene acceso al lugar del evento: {si_no(inferencia['acceso'])}\n\n")

    resultado_texto.insert(tk.END, "Indicios:\n")
    evidencias = ", ".join(inferencia["evidencias"]) if inferencia["evidencias"] else "ninguna"
    resultado_texto.insert(tk.END, f"• Evidencias en la escena: {evidencias}\n")
    resultado_texto.insert(tk.END, f"• Contradicción durante el evento: {si_no(inferencia['contradiccion_evento'])}\n\n")

    coartada = consultar_coartada(persona)
    if coartada:
        lugar, hora = coartada
        resultado_texto.insert(tk.END, f"Coartada: declaró estar en {lugar} a las {hora} y el registro de movimientos lo respalda.\n\n")
    else:
        resultado_texto.insert(tk.END, "Coartada: no tiene una coartada válida.\n\n")

    contradicciones = consultar_contradicciones(persona)
    if contradicciones:
        resultado_texto.insert(tk.END, "Contradicciones:\n")
        for lugar_dicho, hora_dicha, lugar_registro, hora_registro in contradicciones:
            resultado_texto.insert(tk.END, f"• Dijo estar en {lugar_dicho} a las {hora_dicha}, pero según el registro estuvo en {lugar_registro} a las {hora_registro}.\n")
    else:
        resultado_texto.insert(tk.END, "Contradicciones: ninguna.\n")

"""
* Objetivo: Muestra la lista de posibles sospechosos inferida por Prolog
"""
def ver_sospechosos(resultado_texto):
    resultado_texto.delete("1.0", tk.END)
    escribir_evento(resultado_texto)
    sospechosos = consultar_sospechosos()
    if sospechosos:
        resultado_texto.insert(tk.END, "Posibles sospechosos:\n\n")
        for persona in sospechosos:
            resultado_texto.insert(tk.END, f"• {persona}\n")
    else:
        resultado_texto.insert(tk.END, "No se encontraron posibles sospechosos.")

"""
* Objetivo: Muestra todas las contradicciones encontradas en el caso.
"""
def ver_contradicciones(resultado_texto):
    resultado_texto.delete("1.0", tk.END)
    contradicciones = consultar_todas_contradicciones()
    if contradicciones:
        resultado_texto.insert(tk.END, "Contradicciones encontradas en el caso:\n\n")
        for persona, lugar_dicho, hora_dicha, lugar_registro, hora_registro in contradicciones:
            resultado_texto.insert(tk.END, f"• {persona}: dijo estar en {lugar_dicho} a las {hora_dicha}, pero según el registro estuvo en {lugar_registro} a las {hora_registro}.\n")
    else:
        resultado_texto.insert(tk.END, "No se encontraron contradicciones.")

"""
* Objetivo: Muestra la ventana de análisis de sospechosos.
"""
def mostrar_sospechosos(contenido):
    for widget in contenido.winfo_children(): # Limpia el contenido anterior
        widget.destroy()

    titulo = tk.Label(contenido, text="Análisis de Sospechosos", font=("Arial", 16, "bold"), bg="#FFF8F2", fg="#493747")
    titulo.pack(pady=10)

    # Marco para la persona y los botones
    marco_controles = tk.Frame(contenido, bg="#FFF8F2")
    marco_controles.pack(pady=10)

    # Las personas se leen de Prolog para que funcione con cualquier hechos.pl
    combo_persona = ttk.Combobox(marco_controles, width=20, values=consultar_personas(), state="readonly")
    combo_persona.grid(row=0, column=0, padx=5)

    boton_analizar = tk.Button(marco_controles, text="Analizar persona", width=18, bg="#A35F6B", fg="white", font=("Segoe UI", 10, "bold"), command=lambda: analizar(combo_persona, resultado_texto))
    boton_analizar.grid(row=0, column=1, padx=5)

    boton_sospechosos = tk.Button(marco_controles, text="Ver posibles sospechosos", width=22, bg="#A35F6B", fg="white", font=("Segoe UI", 10, "bold"), command=lambda: ver_sospechosos(resultado_texto))
    boton_sospechosos.grid(row=0, column=2, padx=5)

    boton_contradicciones = tk.Button(marco_controles, text="Ver contradicciones", width=18, bg="#A35F6B", fg="white", font=("Segoe UI", 10, "bold"), command=lambda: ver_contradicciones(resultado_texto))
    boton_contradicciones.grid(row=0, column=3, padx=5)

    boton_limpiar = tk.Button(marco_controles, text="Limpiar", width=12, bg="#A35F6B", fg="white", font=("Segoe UI", 10, "bold"), command=lambda: resultado_texto.delete("1.0", tk.END))
    boton_limpiar.grid(row=0, column=4, padx=5)

    resultado_texto = tk.Text(contenido, width=90, height=20, bg="#FFF8F2", fg="#3F3540", font=("Consolas", 12), wrap="word")
    resultado_texto.pack(pady=10, padx=20, fill="both", expand=True)