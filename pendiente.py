import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para inicializar la gráfica vacía
def inicializar_grafica():
    # Limpiar la figura anterior si existe
    for widget in frame_grafica.winfo_children():
        widget.destroy()

    # Crear la figura en la misma ventana
    global fig, ax
    fig, ax = plt.subplots(figsize=(8, 6))

    # Configurar la gráfica vacía con valores base de -999 a 999
    ax.set_title("Gráfica del Método DDA")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.set_xlim(-999, 999)  # Límites para el eje X de -999 a 999
    ax.set_ylim(-999, 999)  # Límites para el eje Y de -999 a 999

    # Establecer la relación de aspecto igual para que X y Y sean proporcionales
    ax.set_aspect('equal', 'box')

    # Integrar la gráfica en la interfaz Tkinter
    global canvas
    canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')

    # Conectar el evento de movimiento del mouse con la función de mostrar coordenadas
    canvas.mpl_connect('motion_notify_event', on_move)

# Función que se ejecuta cuando el mouse se mueve sobre la gráfica
def on_move(event):
    if event.inaxes != ax:  # Si el mouse no está dentro de los ejes de la gráfica
        return

    # Obtener las coordenadas del mouse en el gráfico
    x, y = event.xdata, event.ydata
    
    if x is not None and y is not None:  # Si las coordenadas son válidas
        # Actualizar la etiqueta con las coordenadas del punto
        label_coordenadas.config(text=f"Coordenadas: X = {x:.2f}, Y = {y:.2f}")

# Función para calcular la pendiente y graficar usando el método DDA
def calcular_y_graficar():
    try:
        xa = float(entry_xa.get())
        ya = float(entry_ya.get())
        xb = float(entry_xb.get())
        yb = float(entry_yb.get())

        dx = xb - xa
        dy = yb - ya

        # Calcular la pendiente
        pendiente = 'Infinita (línea vertical)' if dx == 0 else f"{(dy / dx):.2f}"
        label_resultado.config(text=f"Pendiente (m): {pendiente}")

        pasos = int(max(abs(dx), abs(dy)))
        x_incremento = dx / pasos
        y_incremento = dy / pasos

        x = xa
        y = ya

        # Listas para la tabla DDA
        pasos_lista, x_lista, y_lista = [], [], []

        for i in range(pasos + 1):
            pasos_lista.append(i)
            x_lista.append(round(x, 2))
            y_lista.append(round(y, 2))
            x += x_incremento
            y += y_incremento

        # Dibujar la línea DDA en la gráfica existente
        ax.plot(x_lista, y_lista, marker='o', color='blue', label='Línea DDA')
        ax.legend()

        # Hacer zoom en la parte de la recta
        min_x, max_x = min(x_lista), max(x_lista)
        min_y, max_y = min(y_lista), max(y_lista)
        margen = 100  # Margen adicional para el zoom
        ax.set_xlim(min_x - margen, max_x + margen)
        ax.set_ylim(min_y - margen, max_y + margen)

        # Redibujar la gráfica
        canvas.draw()

        # Mostrar la tabla DDA en la interfaz Tkinter
        for widget in frame_tabla.winfo_children():
            widget.destroy()

        columnas = ['Paso', 'X', 'Y']
        tabla_texto = tk.Text(frame_tabla, height=10, width=30, font=("Arial", 10))
        tabla_texto.insert(tk.END, f"{'Paso':<6}{'X':<10}{'Y':<10}\n")
        tabla_texto.insert(tk.END, f"{'-'*26}\n")
        for paso, x_val, y_val in zip(pasos_lista, x_lista, y_lista):
            tabla_texto.insert(tk.END, f"{paso:<6}{x_val:<10}{y_val:<10}\n")
        tabla_texto.config(state='disabled')
        tabla_texto.pack()

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")

