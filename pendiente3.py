import tkinter as tk
from tkinter import messagebox
from tkinter import colorchooser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

colores_octantes = ['red', 'green', 'blue', 'orange', 'purple', 'brown', 'pink', 'gray']  # Lista global de colores
# Variable global para el color de relleno del triángulo
color_relleno_triangulo = 'red'
color_elipse = 'blue'  # Color inicial para la elipse
colores_segmentos_elipse = ['red', 'green', 'blue', 'yellow']  # Colores para los 4 segmentos de la elipse

# Función para inicializar la gráfica vacía
def inicializar_grafica():
    for widget in frame_grafica.winfo_children():
        widget.destroy()

    global fig, ax
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Gráfica del Método DDA")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.set_xlim(-999, 999)
    ax.set_ylim(-999, 999)
    ax.set_aspect('equal', 'box')

    global canvas
    canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')

    # Conectar el evento de movimiento del mouse con la función de mostrar coordenadas
    canvas.mpl_connect('motion_notify_event', on_move)
    # Conectar el evento de la rueda del mouse para hacer zoom
    canvas.mpl_connect('scroll_event', on_scroll)

# Función para manejar el zoom con la rueda del mouse
def on_scroll(event):
    if event.inaxes != ax:  # Si el mouse no está dentro de los ejes de la gráfica
        return

    # Obtener los límites actuales de los ejes
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # Calcular el factor de zoom
    zoom_factor = 1.1 if event.button == 'up' else 0.9

    # Aplicar el zoom
    ax.set_xlim([x * zoom_factor for x in xlim])
    ax.set_ylim([y * zoom_factor for y in ylim])

    # Redibujar la gráfica
    canvas.draw()

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
        mostrar_tabla_dda(pasos_lista, x_lista, y_lista)

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")
                
# Función para mostrar la tabla DDA
def mostrar_tabla_dda(pasos_lista, x_lista, y_lista):
    # Limpiar el frame de la tabla
    for widget in frame_tabla.winfo_children():
        widget.destroy()

    # Crear un widget Text para mostrar la tabla
    tabla_texto = tk.Text(frame_tabla, height=20, width=20, font=("Arial", 12))
    tabla_texto.insert(tk.END, f"{'Paso':<6}{'X':<10}{'Y':<10}\n")
    tabla_texto.insert(tk.END, f"{'-'*26}\n")
    for paso, x_val, y_val in zip(pasos_lista, x_lista, y_lista):
        tabla_texto.insert(tk.END, f"{paso:<6}{x_val:<10}{y_val:<10}\n")
    tabla_texto.config(state='disabled')
    tabla_texto.pack()

# Función para calcular y graficar un círculo usando el método del punto medio
def calcular_y_graficar_circulo():
    try:
        # Obtener los valores de entrada
        xc = int(entry_xc.get())
        yc = int(entry_yc.get())
        r = int(entry_radio.get())

        # Limpiar la gráfica actual
        ax.cla()
        ax.set_title("Círculo - Método del Punto Medio")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True)
        ax.set_aspect('equal', 'box')

        # Inicializar listas para almacenar los puntos de cada octante
        octantes = [[] for _ in range(8)]
        colores = colores_octantes  # Usar la lista global de colores

        # Algoritmo del Punto Medio para la Circunferencia
        x = 0
        y = r
        P = 1 - r  # Parámetro de decisión inicial

        while x <= y:
            # Almacenar los puntos en cada octante
            octantes[0].append((xc + x, yc + y))
            octantes[1].append((xc + y, yc + x))
            octantes[2].append((xc + y, yc - x))
            octantes[3].append((xc + x, yc - y))
            octantes[4].append((xc - x, yc - y))
            octantes[5].append((xc - y, yc - x))
            octantes[6].append((xc - y, yc + x))
            octantes[7].append((xc - x, yc + y))

            # Actualizar el parámetro de decisión
            if P < 0:
                P += 2 * x + 3
            else:
                P += 2 * (x - y) + 5
                y -= 1
            x += 1

        # Dibujar los puntos en la gráfica y rellenar cada octante
        for i, octante in enumerate(octantes):
            x_vals = [p[0] for p in octante]
            y_vals = [p[1] for p in octante]
            ax.plot(x_vals, y_vals, marker='o', markersize=3, linestyle='None', color=colores[i])
            ax.fill([xc] + x_vals, [yc] + y_vals, color=colores[i], alpha=0.3)  # Rellenar el octante

        # Ajustar los límites de la gráfica
        ax.set_xlim(xc - r - 10, xc + r + 10)
        ax.set_ylim(yc - r - 10, yc + r + 10)

        # Redibujar la gráfica
        canvas.draw()

        # Mostrar las tablas de los octantes
        mostrar_tablas_octantes(octantes, P)

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")

# Función para mostrar las tablas de los octantes
def mostrar_tablas_octantes(octantes, P0):
    # Limpiar el frame de la tabla
    for widget in frame_tabla_circulo.winfo_children():
        widget.destroy()

    # Crear un frame para las tablas
    frame_tablas = tk.Frame(frame_tabla_circulo)
    frame_tablas.pack(fill='both', expand=True)

    # Función para crear una tabla
    def crear_tabla(frame, datos, titulo, P0, octante_idx):
        frame_octante = tk.Frame(frame) 
        # Botón para cambiar color
        btn_color = tk.Button(
            frame_octante, 
            text=f"Color Octante {octante_idx + 1}", 
            command=lambda idx=octante_idx: cambiar_color(idx),
            bg=colores_octantes[octante_idx]  # Color de fondo del botón
        )
        btn_color.pack(pady=5)
        
        tabla_texto = tk.Text(frame_octante, height=10, width=13, font=("Arial", 12))
        tabla_texto.insert(tk.END, f"{titulo}\n")
        tabla_texto.insert(tk.END, f"P0 = {P0}\n")  # Mostrar P0
        tabla_texto.insert(tk.END, f"{'X':<10}{'Y':<10}\n")
        tabla_texto.insert(tk.END, f"{'-'*20}\n")
        for i in range(0, len(datos), 4):  # Mostrar 4 puntos por fila
            for x, y in datos[i:i+4]:
                tabla_texto.insert(tk.END, f"{x:<10}{y:<10}\n")
            tabla_texto.insert(tk.END, f"{'-'*20}\n")
        tabla_texto.config(state='disabled')

        # Empacar el widget Text dentro del frame del octante
        tabla_texto.pack(side='top', padx=10, pady=10)
        return frame_octante  # Devuelves el frame completo con la tabla y el botón


    # Crear un frame para los primeros 4 octantes
    frame_arriba = tk.Frame(frame_tablas)
    frame_arriba.pack(side='top', fill='both', expand=True)

    # Crear un frame para los últimos 4 octantes
    frame_abajo = tk.Frame(frame_tablas)
    frame_abajo.pack(side='bottom', fill='both', expand=True)

    # Para los primeros 4 octantes
    for i in range(4):
        tabla = crear_tabla(frame_arriba, octantes[i], f"Octante {i + 1}", P0, i)  # Pasar el índice 'i'
        tabla.pack(side='left', padx=10, pady=10)

    # Para los últimos 4 octantes
    for i in range(4, 8):
        tabla = crear_tabla(frame_abajo, octantes[i], f"Octante {i + 1}", P0, i)  # Pasar el índice 'i'
        tabla.pack(side='left', padx=10, pady=10)

