import pathlib
from pathlib import Path
import os

import tkinter as tk
from tkinter import simpledialog, messagebox, PhotoImage, ttk, Canvas, filedialog

import numpy as np
import matplotlib.pyplot as plt
import QuakeProgram.Ventanas.ventanas as ventanas_convolucion

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#VARIABLES GLOBALES 
#Defino una lista y su indice que llevara todos los datos de los terremotos
respuestas=[]
# pun es el puntero que señala al terremoto dentro de respuestas en el que estamos parado respuestas[pun]=terremoto actual
pun=0 
#verificador estaba dentro e respuestas pero daba problemas es una lista de boleanos tal que verificador[pun] es falso si la funcion quedo sin trasformar y viseversa
verificador = []

#PHATS
ruta = pathlib.Path('.')

rutaGuiAssets=ruta / "Gui" / "assets" / "frame0"

rutaLogo=rutaGuiAssets / "QuakeProgramLogo.ico"

ruta = ruta / "QuakeProgram"

imp= ruta / "Imputs"

ruta_output=ruta / "Outputs"

#FUNCIONES
#Verificar archivos
def obtener_archivos_en_directorio(ruta):
    # Obtener la lista de archivos y directorios en la ruta especificada
    contenido = os.listdir(ruta)
    
    # Retornar solo los archivos (excluir directorios)
    archivos = [archivo for archivo in contenido if os.path.isfile(os.path.join(ruta, archivo))]
    
    return archivos

def descomprimirtxt(ruta):
    #a
    
    respuesta=[]
    
    funcion_t= np.loadtxt(ruta) #Trae el txt y lo almacena en un array de np donde funcion_t[0] son los t[] y funcion_t[1] son los ft[]
    t= funcion_t[:, 0] #Los llevamos a variables para que sea mas facil de manejar 
    ft=funcion_t[:, 1]
    coeficiente_fourier = (np.fft.fft(ft)/len(t))*2 #Sacamos los coeficientes de la serie de fourier para cada pto, lo dividimos por el ancho de la entrada que seria el 1/N de la teoria
    trafo_fourier= abs(coeficiente_fourier) #Utilizamos el valor absoluto para calcular la trasformada de fourier
    frecuencia = np.fft.fftfreq(len(t),t[0]-t[1]) #Calculamos la unidades de frecuencia angular por muestra y lo dividimos por 2pi para llevarlo a Hz 
    #Usamos esta funcion para crear los txt donde se guardaran los coeficientes de fourier dentro de Outputs
    
    respuesta.append(t)
    respuesta.append(ft) #Creamos una lista de los ft que sera usada para el ejer E
    respuesta.append(frecuencia)
    respuesta.append(trafo_fourier)
    respuesta.append(coeficiente_fourier)
    return respuesta

def directorio_vacio(ruta):
    # Obtener la lista de archivos y directorios en la ruta especificada
    contenido = os.listdir(ruta)
    
    # Verificar si la lista está vacía
    if len(contenido) == 0:
        return True
    else:
        return False


#Funciones auxiliares para otras funciones
def encontrarCualRespuestas(nombre):
    for i, respuesta in enumerate(respuestas):
        if respuesta[5] == nombre:
            return i
    return -1

def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy() 

def Grafica(x,y,nombre,nombrex,nombrey):
    plt.figure()
    plt.title(nombre)
    plt.grid()
    plt.plot(x,y)
    plt.xlabel(nombrex)
    plt.ylabel(nombrey)

    # Crear una figura y sus ejes
    fig, ax = plt.subplots()

    # Graficar datos de ejemplo
    ax.plot(x, y)

    # Personalizar la figura
    ax.set_xlabel(nombrex)  # Nombre del eje X
    ax.set_ylabel(nombrey)  # Nombre del eje Y
    ax.grid(True)  # Agregar una grilla

    # Nombrar la figura
    fig.suptitle(nombre)  # Nombre de la figura

    # Devolver la figura
    return fig   

