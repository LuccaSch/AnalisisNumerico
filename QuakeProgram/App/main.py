import pathlib
import numpy as np
import os

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

def calcular_distancia_fourier(terremoto1, terremoto2):
    # Calcula la diferencia entre los espectros de frecuencia
    diferencia_espectros = np.abs(terremoto1 - terremoto2)
    # Calcula la distancia euclidiana entre los espectros de frecuencia
    distancia = np.linalg.norm(diferencia_espectros)
    return distancia

def directorio_vacio(ruta):
    # Obtener la lista de archivos y directorios en la ruta especificada
    contenido = os.listdir(ruta)
    
    # Verificar si la lista está vacía
    if len(contenido) == 0:
        return True
    else:
        return False

def obtener_archivos_en_directorio(ruta):
    # Obtener la lista de archivos y directorios en la ruta especificada
    contenido = os.listdir(ruta)
    
    # Retornar solo los archivos (excluir directorios)
    archivos = [archivo for archivo in contenido if os.path.isfile(os.path.join(ruta, archivo))]
    
    return archivos

def guardar_arreglo_en_txt(arreglo, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        for elemento in arreglo:
            archivo.write(str(elemento) + '\n')

ruta = pathlib.Path('.')

ruta = ruta / "QuakeProgram"

imp= ruta / "Imputs"

if(directorio_vacio(imp)):
    print("Debe cargar Imputs para analisar")
else: 
    archivo=obtener_archivos_en_directorio(imp)
    funciones_de_t= []
    frecuencias=[]
    coeficientes_de_fourier=[]
    transformadas_de_fouerier=[]
    
    for indice in archivo:
        print(indice)
        direc = ruta / "Imputs" / indice
        archivo_output=ruta / "Outputs" / indice
        
        #1
        funcion_t= np.loadtxt(direc)
        t= funcion_t[:, 0]
        ft=funcion_t[:, 1]
        coeficiente_fourier = np.fft.fft(ft)/len(t) #Sacamos los coeficientes de la serie de fourier para cada pto, lo dividimos por el ancho de la entrada que seria el 1/N que esplicaron en clase
        trafo_fourier= abs(coeficiente_fourier)
        frecuencia = np.fft.fftfreq(len(t),t[0]-t[1])
    
        guardar_arreglo_en_txt(coeficiente_fourier,archivo_output)
        
        mostrarGrafica(t,ft,indice,trafo_fourier,frecuencia) #mostramos la grafica de la trasformada