# Función para limpiar la gráfica
def limpiar_grafica():
    # Limpiar la gráfica actual
    ax.cla()  # Limpiar los ejes de la gráfica
    ax.set_title("Gráfica del Método DDA")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.set_xlim(-999, 999)  # Límites para el eje X de -999 a 999
    ax.set_ylim(-999, 999)  # Límites para el eje Y de -999 a 999
    ax.set_aspect('equal', 'box')

    # Redibujar la gráfica vacía
    canvas.draw()

# Función para hacer zoom manual
def zoom_manual():
    try:
        # Obtener los valores de los campos de entrada para el zoom manual
        lim_x_min = float(entry_lim_x_min.get())
        lim_x_max = float(entry_lim_x_max.get())
        lim_y_min = float(entry_lim_y_min.get())
        lim_y_max = float(entry_lim_y_max.get())

        # Actualizar los límites de la gráfica
        ax.set_xlim(lim_x_min, lim_x_max)
        ax.set_ylim(lim_y_min, lim_y_max)

        # Redibujar la gráfica con el zoom aplicado
        canvas.draw()

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos para el zoom.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Método DDA - Cálculo de Pendiente y Gráfica")
root.state('zoomed')  # Pantalla completa

# Crear marcos para la disposición
frame_izquierda = tk.Frame(root, padx=10, pady=10)
frame_izquierda.pack(side='left', fill='y')

frame_tabla = tk.Frame(frame_izquierda, pady=10)
frame_tabla.pack(side='bottom', fill='x')

frame_grafica = tk.Frame(root, padx=10, pady=10, bg='white')
frame_grafica.pack(side='right', expand=True, fill='both')

# Inicializar la gráfica vacía
inicializar_grafica()

# Entradas de datos
tk.Label(frame_izquierda, text="Ingrese los valores:", font=("Arial", 12, "bold")).pack(pady=5)

entry_xa = tk.Entry(frame_izquierda, width=10)
tk.Label(frame_izquierda, text="Xa:").pack()
entry_xa.pack()

entry_ya = tk.Entry(frame_izquierda, width=10)
tk.Label(frame_izquierda, text="Ya:").pack()
entry_ya.pack()

entry_xb = tk.Entry(frame_izquierda, width=10)
tk.Label(frame_izquierda, text="Xb:").pack()
entry_xb.pack()

entry_yb = tk.Entry(frame_izquierda, width=10)
tk.Label(frame_izquierda, text="Yb:").pack()
entry_yb.pack()

# Botón de cálculo
tk.Button(frame_izquierda, text="Calcular y Graficar", command=calcular_y_graficar, bg="green", fg="white").pack(pady=10)

# Resultado de la pendiente
label_resultado = tk.Label(frame_izquierda, text="Pendiente (m): ", font=("Arial", 12))
label_resultado.pack(pady=5)

# Etiqueta para mostrar las coordenadas del mouse
label_coordenadas = tk.Label(frame_izquierda, text="Coordenadas: ", font=("Arial", 10))
label_coordenadas.pack(pady=5)

# Campos de entrada para el zoom manual
tk.Label(frame_izquierda, text="Zoom Manual", font=("Arial", 12, "bold")).pack(pady=10)

tk.Label(frame_izquierda, text="Limite X Min:").pack()
entry_lim_x_min = tk.Entry(frame_izquierda, width=10)
entry_lim_x_min.pack()

tk.Label(frame_izquierda, text="Limite X Max:").pack()
entry_lim_x_max = tk.Entry(frame_izquierda, width=10)
entry_lim_x_max.pack()

tk.Label(frame_izquierda, text="Limite Y Min:").pack()
entry_lim_y_min = tk.Entry(frame_izquierda, width=10)
entry_lim_y_min.pack()

tk.Label(frame_izquierda, text="Limite Y Max:").pack()
entry_lim_y_max = tk.Entry(frame_izquierda, width=10)
entry_lim_y_max.pack()

# Botón de zoom manual
tk.Button(frame_izquierda, text="Aplicar Zoom", command=zoom_manual, bg="blue", fg="white").pack(pady=10)

# Botón de limpieza
tk.Button(frame_izquierda, text="Limpiar Gráfica", command=limpiar_grafica, bg="red", fg="white").pack(pady=10)

root.mainloop()
