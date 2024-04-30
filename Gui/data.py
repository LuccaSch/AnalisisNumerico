import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from main import *


ruta = pathlib.Path('.')
ruta = ruta / "QuakeProgram" / "Imputs" / "terremoto1.txt"


def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Función para realizar la transformación
def transformar(frame):
    if(not(respuesta[5])):
        respuesta[5]=True
        
        limpiar_frame(frame)
        
        # Crear la segunda gráfica (fig2)
        
        fig2 = Grafica(respuesta[3], respuesta[2], "FFT Terremoto2.txt", "s", "m/s^2")

        # Crear un nuevo lienzo para la segunda gráfica
        canvas2 = FigureCanvasTkAgg(fig2, master=frame_grafica)
        
        # Dibujar la segunda gráfica en el lienzo
        canvas2.draw()

        # Empaquetar el widget del lienzo de la segunda gráfica en el mismo lugar que la primera gráfica
        canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        plt.close('all')
        

# Función para realizar la antitransformación
def antitransformar(frame):
     if(respuesta[5]):
        respuesta[5]=False
        
        limpiar_frame(frame)
        
        # Crear la segunda gráfica (fig2)
        
        fig2 = Grafica(respuesta[0], respuesta[1], "FFT Terremoto2.txt", "s", "m/s^2")

        # Crear un nuevo lienzo para la segunda gráfica
        canvas2 = FigureCanvasTkAgg(fig2, master=frame_grafica)
        
        # Dibujar la segunda gráfica en el lienzo
        canvas2.draw()

        # Empaquetar el widget del lienzo de la segunda gráfica en el mismo lugar que la primera gráfica
        canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        plt.close('all')

# Función para realizar la convolución
def convolucionar():
    # Agregar aquí la lógica para la convolución
    print("Convolucionar")

def analisar():
    # Agregar aquí la lógica para la convolución
    print("Analisar")
    
def anterior():
    # Agregar aquí la lógica para la convolución
    print("Anterior")
    
def posterior():
    # Agregar aquí la lógica para la convolución
    print("Posterior")
    
# Crear ventana Tkinter
root = tk.Tk()
root.title("QuakeProgram")
root.geometry("850x550")  # Tamaño fijo de la ventana
root.configure(bg="#2A2F4F")  # Color de fondo de la ventana

# Crear un marco superior para el título
title_frame = ttk.Frame(root, height=50, relief=tk.RAISED, borderwidth=2, style='Title.TFrame')
title_frame.pack(fill=tk.X)

# Crear un label con el nombre del programa
title_label = ttk.Label(title_frame, text="QuakeProgram", style='Title.TLabel')
title_label.pack(pady=10)

# Crear un marco para la gráfica
frame_grafica = ttk.Frame(root)
frame_grafica.pack(side=tk.TOP, padx=10, pady=10)

# Crear una figura de Matplotlib

respuesta=descomprimirtxt(ruta)

fig = Grafica(respuesta[0],respuesta[1],"Terremoto1.txt","s","m/s^2")
canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
plt.close(fig)


#BOTONES

s = ttk.Style()
s.configure('TFrame', background="#2A2F4F")  # Cambiar el color de fondo a azul

# Crear un marco para los botones
frame_botones = ttk.Frame(root, style='TFrame')
frame_botones.pack(side=tk.BOTTOM, pady=10)

# Crear los botones
btn_anterior= ttk.Button(frame_botones, text="Anterior", command=anterior())
btn_anterior.pack(side=tk.LEFT, padx=5)

btn_transformar = ttk.Button(frame_botones, text="Transformar", command=lambda:transformar(frame_grafica))
btn_transformar.pack(side=tk.LEFT, padx=5)

btn_antitransformar = ttk.Button(frame_botones, text="Antitransformar", command=lambda:antitransformar((frame_grafica)))
btn_antitransformar.pack(side=tk.LEFT, padx=5)

btn_convolucionar = ttk.Button(frame_botones, text="Convolucionar", command=convolucionar)
btn_convolucionar.pack(side=tk.LEFT, padx=5)

btn_analisar = ttk.Button(frame_botones, text="Analisar", command=analisar)
btn_analisar.pack(side=tk.LEFT, padx=5)

btn_posterior = ttk.Button(frame_botones, text="Posterior", command=posterior)
btn_posterior.pack(side=tk.LEFT, padx=5)

    

# Ejecutar la aplicación
root.mainloop()