def cambiar_color(octante):
    color = colorchooser.askcolor(title=f"Selecciona un color para el Octante {octante + 1}")[1]
    if color:
        colores_octantes[octante] = color  # Actualizar el color
        calcular_y_graficar_circulo()  # Redibujar el círculo con el nuevo color

def crear_botones_colores(frame):
    for i in range(8):
        btn = tk.Button(frame, text=f"Color Octante {i+1}", command=lambda i=i: cambiar_color(i))
        btn.pack(side='left', padx=5, pady=5)

def mover_circulo():
    try:
        global nuevo_xc, nuevo_yc
        nuevo_xc = int(entry_nuevo_xc.get())
        nuevo_yc = int(entry_nuevo_yc.get())
        r = int(entry_radio.get())

        ax.cla()
        ax.set_title("Círculo Movido - Método del Punto Medio")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True)
        ax.set_aspect('equal', 'box')

        octantes = [[] for _ in range(8)]
        colores = colores_octantes  # Usar la lista global de colores

        x = 0
        y = r
        P = 1 - r

        while x <= y:
            octantes[0].append((nuevo_xc + x, nuevo_yc + y))
            octantes[1].append((nuevo_xc + y, nuevo_yc + x))
            octantes[2].append((nuevo_xc + y, nuevo_yc - x))
            octantes[3].append((nuevo_xc + x, nuevo_yc - y))
            octantes[4].append((nuevo_xc - x, nuevo_yc - y))
            octantes[5].append((nuevo_xc - y, nuevo_yc - x))
            octantes[6].append((nuevo_xc - y, nuevo_yc + x))
            octantes[7].append((nuevo_xc - x, nuevo_yc + y))

            if P < 0:
                P += 2 * x + 3
            else:
                P += 2 * (x - y) + 5
                y -= 1
            x += 1

        for i, octante in enumerate(octantes):
            x_vals = [p[0] for p in octante]
            y_vals = [p[1] for p in octante]
            ax.plot(x_vals, y_vals, marker='o', markersize=3, linestyle='None', color=colores[i])
            ax.fill([nuevo_xc] + x_vals, [nuevo_yc] + y_vals, color=colores[i], alpha=0.3)

        ax.set_xlim(nuevo_xc - r - 10, nuevo_xc + r + 10)
        ax.set_ylim(nuevo_yc - r - 10, nuevo_yc + r + 10)

        canvas.draw()

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")

# Función para calcular y graficar un triángulo relleno
def calcular_y_graficar_triangulo():
    try:
        # Obtener los puntos del triángulo
        x1 = float(entry_x1.get())
        y1 = float(entry_y1.get())
        x2 = float(entry_x2.get())
        y2 = float(entry_y2.get())
        x3 = float(entry_x3.get())
        y3 = float(entry_y3.get())

        # Limpiar la gráfica actual
        ax.cla()
        ax.set_title("Triángulo Relleno - Método DDA")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True)
        ax.set_aspect('equal', 'box')

        # Función para calcular una línea usando DDA
        def calcular_linea_dda(xa, ya, xb, yb):
            dx = xb - xa
            dy = yb - ya
            pasos = int(max(abs(dx), abs(dy)))
            x_incremento = dx / pasos
            y_incremento = dy / pasos
            x, y = xa, ya
            puntos = []
            for _ in range(pasos + 1):
                puntos.append((round(x, 2), round(y, 2)))
                x += x_incremento
                y += y_incremento
            return puntos

        # Calcular las tres líneas del triángulo
        linea1 = calcular_linea_dda(x1, y1, x2, y2)
        linea2 = calcular_linea_dda(x2, y2, x3, y3)
        linea3 = calcular_linea_dda(x3, y3, x1, y1)

        # Calcular las pendientes de las tres líneas
        def calcular_pendiente(xa, ya, xb, yb):
            dx = xb - xa
            dy = yb - ya
            return 'Infinita (línea vertical)' if dx == 0 else f"{(dy / dx):.2f}"

        pendiente1 = calcular_pendiente(x1, y1, x2, y2)
        pendiente2 = calcular_pendiente(x2, y2, x3, y3)
        pendiente3 = calcular_pendiente(x3, y3, x1, y1)

        # Mostrar las pendientes en la interfaz
        label_pendiente1.config(text=f"Pendiente Línea 1 (m): {pendiente1}")
        label_pendiente2.config(text=f"Pendiente Línea 2 (m): {pendiente2}")
        label_pendiente3.config(text=f"Pendiente Línea 3 (m): {pendiente3}")

        # Dibujar las líneas en la gráfica
        ax.plot([p[0] for p in linea1], [p[1] for p in linea1], marker='o', color='blue', label='Línea 1')
        ax.plot([p[0] for p in linea2], [p[1] for p in linea2], marker='o', color='green', label='Línea 2')
        ax.plot([p[0] for p in linea3], [p[1] for p in linea3], marker='o', color='red', label='Línea 3')
        ax.legend()

        # Rellenar el triángulo
        ax.fill([x1, x2, x3], [y1, y2, y3], color=color_relleno_triangulo, alpha=0.8)

        # Ajustar los límites de la gráfica
        min_x = min(x1, x2, x3)
        max_x = max(x1, x2, x3)
        min_y = min(y1, y2, y3)
        max_y = max(y1, y2, y3)
        margen = 50  # Margen adicional
        ax.set_xlim(min_x - margen, max_x + margen)
        ax.set_ylim(min_y - margen, max_y + margen)

        # Redibujar la gráfica
        canvas.draw()

        # Mostrar las tablas de las tres líneas
        mostrar_tablas_triangulo(linea1, linea2, linea3)

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")

