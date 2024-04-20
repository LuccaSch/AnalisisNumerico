import pathlib
import numpy as np

from numpy import array
from matplotlib import pyplot as plt
  
def mostrarGrafica(t,ft,nombre,trafo_fourier,frecuencia):
 plt.figure()
 plt.title(nombre)
 plt.grid()
 plt.plot(t,ft)
 plt.xlabel("tiempo")
 plt.ylabel("Amplitud")
 plt.figure() # Crear una nueva figura
 plt.plot(frecuencia,trafo_fourier) # Graficar los valores absolutos de los coeficientes de Fourier
 plt.grid()
 plt.title("Transformada de Fourier para "+nombre)
 plt.xlabel("Frecuencia")
 plt.ylabel("Amplitud")
 plt.show()
 return

def guardar_arreglo_en_txt(arreglo, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        for elemento in arreglo:
            archivo.write(str(elemento) + '\n')

ruta = pathlib.Path('.')

ruta = ruta / "QuakeProgram"

print('Buscar el archivo que desea leer')

respuesta = input('Ingrese el nombre del archivo [exit para salir]: ')
nombre = respuesta

archivo = ruta / "Imputs" / respuesta

while respuesta!="exit":
    if archivo.exists():
        #Ejer 1
        datos = np.loadtxt(archivo) #Descomprimimos el txt en una lista donde el primer elemento es el t y el segundo elemento el Ft, guarados en arreglos .np
        t= datos[:, 0]
        ft=datos[:, 1]
        coeficiente_fourier = np.fft.fft(ft)/len(t) #Sacamos los coeficientes de la serie de fourier para cada pto, lo dividimos por el ancho de la entrada que seria el 1/N que esplicaron en clase
        trafo_fourier= abs(coeficiente_fourier) 
        
        frecuencia = np.fft.fftfreq(len(t),t[0]-t[1])
        
        archivo_output= ruta / "Outputs" / "coeficientes1.txt" #generamos una ruta a Outputs
        guardar_arreglo_en_txt(coeficiente_fourier,archivo_output)#guardamos todos los coeficientes de fourier en outputs
        
        mostrarGrafica(t,ft,nombre,trafo_fourier,frecuencia) #mostramos la grafica de la trasformada
        #Ejer 2
        
        
        respuesta = "exit" #salimos del while
    else:
        #Caso de ingresar mal el archivo
        print('No existe el archivo seleccionado')
        
        respuesta = input('Ingrese el nombre del archivo [exit para salir]: ')
        
        archivo = ruta / "Imputs" / respuesta
        
        nombre = respuesta