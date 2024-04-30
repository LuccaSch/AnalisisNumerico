import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import QuakeProgram.Ventanas.ventanas as ven
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from main import *


#Defino una lista y su indice que llevara todos los datos de los terremotos
respuestas=[]
pun=0
verificador = []
#Defino varios path utiles para operar en el programa
ruta = pathlib.Path('.')

ruta = ruta / "QuakeProgram"

imp= ruta / "Imputs"

archivo_output=ruta / "Outputs"

#Obtengo los nombres de los archivos de inputs
archivo=obtener_archivos_en_directorio(imp)

for indice in archivo:
    direc = ruta / "Imputs" / indice
    respuesta=descomprimirtxt(direc)
    #esto es sucio pero mas tarde me di cuenta que quiero el indice
    respuesta.append(indice)
    verificador.append(False)
    respuestas.append(respuesta)


def convolucionar(frame):
    global respuestas
    global pun
    
    
    nombre_ventana = input("Ingrese el nombre de la función que desea ejecutar: ")
    funcion = getattr(ven, nombre_ventana, None)
    if funcion:
        h = funcion()  # Ejecutamos la función y guardamos el resultado
        señal_suavizada = np.convolve(respuestas[pun][1], h, mode='same') #convolucionamos la loma h con nuestra funcion, la longitud quedara como len(t) ya que usamos el mode ´same´ para facilitarnos mas adelante
        trafo_suavizada = np.abs((np.fft.fft(señal_suavizada)/len(respuestas[pun][0]))*2) #hacemos la trasformada de fourier de la funcion suavizada
        respuestas[pun][1]=señal_suavizada
        respuestas[pun][3]=trafo_suavizada
        if(verificador[pun]):
            transformar(frame)
        else:
            antitransformar(frame)
    else:
        print("La función especificada no existe")    
    return
    
      
    
   # h = ventana_gausiana() #elegimos un suavizado de 3 pero podriamos suvirlo para suavizar mas la funcion
    #señal_suavizada = np.convolve(respuestas[pun][1], h, mode='same') #convolucionamos la loma h con nuestra funcion, la longitud quedara como len(t) ya que usamos el mode ´same´ para facilitarnos mas adelante
    #trafo_suavizada = np.abs((np.fft.fft(señal_suavizada)/len(respuestas[pun][0]))*2) #hacemos la trasformada de fourier de la funcion suavizada
    #respuestas[pun][1]=señal_suavizada
    #respuestas[pun][3]=trafo_suavizada
    #if(verificador[pun]):
    #    transformar(frame)
    #else:
    #    antitransformar(frame)
    return

def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
# Función para realizar la transformación

def transformar(frame):
    global pun
    global verificador
    global respuestas
    #if(not(verificador[pun])):
    verificador[pun]=True
    
    limpiar_frame(frame)
    
    # Crear la segunda gráfica (fig2)
    
    nombre="FFT "+respuestas[pun][5]
    print(nombre)
    
    fig2 = Grafica(respuestas[pun][2], respuestas[pun][3], nombre, "Hz", "m/s^2")

    # Crear un nuevo lienzo para la segunda gráfica
    canvas2 = FigureCanvasTkAgg(fig2, master=frame_grafica)
    
    # Dibujar la segunda gráfica en el lienzo
    canvas2.draw()

    # Empaquetar el widget del lienzo de la segunda gráfica en el mismo lugar que la primera gráfica
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    plt.close('all')
# Función para realizar la antitransformación

def antitransformar(frame):
    global pun
    global verificador
    global respuestas
    #if(verificador[pun]==1.0):
    verificador[pun]=False
    
    limpiar_frame(frame)
    
    # Crear la segunda gráfica (fig2)
    
    nombre=respuestas[pun][5]
    
    fig2 = Grafica(respuestas[pun][0], respuestas[pun][1], nombre, "s", "m/s^2")

    # Crear un nuevo lienzo para la segunda gráfica
    canvas2 = FigureCanvasTkAgg(fig2, master=frame_grafica)
    
    # Dibujar la segunda gráfica en el lienzo
    canvas2.draw()

    # Empaquetar el widget del lienzo de la segunda gráfica en el mismo lugar que la primera gráfica
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    plt.close('all')
# Función para realizar la convolución

def analisar():
    # Agregar aquí la lógica para la convolución
    print("Analisar")
    
def anterior(frame):
    global pun
    global verificador
    global respuestas
    if(pun>0):
        pun=pun-1
        if(verificador[pun]):
            transformar(frame)
        else:
            antitransformar(frame)
    else:
        print("Primer Elemento")
            
    
def posterior(frame):
    global pun
    global verificador
    global respuestas
    tam=len(verificador)-1
    if(pun==tam):
        print("Ultimo elemento")
    else:
        pun=pun+1
        if(verificador[pun]):
            transformar(frame)
        else:
            antitransformar(frame)
    
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

fig = Grafica(respuestas[pun][0],respuestas[pun][1],"Terremoto1.txt","s","m/s^2")
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
btn_anterior= ttk.Button(frame_botones, text="<-- Anterior", command=lambda: anterior(frame_grafica))
btn_anterior.pack(side=tk.LEFT, padx=5)

btn_transformar = ttk.Button(frame_botones, text="Transformar", command=lambda: transformar(frame_grafica))
btn_transformar.pack(side=tk.LEFT, padx=5)

btn_antitransformar = ttk.Button(frame_botones, text="Antitransformar", command=lambda: antitransformar(frame_grafica))
btn_antitransformar.pack(side=tk.LEFT, padx=5)

btn_convolucionar = ttk.Button(frame_botones, text="Convolucionar", command=lambda: convolucionar(frame_grafica))
btn_convolucionar.pack(side=tk.LEFT, padx=5)

btn_analisar = ttk.Button(frame_botones, text="Analisar", command=analisar)
btn_analisar.pack(side=tk.LEFT, padx=5)

btn_posterior = ttk.Button(frame_botones, text="Posterior -->", command=lambda: posterior(frame_grafica))
btn_posterior.pack(side=tk.LEFT, padx=5)

    

# Ejecutar la aplicación
root.mainloop()