# Función para mostrar las tablas de las tres líneas del triángulo
def mostrar_tablas_triangulo(linea1, linea2, linea3):
    # Limpiar el frame de la tabla
    for widget in frame_tabla_triangulo.winfo_children():
        widget.destroy()

    # Crear un frame para las tres tablas
    frame_tablas = tk.Frame(frame_tabla_triangulo)
    frame_tablas.pack(fill='both', expand=True)

    # Función para crear una tabla
    def crear_tabla(frame, datos, titulo):
        tabla_texto = tk.Text(frame, height=20, width=15, font=("Arial", 12))
        tabla_texto.insert(tk.END, f"{titulo}\n")
        tabla_texto.insert(tk.END, f"{'Paso':<6}{'X':<10}{'Y':<10}\n")
        tabla_texto.insert(tk.END, f"{'-'*26}\n")
        for i, (x, y) in enumerate(datos):
            tabla_texto.insert(tk.END, f"{i:<6}{x:<10}{y:<10}\n")
        tabla_texto.config(state='disabled')
        tabla_texto.pack(side='left', padx=10, pady=10)

    # Crear las tres tablas
    crear_tabla(frame_tablas, linea1, "Línea 1")
    crear_tabla(frame_tablas, linea2, "Línea 2")
    crear_tabla(frame_tablas, linea3, "Línea 3")

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

    # Limpiar las tablas de los octantes
    for widget in frame_tabla_circulo.winfo_children():
        widget.destroy()

# Función para cambiar el color de relleno del triángulo
def cambiar_color_triangulo():
    global color_relleno_triangulo
    color = colorchooser.askcolor(title="Seleccionar color de relleno")[1]
    if color:
        color_relleno_triangulo = color
        calcular_y_graficar_triangulo()
        

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
        
# Función para hacer zoom manual en el triángulo
def zoom_manual_triangulo():
    try:
        # Obtener los valores de los campos de entrada para el zoom manual
        lim_x_min = float(entry_lim_x_min_triangulo.get())
        lim_x_max = float(entry_lim_x_max_triangulo.get())
        lim_y_min = float(entry_lim_y_min_triangulo.get())
        lim_y_max = float(entry_lim_y_max_triangulo.get())

        # Actualizar los límites de la gráfica
        ax.set_xlim(lim_x_min, lim_x_max)
        ax.set_ylim(lim_y_min, lim_y_max)

        # Redibujar la gráfica con el zoom aplicado
        canvas.draw()

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos para el zoom.")

# Función para hacer zoom manual en la elipse
def zoom_manual_elipse():
    try:
        # Obtener los valores de los campos de entrada para el zoom manual
        lim_x_min = float(entry_lim_x_min_elipse.get())
        lim_x_max = float(entry_lim_x_max_elipse.get())
        lim_y_min = float(entry_lim_y_min_elipse.get())
        lim_y_max = float(entry_lim_y_max_elipse.get())

        # Actualizar los límites de la gráfica
        ax.set_xlim(lim_x_min, lim_x_max)
        ax.set_ylim(lim_y_min, lim_y_max)

        # Redibujar la gráfica con el zoom aplicado
        canvas.draw()

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos para el zoom.")

# Función para mostrar la pantalla de inicio
def mostrar_pantalla_inicio():
    # Ocultar otros frames
    frame_trazado.pack_forget()
    frame_opciones.pack_forget()
    frame_grafica.pack_forget()
    frame_linea_recta.pack_forget()
    frame_triangulo.pack_forget()
    frame_circulo.pack_forget()
    frame_elipse.pack_forget()  # Ocultar el frame de la elipse

    # Mostrar pantalla de inicio
    frame_inicio.pack(expand=True, fill='both')

# Función para mostrar el menú de trazado
def mostrar_menu_trazado():
    frame_inicio.pack_forget()
    frame_opciones.pack_forget()
    frame_grafica.pack_forget()
    frame_linea_recta.pack_forget()
    frame_triangulo.pack_forget()
    frame_circulo.pack_forget()
    frame_elipse.pack_forget()  # Ocultar el frame de la elipse
    frame_trazado.pack(expand=True, fill='both')

# Función para mostrar el menú de opciones
def mostrar_menu_opciones():
    frame_inicio.pack_forget()
    frame_trazado.pack_forget()
    frame_grafica.pack_forget()
    frame_linea_recta.pack_forget()
    frame_triangulo.pack_forget()
    frame_circulo.pack_forget()
    frame_elipse.pack_forget()  # Ocultar el frame de la elipse
    frame_opciones.pack(expand=True, fill='both')

# Función para mostrar la interfaz de línea recta
def mostrar_linea_recta():
    frame_inicio.pack_forget()
    frame_trazado.pack_forget()
    frame_opciones.pack_forget()
    frame_triangulo.pack_forget()
    frame_circulo.pack_forget()
    frame_elipse.pack_forget()  # Ocultar el frame de la elipse
    frame_grafica.pack(side='right', expand=True, fill='both')
    frame_linea_recta.pack(side='left', fill='both')

# Función para mostrar la interfaz de triángulo
def mostrar_triangulo():
    frame_inicio.pack_forget()
    frame_trazado.pack_forget()
    frame_opciones.pack_forget()
    frame_linea_recta.pack_forget()
    frame_circulo.pack_forget()
    frame_elipse.pack_forget()  # Ocultar el frame de la elipse
    frame_grafica.pack(side='right', expand=True, fill='both')
    frame_triangulo.pack(side='left', fill='both')