def guardar_arreglo_en_txt(arreglo, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        for elemento in arreglo:
            archivo.write(str(elemento) + '\n')

def submuestreo_terremotos(terremoto1, terremoto2):
    # Índices equidistantes para el terremoto
    indices_terremoto = np.linspace(0, len(terremoto2) - 1, len(terremoto1), dtype=int)
     # Submuestreo del segundo terremoto
    terremoto2_submuestreado = terremoto2[indices_terremoto]
    
    return terremoto2_submuestreado
    
def relative_to_assets(path: str) -> Path:
    return rutaGuiAssets / Path(path)

#Funcion del boton OPERAR que tiene 3 subbotones covolucionar, submuestrear y sumarFreq
def operar(frame):
    ventana2_botones = tk.Toplevel(root)
    ventana2_botones.title("Operar")
    ventana2_botones.iconbitmap(rutaLogo)

    # Crear un marco para contener los botones
    marco_botones2 = tk.Frame(ventana2_botones)
    marco_botones2.pack(padx=10, pady=10)
    btn_convolucionar= ttk.Button(marco_botones2, text="convolucionar",command=lambda: convolucionar(frame,ventana2_botones))
    btn_convolucionar.pack(side=tk.LEFT, padx=5)

    btn_Remuestrear = ttk.Button(marco_botones2, text="Submuestrar", command=lambda: submuestreo(frame,ventana2_botones))
    btn_Remuestrear.pack(side=tk.LEFT, padx=5) 
    
    btn_Sumarfrecuencias = ttk.Button(marco_botones2, text="Sumar frecuencias", command=lambda: sumarFrecuencias(frame,ventana2_botones))
    btn_Sumarfrecuencias.pack(side=tk.LEFT, padx=5)
    
def convolucionar(frame,ven):
    ven.destroy()
    global respuestas
    global pun
    # Mostrar cuadro de diálogo para que el usuario ingrese el texto
    nombre_ventana = simpledialog.askstring("Ingresar ventana", "Por favor ingresa la ventana:")
    
    # Verificar si se ingresó algún texto
    if nombre_ventana is not None:
        funcion = getattr(ventanas_convolucion, nombre_ventana, None)
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
            messagebox.showinfo("Convolucion exitosa",f"¡Se a convolucionado {respuestas[pun][5]} con {nombre_ventana}!")
        else:
            messagebox.showerror("Error de convolucion", "La ventana seleccionada no existe") 
    return

def submuestreo(frame,ven):
    ven.destroy()
    global pun
    global verificador
    global respuestas   
    #d
    #Para poder comprar los terremotos nesesitamos que la cantidad de datos muestreados sea la misma, para ello debemos realizar un submuestreo del terremoto2 para que tenga 4000 muestras
    nombreT = simpledialog.askstring("Remuestreo", f"Ingresar el nombre del terremoto con el cual quiere remuestrear {respuestas[pun][5]}: ")
    punaux=encontrarCualRespuestas(nombreT)
    if nombreT is not None:
        if(punaux<0):
            messagebox.showerror("Error",f"No se encontro ningun terremoto llamado {nombreT}")
        else: 
            if(len(respuestas[pun][0])<=len(respuestas[punaux][0])):
                messagebox.showerror("Error",f"El tamaño del remuestreo debe ser menor al tamaño de {respuestas[pun][5]} ({len(respuestas[pun][0])})") 
            else:
                terremoto_submuestrado=submuestreo_terremotos(respuestas[punaux][1],respuestas[pun][1])
                terremoto_submuestrado_trasf= np.abs((np.fft.fft(terremoto_submuestrado)/len(respuestas[punaux][0]))*2)
                
                respuestas[pun][1]=terremoto_submuestrado
                respuestas[pun][3]=terremoto_submuestrado_trasf
                
                t_remuestreados = respuestas[punaux][0]
                frecuencia_remuestrea = np.fft.fftfreq(len(t_remuestreados),t_remuestreados[0]-t_remuestreados[1])
                respuestas[pun][0]= t_remuestreados
                respuestas[pun][2]=frecuencia_remuestrea
                
                if(verificador[pun]):
                        transformar(frame)
                else:
                        antitransformar(frame) 

def sumarFrecuencias(frame,ven):
    ven.destroy()
    nombreT = simpledialog.askstring("Remuestreo", f"Ingresar el nombre del terremoto con el cual quiere sumar las frecuencias {respuestas[pun][5]}: ")
    punaux=encontrarCualRespuestas(nombreT)
    if nombreT is not None:
        if punaux<0:
            messagebox.showerror("Error",f"No se encontro ningun terremoto llamado {nombreT}")
        else:
            if(len(respuestas[pun][2])==len(respuestas[punaux][2])):
                respuestas[pun][3] = respuestas[pun][3]*respuestas[punaux][3]
                respuestas[pun][1] = np.fft.ifft(respuestas[pun][3])
                respuestas[pun][5] = respuestas[pun][5]+"+"+respuestas[punaux][5]    
                if(verificador[pun]):
                        transformar(frame)
                else:
                        antitransformar(frame)  
            else:
                messagebox.showerror("Error",f"Las frecuencias de los terremotos no son de igual longitud")
                                             
                                             
# Función para el Boton TRASFORMAR
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


# Función para el Boton ANTITRASFORMAR
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


#Funcion para el Boton ANALISAR que tiene 2 subotones Comparar Y analisisDeMaximos
def analisar():
    global pun
    global verificador
    global respuestas
    ventana_botones = tk.Toplevel(root)
    ventana_botones.title("Analisar")
    ventana_botones.iconbitmap(rutaLogo)

    # Crear un marco para contener los botones
    marco_botones = tk.Frame(ventana_botones)
    marco_botones.pack(padx=10, pady=10)
    btn_maximos= ttk.Button(marco_botones, text="Analisis de Maximos", command=lambda: analisisMaximos(ventana_botones))
    btn_maximos.pack(side=tk.LEFT, padx=5)

    btn_Comparar = ttk.Button(marco_botones, text="Comparar terremotos", command=lambda: compararT(ventana_botones))
    btn_Comparar.pack(side=tk.LEFT, padx=5) 
        
def compararT(ven):
    ven.destroy()
    global pun
    global verificador
    global respuestas 
    global ruta_output
    nombreT = simpledialog.askstring("Remuestreo", f"Ingresar el nombre del terremoto con el cual quiere comparar {respuestas[pun][5]}: ")
    punaux=encontrarCualRespuestas(nombreT)
    if nombreT is not None:
        if(punaux<0):
            messagebox.showerror("Error",f"No se encontro ningun terremoto llamado {nombreT}")
        else:
            if (len(respuestas[pun][0]))!=len(respuestas[punaux][0]):
                messagebox.showerror("Error",f"Ambos terremotos deben tener la misma cantidad de datos Muestreados")
            else:
                correlacionEnHz= np.correlate(respuestas[pun][3],respuestas[punaux][3],mode="valid")
                nombre="Analisis de "+ respuestas[pun][5]
                with open((ruta_output / nombre), 'a') as archivo:
                    mensaje= f"El nivel de similitud entre {respuestas[pun][5]} y {respuestas[punaux][5]} las graficas en Frecuencia es de {correlacionEnHz}.\n"
                    archivo.write(mensaje)
                    
def analisisMaximos(ven):
    ven.destroy()
    global respuestas
    global pun
    global ruta_output
   #c
    indice_max = np.argmax(respuestas[pun][3]) #Buscamos dentro de trafo_fourier el valor maximo
    frecuencia_max = abs(respuestas[pun][2][indice_max]) #La frecuencia maxima estara en frecuencia[valor_maximo]
    nombre="Analisis de "+ respuestas[pun][5]
    with open((ruta_output / nombre), 'a') as archivo: #Lo guardamos en  el archivo Respuestas dentro de Outputs
        mensaje= f"En {respuestas[pun][5]} la frecuencia mas acelerada es {frecuencia_max} y su amplitud es de {respuestas[pun][3][indice_max]}.\n"
        archivo.write(mensaje)

#Funcion De desplazamiento del puntero pun  
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
        messagebox.showinfo("Informacion",f"{respuestas[pun][5]} es el primer Terrremoto")
         
def posterior(frame):
    global pun
    global verificador
    global respuestas
    tam=len(verificador)-1
    if(pun==tam):
        messagebox.showinfo("Informacion",f"{respuestas[pun][5]} en el ultimo Terremoto")
    else:
        pun=pun+1
        if(verificador[pun]):
            transformar(frame)
        else:
            antitransformar(frame)

#GUI
if (not(directorio_vacio(imp))):
    #CASO DEL DIRECTORIO NO VACIO
    #buscamos los archivos de inputs
    archivo=obtener_archivos_en_directorio(imp)
    #Se carga la matriz respuestas[[t][x(t)][wt][X[wt]][Nombe_archivo_txt]]
    for indice in archivo:
        direc = ruta / "Imputs" / indice
        respuesta=descomprimirtxt(direc)
        #esto es sucio pero mas tarde me di cuenta que quiero el nombre del terremoto
        respuesta.append(indice)
        verificador.append(False)
        respuestas.append(respuesta)   
    # Crear ventana Tkinter que sera la raiz
    root = tk.Tk()
    root.title("QuakeProgram")
    root.iconbitmap(rutaLogo)
    root.geometry("850x800")  # Tamaño fijo de la ventana
    root.configure(bg="#2A2F4F")  # Color de fondo de la ventana

    # Crear un marco superior para el título
    title_canvas = tk.Canvas(root, height=50, relief=tk.RAISED, borderwidth=2, background='#9294C5')
    title_canvas.pack(fill=tk.X)

    # Crear un label con el nombre del programa
    title_canvas.create_text(
        61.0,
        6.0,
        anchor="nw",
        text="QuakeProgram",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = title_canvas.create_image(
        37.0,
        24.0,
        image=image_image_1
    )

    # Crear un marco para la gráfica
    frame_grafica = ttk.Frame(root)
    frame_grafica.pack(side=tk.TOP, padx=10, pady=10)

    # Crear una figura de Matplotlib

    fig = Grafica(respuestas[pun][0],respuestas[pun][1],"Terremoto1.txt","s","m/s^2")
    canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    plt.close(fig)


    #BOTONES dentro del GUI

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

    btn_operar = ttk.Button(frame_botones, text="Operar", command=lambda: operar(frame_grafica))
    btn_operar.pack(side=tk.LEFT, padx=5)

    btn_analisar = ttk.Button(frame_botones, text="Analisar", command=lambda: analisar())
    btn_analisar.pack(side=tk.LEFT, padx=5)

    btn_posterior = ttk.Button(frame_botones, text="Posterior -->", command=lambda: posterior(frame_grafica))
    btn_posterior.pack(side=tk.LEFT, padx=5)

        
    # Ejecutar la aplicación en loop, nesesario para su funcionamiento
    root.mainloop()
else:
    #CASO DIRECTORIO VACIO
    # Función para abrir la carpeta de inputs
    def abrir_carpeta_inputs():
        root.withdraw()  # Oculta la ventana principal mientras se selecciona la carpeta
        carpeta_inputs = filedialog.askdirectory(initialdir=imp)
        root.deiconify()  # Vuelve a mostrar la ventana principal después de seleccionar la carpeta
    
    
    root = tk.Tk()
    root.title("QuakeProgram")
    root.iconbitmap(rutaLogo)
    root.geometry("850x800")  # Tamaño fijo de la ventana
    root.configure(bg="#2A2F4F")  # Color de fondo de la ventana

    # Crear un marco superior para el título
    title_canvas = tk.Canvas(root, height=50, relief=tk.RAISED, borderwidth=2, background='#9294C5')
    title_canvas.pack(fill=tk.X)

    # Crear un label con el nombre del programa
    title_canvas.create_text(
        61.0,
        6.0,
        anchor="nw",
        text="QuakeProgram",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = title_canvas.create_image(
        37.0,
        24.0,
        image=image_image_1
    )
    # Crear canvas para el mensaje de "No se encontraron archivos en Inputs" y el botón
    inputs_canvas = tk.Canvas(root, height=100, bg="#2A2F4F")
    inputs_canvas.pack(fill=tk.X)

    # Texto "No se encontraron archivos en Inputs"
    inputs_canvas.create_text(
        425, 50,
        text="No se encontraron archivos de terremotos en la carpeta Inputs",
        fill="white",
        font=("Inter", 18)
    )

    # Botón para abrir la carpeta de inputs
    abrir_button = tk.Button(inputs_canvas, text="Abrir Carpeta Inputs", command=lambda: abrir_carpeta_inputs())
    abrir_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
    
    
    root.mainloop()

    