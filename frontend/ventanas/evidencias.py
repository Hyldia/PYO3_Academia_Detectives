import tkinter as tk
from tkinter import ttk
from consultas import consultar_evidencias, consultar_movimientos

"""
* Objetivo: Consulta las evidencias asociadas a una persona
"""
def consultar(combo_persona, resultado_texto):
    resultado_texto.delete("1.0", tk.END) # Limpiar el contenido anterior
    persona = combo_persona.get()
    if not persona:
        resultado_texto.insert(tk.END, "Seleccione una persona.")
        return
    evidencias = consultar_evidencias(persona)
    if evidencias:
        resultado_texto.insert(tk.END,  f"Evidencias asociadas a {persona}:\n\n")
        for evidencia in evidencias:
            resultado_texto.insert(tk.END, f"• {evidencia}\n")
    else:
        resultado_texto.insert(tk.END, f"No se encontraron evidencias asociadas a {persona}.")

"""
* Objetivo: Consulta los movimientos de una persona en un lugar durante un periodo de tiempo.
"""
def consultar_historial(combo_persona, combo_lugar, entrada_inicio, entrada_fin, resultado_texto):
    persona = combo_persona.get()
    lugar = combo_lugar.get()
    inicio = entrada_inicio.get()
    fin = entrada_fin.get()
    if not persona or not lugar or not inicio or not fin:
        resultado_texto.delete("1.0", tk.END)
        resultado_texto.insert(tk.END, "Por favor, complete todos los campos.")
        return
    resultado = consultar_movimientos(persona, lugar, inicio, fin)
    resultado_texto.insert(tk.END, f"\n\n{resultado}")

"""
* Objetivo: Muestra la ventana de consulta de evidencias.
"""     
def mostar_evidencias(contenido):
    for widget in contenido.winfo_children(): # Limpia el contenido anterior
        widget.destroy()
        
    titulo = tk.Label(contenido, text="Consulta de Evidencias", font=("Arial", 16, "bold"), bg="#FFF8F2", fg="#493747")
    titulo.pack(pady=10)
    
    # contenedor principal
    marco_principal = tk.Frame(contenido, bg="#FFF8F2")
    marco_principal.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Columna Izquierda
    marco_izquierdo = tk.Frame(marco_principal, bg="#FFF8F2")
    marco_izquierdo.pack(side="left", fill="both", expand=True, padx=20)
    
    combo_persona = ttk.Combobox(marco_izquierdo, width=20, values=["karina", "carlos", "nicole", "diego", "andrey"])
    combo_persona.pack(pady=10)
    
    # Marco para botones
    marco_botones = tk.Frame(marco_izquierdo, bg="#FFF8F2")
    marco_botones.pack(pady=10)
        
    boton_consultar = tk.Button(marco_botones, text="Consultar", width=15, bg="#A35F6B", fg="white", font=("Segoe UI", 10, "bold"), command= lambda: consultar(combo_persona, resultado_texto))
    boton_consultar.grid(row=0, column=0, padx=5)
        
    boton_limpiar = tk.Button(marco_botones, text="Limpiar", width=15, bg="#A35F6B", fg="white", font=("Segoe UI", 10, "bold"), command=lambda: resultado_texto.delete("1.0", tk.END))
    boton_limpiar.grid(row=0, column=1, padx=5)
    
    resultado_texto = tk.Text( marco_izquierdo, width=50, height=8, bg="#FFF8F2", fg="#3F3540", font=("Consolas", 12))
    resultado_texto.pack(pady=10, fill="both", expand=True)
    
    #Columna derecha
    marco_derecho = tk.Frame(marco_principal, bg="#FFF8F2")
    marco_derecho.pack(side="right", fill="y", padx=20)
    
    # Contenido para la consulta de movimientos    
    titulo_movimientos = tk.Label(marco_derecho, text="Consulta de Movimientos", font=("Arial", 16, "bold"), bg="#FFF8F2", fg="#493747")
    titulo_movimientos.pack(pady=10)
    
    combo_lugar = ttk.Combobox(marco_derecho, width=15, values=["laboratorio", "biblioteca", "oficina", "sala_evidencias", "entrada"])
    combo_lugar.pack(pady=10)
    
    label_inicio = tk.Label(marco_derecho, text=" Hora de Inicio (HHMM)", bg="#FFF8F2", fg="#493747")
    label_inicio.pack()
    entrada_inicio = tk.Entry(marco_derecho, width=10)
    entrada_inicio.pack(pady=5)
    
    label_fin = tk.Label(marco_derecho, text=" Hora de fin (HHMM)", bg="#FFF8F2", fg="#493747")
    label_fin.pack()
    entrada_fin = tk.Entry(marco_derecho, width=10)
    entrada_fin.pack(pady=5)
    
    boton_movimientos = tk.Button(marco_derecho, text="Consultar Movimientos", width=20, bg="#A35F6B", fg="white", font=("Segoe UI", 10, "bold"), command=lambda: consultar_historial(combo_persona, combo_lugar, entrada_inicio, entrada_fin, resultado_texto))
    boton_movimientos.pack(pady=15)
    