# Función para mostrar la interfaz de círculo
def mostrar_circulo():
    frame_inicio.pack_forget()
    frame_trazado.pack_forget()
    frame_opciones.pack_forget()
    frame_linea_recta.pack_forget()
    frame_triangulo.pack_forget()
    frame_elipse.pack_forget()  # Ocultar el frame de la elipse
    frame_grafica.pack(side='right', expand=True, fill='both')
    frame_circulo.pack(side='left', fill='both')

# Función para mostrar la interfaz de elipse
def mostrar_elipse():
    frame_inicio.pack_forget()
    frame_trazado.pack_forget()
    frame_opciones.pack_forget()
    frame_linea_recta.pack_forget()
    frame_triangulo.pack_forget()
    frame_circulo.pack_forget()
    frame_grafica.pack(side='right', expand=True, fill='both')
    frame_elipse.pack(side='left', fill='both')

# Función para calcular y graficar una elipse usando el método del punto medio
def calcular_y_graficar_elipse():
    try:
        xc = int(entry_xc_elipse.get())
        yc = int(entry_yc_elipse.get())
        rx = int(entry_rx_elipse.get())
        ry = int(entry_ry_elipse.get())
        
        # Limpiar la gráfica actual
        ax.cla()
        ax.set_title("Elipse - Método del Punto Medio")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True)
        ax.set_aspect('equal', 'box')
        
        # Inicializar listas para cada cuadrante
        cuadrante1 = []
        cuadrante2 = []
        cuadrante3 = []
        cuadrante4 = []
        
        # Valores auxiliares
        rx2 = rx * rx
        ry2 = ry * ry
        dos_ry2 = 2 * ry2
        dos_rx2 = 2 * rx2
        
        # Algoritmo del Punto Medio para Elipse
        x = 0
        y = ry
        
        # REGIÓN 1
        # Parámetro de decisión inicial
        P = round(ry2 - rx2*ry + 0.25*rx2, 2)
        
        while dos_ry2*x < dos_rx2*y:
            # Agregar puntos a cada cuadrante
            cuadrante1.append((x, y, P))
            cuadrante2.append((-x, y, P))
            cuadrante3.append((-x, -y, P))
            cuadrante4.append((x, -y, P))
            
            x += 1
            if P < 0:
                P += dos_ry2*x + ry2
            else:
                y -= 1
                P += dos_ry2*x - dos_rx2*y + ry2
            
            P = round(P, 2)
        
        # REGIÓN 2
        P = round(ry2*(x+0.5)**2 + rx2*(y-1)**2 - rx2*ry2, 2)
        
        while y >= 0:
            # Agregar puntos a cada cuadrante
            cuadrante1.append((x, y, P))
            cuadrante2.append((-x, y, P))
            cuadrante3.append((-x, -y, P))
            cuadrante4.append((x, -y, P))
            
            y -= 1
            if P > 0:
                P += -dos_rx2*y + rx2
            else:
                x += 1
                P += dos_ry2*x - dos_rx2*y + rx2
            
            P = round(P, 2)
        
        # Dibujar la elipse
        puntos_elipse = []
        for x, y, _ in cuadrante1:
            puntos_elipse.append((xc + x, yc + y))
        for x, y, _ in cuadrante2:
            puntos_elipse.append((xc + x, yc + y))
        for x, y, _ in cuadrante3:
            puntos_elipse.append((xc + x, yc + y))
        for x, y, _ in cuadrante4:
            puntos_elipse.append((xc + x, yc + y))
        
        x_coords = [p[0] for p in puntos_elipse]
        y_coords = [p[1] for p in puntos_elipse]
        ax.scatter(x_coords, y_coords, color=color_elipse, s=1)
        
        # Rellenar segmentos - SOLUCIÓN CORREGIDA PARA EL SEGMENTO 3
        segmentos = [
            [p for p in puntos_elipse if p[0] >= xc and p[1] >= yc],  # Cuadrante I
            [p for p in puntos_elipse if p[0] <= xc and p[1] >= yc],  # Cuadrante II
            [p for p in puntos_elipse if p[0] <= xc and p[1] <= yc],  # Cuadrante III
            [p for p in puntos_elipse if p[0] >= xc and p[1] <= yc]   # Cuadrante IV
        ]
        
        # Ordenar los puntos de cada segmento por ángulo para un relleno correcto
        centro = (xc, yc)
        for i, segmento in enumerate(segmentos):
            if segmento:
                # Ordenar los puntos por ángulo respecto al centro
                # Para el cuadrante III (segmento 2), ordenar en sentido antihorario
                if i == 2:  # Cuadrante III
                    segmento_ordenado = sorted(segmento, key=lambda p: math.atan2(centro[1]-p[1], centro[0]-p[0]), reverse=True)
                else:
                    segmento_ordenado = sorted(segmento, key=lambda p: math.atan2(p[1]-centro[1], p[0]-centro[0]))
                
                xs = [centro[0]] + [p[0] for p in segmento_ordenado] + [centro[0]]
                ys = [centro[1]] + [p[1] for p in segmento_ordenado] + [centro[1]]
                ax.fill(xs, ys, color=colores_segmentos_elipse[i], alpha=0.3)
        
        # Ajustar límites
        margen = max(rx, ry) + 10
        ax.set_xlim(xc - margen, xc + margen)
        ax.set_ylim(yc - margen, yc + margen)
        
        # Redibujar
        canvas.draw()
        
        # Mostrar tablas por cuadrante
        mostrar_tablas_elipse(cuadrante1, cuadrante2, cuadrante3, cuadrante4)
        
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")


