import pathlib
import numpy as np
import os

from numpy import array
from matplotlib import pyplot as plt
  
def mostrarGrafica(t,ft,nombre,trafo_fourier,frecuencia,señal_suavizada,trafo_suavizada):
 plt.figure()
 plt.title(nombre)
 plt.grid()
 plt.plot(t,ft)
 plt.xlabel("tiempo [s]")
 plt.ylabel("Amplitud [m/s^2]")
 plt.figure() # Crear una nueva figura
 plt.plot(frecuencia,trafo_fourier) # Graficar los valores absolutos de los coeficientes de Fourier
 plt.grid()
 plt.title("Transformada de Fourier para "+nombre)
 plt.xlabel("Frecuencia [Hz]")
 plt.ylabel("Amplitud [m/s^2]")
 plt.xlim(0, max(frecuencia))
 plt.figure()
 plt.title(nombre + " suavizada")
 plt.grid()
 plt.plot(t,señal_suavizada)
 plt.xlabel("tiempo [s]")
 plt.ylabel("Amplitud [m/s^2]")
 plt.figure()
 plt.title("Transformada de Fourier para "+nombre+ "suavizada")
 plt.grid()
 plt.plot(frecuencia,trafo_suavizada)
 plt.xlabel("Frecuencia [Hz]")
 plt.ylabel("Amplitud [m/s^2]")
 plt.xlim(0, max(frecuencia))
 plt.show()
 return    

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
    
    trasformadas = []
    
    for indice in archivo:
        direc = ruta / "Imputs" / indice
        archivo_output=ruta / "Outputs" / indice
        
        #a
        funcion_t= np.loadtxt(direc) #Trae el txt y lo almacena en un array de np donde funcion_t[0] son los t[] y funcion_t[1] son los ft[]
        t= funcion_t[:, 0] #Los llevamos a variables para que sea mas facil de manejar 
        ft=funcion_t[:, 1]
        coeficiente_fourier = np.fft.fft(ft)/len(t) #Sacamos los coeficientes de la serie de fourier para cada pto, lo dividimos por el ancho de la entrada que seria el 1/N de la teoria
        trafo_fourier= abs(coeficiente_fourier) #Utilizamos el valor absoluto para calcular la trasformada de fourier
        frecuencia = (np.fft.fftfreq(len(t),t[0]-t[1])/2*np.pi) #Calculamos la unidades de frecuencia angular por muestra y lo dividimos por 2pi para llevarlo a Hz
        guardar_arreglo_en_txt(coeficiente_fourier,archivo_output) #Usamos esta funcion para crear los txt donde se guardaran los coeficientes de fourier dentro de Outputs
        
        trasformadas.append(ft) #Creamos una lista de los ft que sera usada para el ejer E
        
        #b
        h = np.ones(100) / 100 #Creamos una funcion loma de burro de 100 de largo y la llamamos h
        señal_suavizada = np.convolve(ft, h, mode='same') #convolucionamos la loma h con nuestra funcion, la longitud quedara como len(t) ya que usamos el mode ´same´ para facilitarnos mas adelante
        trafo_suavizada = np.abs(np.fft.fft(señal_suavizada)/len(t)) #hacemos la trasformada de fourier de la funcion suavizada
        
        
        mostrarGrafica(t,ft,indice,trafo_fourier,frecuencia,señal_suavizada,trafo_suavizada) #mostramos la grafica en funcion de t, su trasformada y sus respectivas suavizadas
        
        #c
        
        indice_max = np.argmax(trafo_fourier) #Buscamos dentro de trafo_fourier el valor maximo
        frecuencia_max = abs(frecuencia[indice_max]) #La frecuencia maxima estara en frecuencia[valor_maximo]
        print(f"La frecuencia de mayor aceleración es {frecuencia_max}") #Mostramos el valor por pantalla
        with open((ruta / "Outputs" / "Respuestas"), 'a') as archivo: #Lo guardamos en  el archivo Respuestas dentro de Outputs
            mensaje= f"En {indice} la frecuencia mas acelerada es {frecuencia_max}.\n"
            archivo.write(mensaje)
            
    #e
    
    with open((ruta / "Outputs" / "Respuestas"), 'a') as archivo:
            mensaje= f"E.\n"
            archivo.write(mensaje)
            
    correlacion13= np.correlate(trasformadas[0],trasformadas[2],mode="valid") #Utilizamos correlate de las ft guardadas anteriormente en trasformadas, este calcula la diferencia entre las trasformadas y devuelve un valor
    correlacion23= np.correlate(trasformadas[1],trasformadas[2],mode="valid") #Calculamos este valor para ambas ya que sera la diferencia entre los spectros de frecuencia de terremoto1-2 y terremoto3
    with open((ruta / "Outputs" / "Respuestas"), 'a') as archivo:
        if (np.sum(correlacion13)> np.sum(correlacion23)): #si correlacion13 es mayor la diferencia de espectros es menor y por ende las graficas 1 y 3 son mas similares que 2 y 3
            mensaje= f"El sismografo terremoto 3 esta mas cerca de terremoto 1.\n" #guardamos dentro de respuesta 
            archivo.write(mensaje)
        else:
            mensaje= f"El sismografo terremoto 3 esta mas cerca de terremoto 2.\n" #si correlacion13 es mayor la diferencia de espectros es menor y por ende las graficas 2 y 3 son mas similares que 1 y 3
            archivo.write(mensaje)