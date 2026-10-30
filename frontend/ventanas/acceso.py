import tkinter as tk
from tkinter import ttk
from consultas import consultar_accesos
    
def consultar(combo_persona, resultado_texto): 
    resultado_texto.delete("1.0", tk.END) # Limpiar enl contenido anterior
    persona = combo_persona.get()
    if not persona:
        resultado_texto.insert(tk.END, "Seleccione una persona.")
        return
    accesos = consultar_accesos(persona)
    if accesos:
        resultado_texto.insert(tk.END,  f"{persona} tiene acceso a:\n\n")
        for lugar in accesos:
            resultado_texto.insert(tk.END, f"• {lugar}\n")
    else:
        resultado_texto.insert(tk.END, f"{persona} no tiene accesos a ningun lugar.")
        
def mostrar_accesos(contenido):
    # Limpia contenido anterior
    for widget in contenido.winfo_children():
        widget.destroy()
    
    titulo = tk.Label(contenido, text="Consulta de Accesos", font=("Arial", 16, "bold"), bg="#FFF8F2", fg="#493747")
    titulo.pack(pady=10)
    
    combo_persona = ttk.Combobox(contenido, width=15, height=25, values=["karina", "carlos", "nicole", "diego", "andrey"])
    combo_persona.pack(pady=5)
    
    resultado_texto = tk.Text(contenido, width=50, height=12, bg="#FFF8F2", fg="#3F3540", font=("Consolas", 12))
    resultado_texto.pack(pady=15)
    
    # Marco para botones
    marco_botones = tk.Frame(contenido)
    marco_botones.pack(pady=10)

    boton_consultar = tk.Button(marco_botones, text="Consultar", width=15, bg="#6B4366", fg="white", font=("Segoe UI", 10, "bold"), command= lambda: consultar(combo_persona, resultado_texto)) 
    boton_consultar.grid(row=0, column=0, padx=5)
    
    boton_limpiar = tk.Button(marco_botones, text="Limpiar", width=15, bg="#C592AD", fg="white", font=("Segoe UI", 10, "bold"), command=lambda: resultado_texto.delete("1.0", tk.END))
    boton_limpiar.grid(row=0, column=1, padx=5)