# Función para mostrar las tablas de la elipse por cuadrante
def mostrar_tablas_elipse(cuadrante1, cuadrante2, cuadrante3, cuadrante4):
    # Limpiar el frame de la tabla
    for widget in frame_tabla_elipse.winfo_children():
        widget.destroy()

    # Crear un frame principal con scrollbar
    main_frame = tk.Frame(frame_tabla_elipse)
    main_frame.pack(fill='both', expand=True)

    # Crear un canvas y scrollbar
    canvas_tabla = tk.Canvas(main_frame)
    scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas_tabla.yview)
    scrollable_frame = tk.Frame(canvas_tabla)

    # Configurar el canvas
    canvas_tabla.configure(yscrollcommand=scrollbar.set)
    canvas_tabla.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    canvas_tabla.create_window((0, 0), window=scrollable_frame, anchor='nw')
    scrollable_frame.bind('<Configure>', lambda e: canvas_tabla.configure(scrollregion=canvas_tabla.bbox('all')))

    # Función para crear una tabla de cuadrante
    def crear_tabla_cuadrante(frame, datos, titulo):
        frame_cuadrante = tk.Frame(frame, bd=2, relief='groove')
        tk.Label(frame_cuadrante, text=titulo, font=('Arial', 10, 'bold')).pack()
        
        # Crear widget Text con scrollbar
        text_frame = tk.Frame(frame_cuadrante)
        text_frame.pack(fill='both', expand=True)
        
        text = tk.Text(text_frame, height=10, width=30, wrap='none')
        scroll = tk.Scrollbar(text_frame, command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        
        scroll.pack(side='right', fill='y')
        text.pack(side='left', fill='both', expand=True)
        
        # Insertar datos
        text.insert('end', f"{'Iter':<5}{'X':<10}{'Y':<10}{'Pk':<10}\n")
        text.insert('end', '-'*35 + '\n')
        
        for i, (x, y, pk) in enumerate(datos):
            text.insert('end', f"{i:<5}{x:<10}{y:<10}{pk:<10.2f}\n")
        
        text.config(state='disabled')
        return frame_cuadrante

    # Crear tablas para cada cuadrante
    frame_tablas = tk.Frame(scrollable_frame)
    frame_tablas.pack(fill='both', expand=True, padx=10, pady=10)

    # Cuadrante 1 (Superior derecho)
    frame_c1 = crear_tabla_cuadrante(frame_tablas, cuadrante1, "Cuadrante I (Superior derecho)")
    frame_c1.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    # Cuadrante 2 (Superior izquierdo)
    frame_c2 = crear_tabla_cuadrante(frame_tablas, cuadrante2, "Cuadrante II (Superior izquierdo)")
    frame_c2.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

    # Cuadrante 3 (Inferior izquierdo)
    frame_c3 = crear_tabla_cuadrante(frame_tablas, cuadrante3, "Cuadrante III (Inferior izquierdo)")
    frame_c3.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    # Cuadrante 4 (Inferior derecho)
    frame_c4 = crear_tabla_cuadrante(frame_tablas, cuadrante4, "Cuadrante IV (Inferior derecho)")
    frame_c4.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

    # Configurar el grid
    frame_tablas.grid_rowconfigure(0, weight=1)
    frame_tablas.grid_rowconfigure(1, weight=1)
    frame_tablas.grid_columnconfigure(0, weight=1)
    frame_tablas.grid_columnconfigure(1, weight=1)

# Función para dibujar una elipse usando el algoritmo del punto medio (horizontal)
def draw_ellipse_midpoint(xc, yc, rx, ry):
    points = []
    x = 0
    y = ry
    rx2 = rx * rx
    ry2 = ry * ry
    p = ry2 - rx2 * ry + 0.25 * rx2
    
    # Región 1
    while ry2 * x < rx2 * y:
        points.append((x + xc, y + yc))
        points.append((-x + xc, y + yc))
        points.append((x + xc, -y + yc))
        points.append((-x + xc, -y + yc))
        
        if p < 0:
            x += 1
            p += 2 * ry2 * x + ry2
        else:
            x += 1
            y -= 1
            p += 2 * ry2 * x - 2 * rx2 * y + ry2
    
    # Región 2
    p = ry2 * (x + 0.5) * (x + 0.5) + rx2 * (y - 1) * (y - 1) - rx2 * ry2
    
    while y >= 0:
        points.append((x + xc, y + yc))
        points.append((-x + xc, y + yc))
        points.append((x + xc, -y + yc))
        points.append((-x + xc, -y + yc))
        
        if p > 0:
            y -= 1
            p += -2 * rx2 * y + rx2
        else:
            x += 1
            y -= 1
            p += 2 * ry2 * x - 2 * rx2 * y + rx2
    
    return points

# Función para cambiar el color de la elipse
def cambiar_color_elipse():
    global color_elipse
    color = colorchooser.askcolor(title="Seleccionar color de la elipse")[1]
    if color:
        color_elipse = color
        calcular_y_graficar_elipse()

# Función para cambiar el color de un segmento de la elipse
def cambiar_color_segmento_elipse(segmento):
    global colores_segmentos_elipse
    color = colorchooser.askcolor(title=f"Seleccionar color para el segmento {segmento + 1}")[1]
    if color:
        colores_segmentos_elipse[segmento] = color
        calcular_y_graficar_elipse()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Aplicación de Gráficos")
root.state('zoomed')  # Pantalla completa

# Frame de inicio
frame_inicio = tk.Frame(root)
tk.Label(frame_inicio, text="Pantalla de Inicio", font=("Arial", 16)).pack(pady=20)
tk.Button(frame_inicio, text="1. Selección de Trazado", command=mostrar_menu_trazado, width=20).pack(pady=10)
tk.Button(frame_inicio, text="2. Opciones", command=mostrar_menu_opciones, width=20).pack(pady=10)
tk.Button(frame_inicio, text="3. Salir", command=root.destroy, width=20).pack(pady=10)

# Frame de selección de trazado
frame_trazado = tk.Frame(root)
tk.Label(frame_trazado, text="Selección de Trazado", font=("Arial", 16)).pack(pady=20)
tk.Button(frame_trazado, text="1. Línea Recta", command=mostrar_linea_recta, width=20).pack(pady=10)
tk.Button(frame_trazado, text="2. Triángulo", command=mostrar_triangulo, width=20).pack(pady=10)
tk.Button(frame_trazado, text="3. Círculo", command=mostrar_circulo, width=20).pack(pady=10)
tk.Button(frame_trazado, text="4. Elipse", command=mostrar_elipse, width=20).pack(pady=10)  # Nueva opción
tk.Button(frame_trazado, text="5. Regresar", command=mostrar_pantalla_inicio, width=20).pack(pady=10)

# Frame de opciones
frame_opciones = tk.Frame(root)
tk.Label(frame_opciones, text="Opciones", font=("Arial", 16)).pack(pady=20)

# Botones para cambiar la resolución
tk.Label(frame_opciones, text="Cambiar Resolución:", font=("Arial", 12)).pack(pady=5)
tk.Button(frame_opciones, text="HD (1280x720)", command=lambda: root.geometry("1280x720"), width=20).pack(pady=5)
tk.Button(frame_opciones, text="Full HD (1920x1080)", command=lambda: root.geometry("1920x1080"), width=20).pack(pady=5)
tk.Button(frame_opciones, text="2K (2560x1440)", command=lambda: root.geometry("2560x1440"), width=20).pack(pady=5)
tk.Button(frame_opciones, text="4K (3840x2160)", command=lambda: root.geometry("3840x2160"), width=20).pack(pady=5)

# Botón de regresar
tk.Button(frame_opciones, text="Regresar", command=mostrar_pantalla_inicio, width=20).pack(pady=10)

# Frame de línea recta
frame_linea_recta = tk.Frame(root, padx=20, pady=20, width=400, height=600)
frame_linea_recta.pack_propagate(False)  # Evita que el frame se ajuste al contenido
tk.Label(frame_linea_recta, text="Línea Recta - Método DDA", font=("Arial", 12, "bold")).pack(pady=5)

# Entradas de datos para la línea recta
entry_xa = tk.Entry(frame_linea_recta, width=10)
tk.Label(frame_linea_recta, text="Xa:").pack()
entry_xa.pack()

entry_ya = tk.Entry(frame_linea_recta, width=10)
tk.Label(frame_linea_recta, text="Ya:").pack()
entry_ya.pack()

entry_xb = tk.Entry(frame_linea_recta, width=10)
tk.Label(frame_linea_recta, text="Xb:").pack()
entry_xb.pack()

entry_yb = tk.Entry(frame_linea_recta, width=10)
tk.Label(frame_linea_recta, text="Yb:").pack()
entry_yb.pack()

# Botón de cálculo
tk.Button(frame_linea_recta, text="Calcular y Graficar", command=calcular_y_graficar, bg="green", fg="white").pack(pady=10)

# Resultado de la pendiente
label_resultado = tk.Label(frame_linea_recta, text="Pendiente (m): ", font=("Arial", 12))
label_resultado.pack(pady=5)

# Etiqueta para mostrar las coordenadas del mouse
label_coordenadas = tk.Label(frame_linea_recta, text="Coordenadas: ", font=("Arial", 10))
label_coordenadas.pack(pady=5)

# Campos de entrada para el zoom manual
tk.Label(frame_linea_recta, text="Zoom Manual", font=("Arial", 12, "bold")).pack(pady=10)

tk.Label(frame_linea_recta, text="Limite X Min:").pack()
entry_lim_x_min = tk.Entry(frame_linea_recta, width=10)
entry_lim_x_min.pack()

tk.Label(frame_linea_recta, text="Limite X Max:").pack()
entry_lim_x_max = tk.Entry(frame_linea_recta, width=10)
entry_lim_x_max.pack()

tk.Label(frame_linea_recta, text="Limite Y Min:").pack()
entry_lim_y_min = tk.Entry(frame_linea_recta, width=10)
entry_lim_y_min.pack()

tk.Label(frame_linea_recta, text="Limite Y Max:").pack()
entry_lim_y_max = tk.Entry(frame_linea_recta, width=10)
entry_lim_y_max.pack()

# Botón de zoom manual
tk.Button(frame_linea_recta, text="Aplicar Zoom", command=zoom_manual, bg="blue", fg="white").pack(pady=10)

# Botón de limpieza
tk.Button(frame_linea_recta, text="Limpiar Gráfica", command=limpiar_grafica, bg="red", fg="white").pack(pady=10)

# Botón para regresar al menú
tk.Button(frame_linea_recta, text="Regresar al Menú", command=mostrar_pantalla_inicio, bg="gray", fg="white").pack(pady=10)


# Frame de tabla para la línea recta
frame_tabla = tk.Frame(frame_linea_recta, pady=10)
frame_tabla.pack(fill='both', expand=True)

# Frame de triángulo
frame_triangulo = tk.Frame(root, padx=20, pady=20, width=550, height=600)
frame_triangulo.pack_propagate(False)  # Evita que el frame se ajuste al contenido
tk.Label(frame_triangulo, text="Triángulo Relleno - Método DDA", font=("Arial", 12, "bold")).pack(pady=5)

# Entradas para el triángulo
tk.Label(frame_triangulo, text="Punto 1 (X1, Y1):").pack()
entry_x1 = tk.Entry(frame_triangulo, width=10)
entry_x1.pack()
entry_y1 = tk.Entry(frame_triangulo, width=10)
entry_y1.pack()

tk.Label(frame_triangulo, text="Punto 2 (X2, Y2):").pack()
entry_x2 = tk.Entry(frame_triangulo, width=10)
entry_x2.pack()
entry_y2 = tk.Entry(frame_triangulo, width=10)
entry_y2.pack()

tk.Label(frame_triangulo, text="Punto 3 (X3, Y3):").pack()
entry_x3 = tk.Entry(frame_triangulo, width=10)
entry_x3.pack()
entry_y3 = tk.Entry(frame_triangulo, width=10)
entry_y3.pack()

# Frame para botones de cálculo y color
frame_botones_triangulo = tk.Frame(frame_triangulo)
frame_botones_triangulo.pack(pady=10)

# Botones
tk.Button(
    frame_botones_triangulo, 
    text="Calcular Triángulo", 
    command=calcular_y_graficar_triangulo, 
    bg="purple", 
    fg="white"
).pack(side='left', padx=5)

tk.Button(
    frame_botones_triangulo, 
    text="Cambiar Color", 
    command=cambiar_color_triangulo, 
    bg="blue", 
    fg="white"
).pack(side='left', padx=5)

# Etiquetas para mostrar las pendientes de las líneas del triángulo
label_pendiente1 = tk.Label(frame_triangulo, text="Pendiente Línea 1 (m): ", font=("Arial", 10))
label_pendiente1.pack(pady=5)

label_pendiente2 = tk.Label(frame_triangulo, text="Pendiente Línea 2 (m): ", font=("Arial", 10))
label_pendiente2.pack(pady=5)

label_pendiente3 = tk.Label(frame_triangulo, text="Pendiente Línea 3 (m): ", font=("Arial", 10))
label_pendiente3.pack(pady=5)

# Campos de entrada para el zoom manual en el triángulo
tk.Label(frame_triangulo, text="Zoom Manual", font=("Arial", 12, "bold")).pack(pady=10)

# Frame para los límites de X
frame_zoom_x = tk.Frame(frame_triangulo)
frame_zoom_x.pack()

tk.Label(frame_zoom_x, text="Limite X Min:").grid(row=0, column=0, padx=5)
entry_lim_x_min_triangulo = tk.Entry(frame_zoom_x, width=10)
entry_lim_x_min_triangulo.grid(row=0, column=1, padx=5)

tk.Label(frame_zoom_x, text="Limite X Max:").grid(row=0, column=2, padx=5)
entry_lim_x_max_triangulo = tk.Entry(frame_zoom_x, width=10)
entry_lim_x_max_triangulo.grid(row=0, column=3, padx=5)

# Frame para los límites de Y
frame_zoom_y = tk.Frame(frame_triangulo)
frame_zoom_y.pack()

tk.Label(frame_zoom_y, text="Limite Y Min:").grid(row=0, column=0, padx=5)
entry_lim_y_min_triangulo = tk.Entry(frame_zoom_y, width=10)
entry_lim_y_min_triangulo.grid(row=0, column=1, padx=5)

tk.Label(frame_zoom_y, text="Limite Y Max:").grid(row=0, column=2, padx=5)
entry_lim_y_max_triangulo = tk.Entry(frame_zoom_y, width=10)
entry_lim_y_max_triangulo.grid(row=0, column=3, padx=5)

# Frame para los botones de zoom y limpiar
frame_botones_zoom = tk.Frame(frame_triangulo)
frame_botones_zoom.pack(pady=10)

tk.Button(frame_botones_zoom, text="Aplicar Zoom", command=zoom_manual_triangulo, bg="blue", fg="white").grid(row=0, column=0, padx=5)
tk.Button(frame_botones_zoom, text="Limpiar Gráfica", command=limpiar_grafica, bg="red", fg="white").grid(row=0, column=1, padx=5)

# Frame de tabla para el triángulo
frame_tabla_triangulo = tk.Frame(frame_triangulo, pady=10)
frame_tabla_triangulo.pack(fill='both', expand=True)

# Botón para regresar al menú
tk.Button(frame_triangulo, text="Regresar al Menú", command=mostrar_pantalla_inicio, bg="gray", fg="white").pack(pady=10)

# Frame de gráfica
frame_grafica = tk.Frame(root, padx=10, pady=10, bg='white')

# Frame de tabla para la línea recta
frame_tabla = tk.Frame(frame_linea_recta, pady=10)
frame_tabla.pack(fill='both', expand=True)

# Frame de círculo
frame_circulo = tk.Frame(root, padx=20, pady=20, width=680, height=600)
frame_circulo.pack_propagate(False)  # Evita que el frame se ajuste al contenido
tk.Label(frame_circulo, text="Círculo - Método del Punto Medio", font=("Arial", 12, "bold")).pack(pady=5)

# Frame para las entradas de Xc, Yc y R
frame_entradas = tk.Frame(frame_circulo)
frame_entradas.pack(pady=10)

# Entrada para Xc
tk.Label(frame_entradas, text="Xc:").grid(row=0, column=0, padx=5)
entry_xc = tk.Entry(frame_entradas, width=10)
entry_xc.grid(row=0, column=1, padx=5)

# Entrada para Yc
tk.Label(frame_entradas, text="Yc:").grid(row=0, column=2, padx=5)
entry_yc = tk.Entry(frame_entradas, width=10)
entry_yc.grid(row=0, column=3, padx=5)

# Entrada para R
tk.Label(frame_entradas, text="R:").grid(row=0, column=4, padx=5)
entry_radio = tk.Entry(frame_entradas, width=10)
entry_radio.grid(row=0, column=5, padx=5)

# Frame para los botones
frame_botones = tk.Frame(frame_circulo)
frame_botones.pack(pady=10)

# Botón para calcular y graficar el círculo
tk.Button(frame_botones, text="Calcular Círculo", command=calcular_y_graficar_circulo, bg="orange", fg="white").grid(row=0, column=0, padx=5)

# Botón para limpiar la pantalla
tk.Button(frame_botones, text="Limpiar Pantalla", command=limpiar_grafica, bg="red", fg="white").grid(row=0, column=1, padx=5)

# Agregar entradas y botón para mover el círculo
tk.Label(frame_circulo, text="Mover Círculo a Nueva Posición", font=("Arial", 12, "bold")).pack(pady=10)
frame_mover_circulo = tk.Frame(frame_circulo)
frame_mover_circulo.pack(pady=5)

# Entrada para nueva Xc
tk.Label(frame_mover_circulo, text="Nuevo Xc:").grid(row=0, column=0, padx=5)
entry_nuevo_xc = tk.Entry(frame_mover_circulo, width=10)
entry_nuevo_xc.grid(row=0, column=1, padx=5)

# Entrada para nueva Yc
tk.Label(frame_mover_circulo, text="Nuevo Yc:").grid(row=0, column=2, padx=5)
entry_nuevo_yc = tk.Entry(frame_mover_circulo, width=10)
entry_nuevo_yc.grid(row=0, column=3, padx=5)

# Botón para mover el círculo
tk.Button(frame_mover_circulo, text="Mover Círculo", command=mover_circulo, bg="blue", fg="white").grid(row=0, column=4, padx=5)

# Agregar controles de zoom
tk.Label(frame_circulo, text="Zoom Manual", font=("Arial", 12, "bold")).pack(pady=10)
frame_zoom = tk.Frame(frame_circulo)
frame_zoom.pack(pady=5)

# Entradas de zoom
tk.Label(frame_zoom, text="X Min:").grid(row=0, column=0, padx=5)
entry_lim_x_min = tk.Entry(frame_zoom, width=10)
entry_lim_x_min.grid(row=0, column=1, padx=5)

tk.Label(frame_zoom, text="X Max:").grid(row=0, column=2, padx=5)
entry_lim_x_max = tk.Entry(frame_zoom, width=10)
entry_lim_x_max.grid(row=0, column=3, padx=5)

tk.Label(frame_zoom, text="Y Min:").grid(row=1, column=0, padx=5)
entry_lim_y_min = tk.Entry(frame_zoom, width=10)
entry_lim_y_min.grid(row=1, column=1, padx=5)

tk.Label(frame_zoom, text="Y Max:").grid(row=1, column=2, padx=5)
entry_lim_y_max = tk.Entry(frame_zoom, width=10)
entry_lim_y_max.grid(row=1, column=3, padx=5)

# Botón de zoom
tk.Button(frame_zoom, text="Aplicar Zoom", command=zoom_manual, bg="blue", fg="white").grid(row=2, column=1, columnspan=2, pady=5)

# Frame de tabla para el círculo
frame_tabla_circulo = tk.Frame(frame_circulo, pady=10)
frame_tabla_circulo.pack(fill='both', expand=True)

# Botón para regresar al menú
tk.Button(frame_circulo, text="Regresar al Menú", command=mostrar_pantalla_inicio, bg="gray", fg="white").pack(pady=10)

# Frame de gráfica
frame_grafica = tk.Frame(root, padx=10, pady=10, bg='white')

# Frame de elipse
frame_elipse = tk.Frame(root, padx=20, pady=20, width=550, height=600)
frame_elipse.pack_propagate(False)  # Evita que el frame se ajuste al contenido
tk.Label(frame_elipse, text="Elipse - Método del Punto Medio", font=("Arial", 12, "bold")).pack(pady=5)

# Entradas para la elipse
tk.Label(frame_elipse, text="Centro (Xc, Yc):").pack()
entry_xc_elipse = tk.Entry(frame_elipse, width=10)
entry_xc_elipse.pack()
entry_yc_elipse = tk.Entry(frame_elipse, width=10)
entry_yc_elipse.pack()

tk.Label(frame_elipse, text="Radio X (rx):").pack()
entry_rx_elipse = tk.Entry(frame_elipse, width=10)
entry_rx_elipse.pack()

tk.Label(frame_elipse, text="Radio Y (ry):").pack()
entry_ry_elipse = tk.Entry(frame_elipse, width=10)
entry_ry_elipse.pack()

# Frame para botones de la elipse
frame_botones_elipse = tk.Frame(frame_elipse)
frame_botones_elipse.pack(pady=10)

# Botón para graficar la elipse
tk.Button(frame_botones_elipse, text="Graficar Elipse", command=calcular_y_graficar_elipse, bg="green", fg="white").pack(side='left', padx=5)

# Botón para cambiar el color de la elipse
tk.Button(frame_botones_elipse, text="Cambiar Color", command=cambiar_color_elipse, bg="blue", fg="white").pack(side='left', padx=5)

# Botón para limpiar la gráfica
tk.Button(frame_botones_elipse, text="Limpiar Gráfica", command=limpiar_grafica, bg="red", fg="white").pack(side='left', padx=5)

# Frame para cambiar colores de los segmentos de la elipse
frame_colores_segmentos = tk.Frame(frame_elipse)
frame_colores_segmentos.pack(pady=10)

# Botones para cambiar el color de cada segmento de la elipse
for i in range(4):
    tk.Button(
        frame_colores_segmentos, 
        text=f"Color Segmento {i+1}", 
        command=lambda i=i: cambiar_color_segmento_elipse(i), 
        bg=colores_segmentos_elipse[i], 
        fg="white"
    ).pack(side='left', padx=5)

# Campos de entrada para el zoom manual en la elipse
tk.Label(frame_elipse, text="Zoom Manual", font=("Arial", 12, "bold")).pack(pady=10)

# Frame para los límites de X
frame_zoom_x_elipse = tk.Frame(frame_elipse)
frame_zoom_x_elipse.pack()

tk.Label(frame_zoom_x_elipse, text="Limite X Min:").grid(row=0, column=0, padx=5)
entry_lim_x_min_elipse = tk.Entry(frame_zoom_x_elipse, width=10)
entry_lim_x_min_elipse.grid(row=0, column=1, padx=5)

tk.Label(frame_zoom_x_elipse, text="Limite X Max:").grid(row=0, column=2, padx=5)
entry_lim_x_max_elipse = tk.Entry(frame_zoom_x_elipse, width=10)
entry_lim_x_max_elipse.grid(row=0, column=3, padx=5)

# Frame para los límites de Y
frame_zoom_y_elipse = tk.Frame(frame_elipse)
frame_zoom_y_elipse.pack()

tk.Label(frame_zoom_y_elipse, text="Limite Y Min:").grid(row=0, column=0, padx=5)
entry_lim_y_min_elipse = tk.Entry(frame_zoom_y_elipse, width=10)
entry_lim_y_min_elipse.grid(row=0, column=1, padx=5)

tk.Label(frame_zoom_y_elipse, text="Limite Y Max:").grid(row=0, column=2, padx=5)
entry_lim_y_max_elipse = tk.Entry(frame_zoom_y_elipse, width=10)
entry_lim_y_max_elipse.grid(row=0, column=3, padx=5)

# Frame para los botones de zoom y limpiar
frame_botones_zoom_elipse = tk.Frame(frame_elipse)
frame_botones_zoom_elipse.pack(pady=10)

# Botón para aplicar zoom manual
tk.Button(frame_botones_zoom_elipse, text="Aplicar Zoom", command=zoom_manual_elipse, bg="blue", fg="white").grid(row=0, column=0, padx=5)

# Frame para la tabla de la elipse
frame_tabla_elipse = tk.Frame(frame_elipse, pady=10)
frame_tabla_elipse.pack(fill='both', expand=True)

# Botón para regresar al menú
tk.Button(frame_elipse, text="Regresar al Menú", command=mostrar_pantalla_inicio, bg="gray", fg="white").pack(pady=10)

# Inicializar la gráfica vacía
inicializar_grafica()

# Mostrar pantalla de inicio al iniciar
mostrar_pantalla_inicio()

root.mainloop()