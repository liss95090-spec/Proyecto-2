import tkinter as tk
from tkinter import messagebox

def verificar_caracter():
    # Obtener el carácter ingresado en el campo de texto
    entrada = entry_letra.get().strip()
    
    if len(entrada) != 1:
        messagebox.showerror("Error de Entrada", "Por favor, digite exactamente UN carácter.")
        return
    
    # 1. Obtener código ASCII del carácter ingresado
    valor_ascii = ord(entrada)
    
    # 2. Extraer los 4 bits menos significativos
    cuatro_bits_entrada = valor_ascii & 0x0F
    binario_entrada_str = bin(cuatro_bits_entrada)[2:].zfill(4)
    
    # 3. Simular la lógica del circuito incrementador (+5)
    # Como el circuito trabaja con 4 bits, la suma se restringe con módulo 16
    valor_incrementado = (cuatro_bits_entrada + 5) & 0x0F
    binario_salida_str = bin(valor_incrementado)[2:].zfill(4)
    
    # Actualizar las etiquetas de la interfaz gráfica de usuario
    lbl_ascii_res.config(text=f"{valor_ascii}")
    lbl_bin_entrada.config(text=f"{binario_entrada_str} (Valor: {cuatro_bits_entrada})")
    lbl_bin_salida.config(text=f"{binario_salida_str} (Valor: {valor_incrementado})")
    
    # Mostrar desglose detallado en el registro de la consola interna
    txt_bitacora.insert(tk.END, f"Carácter: '{entrada}' | ASCII: {valor_ascii} | "
                                f"Entrada Circuito: {binario_entrada_str} | "
                                f"Resultado Esperado (+5): {binario_salida_str}\n")
    txt_bitacora.see(tk.END)

# --- CONSTRUCCIÓN DEL ENTORNO GRÁFICO TKINTER ---
root = tk.Tk()
root.title("StrangerTEC - Módulo de Verificación de Entradas (Proyecto II)")
root.geometry("620x460")
root.configure(bg="#0f111a")

# Título Principal
lbl_titulo = tk.Label(root, text="HERRAMIENTA DE VERIFICACIÓN DE ENTRADAS", 
                      font=("Courier New", 14, "bold"), bg="#0f111a", fg="#00ffcc")
lbl_titulo.pack(pady=15)

# Zona de Entrada de Datos
frame_entrada = tk.Frame(root, bg="#1a1c24", bd=2, relief=tk.RIDGE)
frame_entrada.pack(pady=10, fill=tk.X, padx=20)

lbl_instruccion = tk.Label(frame_entrada, text="Digite un carácter para evaluar:", 
                           font=("Arial", 11), bg="#1a1c24", fg="#ffffff")
lbl_instruccion.pack(side=tk.LEFT, padx=10, pady=10)

entry_letra = tk.Entry(frame_entrada, font=("Arial", 12, "bold"), width=5, justify="center")
entry_letra.pack(side=tk.LEFT, padx=10, pady=10)
entry_letra.insert(0, "A")

btn_calcular = tk.Button(frame_entrada, text="Verificar Salidas", font=("Arial", 10, "bold"),
                         bg="#00ffcc", fg="#000000", command=verificar_caracter)
btn_calcular.pack(side=tk.RIGHT, padx=10, pady=10)

# Zona de Despliegue de Resultados Lógicos
frame_resultados = tk.Frame(root, bg="#0f111a")
frame_resultados.pack(pady=15, padx=20, fill=tk.X)

# Grid de información
tk.Label(frame_resultados, text="Código ASCII decimal:", font=("Arial", 11), bg="#0f111a", fg="#aaaaaa").grid(row=0, column=0, sticky="w", pady=5)
lbl_ascii_res = tk.Label(frame_resultados, text="--", font=("Courier New", 12, "bold"), bg="#0f111a", fg="#ffffff")
lbl_ascii_res.grid(row=0, column=1, sticky="w", padx=15)

tk.Label(frame_resultados, text="4 bits de entrada (Extraídos):", font=("Arial", 11), bg="#0f111a", fg="#aaaaaa").grid(row=1, column=0, sticky="w", pady=5)
lbl_bin_entrada = tk.Label(frame_resultados, text="----", font=("Courier New", 12, "bold"), bg="#0f111a", fg="#ffcc00")
lbl_bin_entrada.grid(row=1, column=1, sticky="w", padx=15)

tk.Label(frame_resultados, text="Salida teórica del circuito (+5):", font=("Arial", 11), bg="#0f111a", fg="#aaaaaa").grid(row=2, column=0, sticky="w", pady=5)
lbl_bin_salida = tk.Label(frame_resultados, text="----", font=("Courier New", 12, "bold"), bg="#0f111a", fg="#00ff00")
lbl_bin_salida.grid(row=2, column=1, sticky="w", padx=15)

# Registro / Historial de pruebas realizadas en la sesión
lbl_bitacora = tk.Label(root, text="Historial de evaluaciones analíticas:", font=("Arial", 10, "italic"), bg="#0f111a", fg="#888888")
lbl_bitacora.pack(anchor="w", padx=20, pady=2)

txt_bitacora = tk.Text(root, height=10, width=70, font=("Courier New", 9), bg="#141621", fg="#ffffff", state=tk.NORMAL)
txt_bitacora.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

# Ejecutar la ventana
root.mainloop()