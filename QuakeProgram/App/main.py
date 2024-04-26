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

def ventana_gausiana(suavizado):
    #Podemos variar el valor de suavizado para suavizar mas o menos la funcion
    ventana = np.exp(-0.5 * (np.arange(-30,31)/suavizado)**2)
    return ventana    

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

def submuestreo_terremotos(terremoto1, terremoto2):
    # Cantidad de puntos que deseas para el terremoto2 (igual a la cantidad de puntos del terremoto1)
    n_points_terremoto1 = len(terremoto1)

    # Índices equidistantes para el terremoto2
    indices_terremoto2 = np.linspace(0, len(terremoto2) - 1, n_points_terremoto1, dtype=int)

    # Submuestreo del terremoto2 utilizando los índices generados
    terremoto2_submuestreado = terremoto2[indices_terremoto2]
    return terremoto2_submuestreado

ruta = pathlib.Path('.')

ruta = ruta / "QuakeProgram"

imp= ruta / "Imputs"

if(directorio_vacio(imp)):
    print("Debe cargar Imputs para analisar")
else: 
    archivo=obtener_archivos_en_directorio(imp)
        
    terremotos = []
    trasformadas = []
    frecuencias = []
    
    for indice in archivo:
        direc = ruta / "Imputs" / indice
        archivo_output=ruta / "Outputs" / indice
        
        #a
        funcion_t= np.loadtxt(direc) #Trae el txt y lo almacena en un array de np donde funcion_t[0] son los t[] y funcion_t[1] son los ft[]
        t= funcion_t[:, 0] #Los llevamos a variables para que sea mas facil de manejar 
        ft=funcion_t[:, 1]
        coeficiente_fourier = (np.fft.fft(ft)/len(t))*2 #Sacamos los coeficientes de la serie de fourier para cada pto, lo dividimos por el ancho de la entrada que seria el 1/N de la teoria
        trafo_fourier= abs(coeficiente_fourier) #Utilizamos el valor absoluto para calcular la trasformada de fourier
        frecuencia = np.fft.fftfreq(len(t),t[0]-t[1]) #Calculamos la unidades de frecuencia angular por muestra y lo dividimos por 2pi para llevarlo a Hz
        guardar_arreglo_en_txt(coeficiente_fourier,archivo_output) #Usamos esta funcion para crear los txt donde se guardaran los coeficientes de fourier dentro de Outputs
        
        terremotos.append(ft) #Creamos una lista de los ft que sera usada para el ejer E
        trasformadas.append(trafo_fourier)
        frecuencias.append(frecuencia)
        
        #b
        h = ventana_gausiana(3) #elegimos un suavizado de 3 pero podriamos suvirlo para suavizar mas la funcion
        señal_suavizada = np.convolve(ft, h, mode='same') #convolucionamos la loma h con nuestra funcion, la longitud quedara como len(t) ya que usamos el mode ´same´ para facilitarnos mas adelante
        trafo_suavizada = np.abs(np.fft.fft(señal_suavizada)/len(t)) #hacemos la trasformada de fourier de la funcion suavizada
        
        
        mostrarGrafica(t,ft,indice,trafo_fourier,frecuencia,señal_suavizada,trafo_suavizada) #mostramos la grafica en funcion de t, su trasformada y sus respectivas suavizadas
        
        #c
        
        indice_max = np.argmax(trafo_fourier) #Buscamos dentro de trafo_fourier el valor maximo
        frecuencia_max = abs(frecuencia[indice_max]) #La frecuencia maxima estara en frecuencia[valor_maximo]
        print(f"La frecuencia de mayor aceleración es {frecuencia_max}") #Mostramos el valor por pantalla
        with open((ruta / "Outputs" / "Respuestas"), 'a') as archivo: #Lo guardamos en  el archivo Respuestas dentro de Outputs
            mensaje= f"En {indice} la frecuencia mas acelerada es {frecuencia_max}.\n"
            print(mensaje)
            archivo.write(mensaje)
    
    #d
    #Para poder comprar los terremotos nesesitamos que la cantidad de datos muestreados sea la misma, para ello debemos realizar un submuestreo del terremoto2 para que tenga 4000 muestras
    
    terremoto2_submuestrado=submuestreo_terremotos(terremotos[0],terremotos[1])
    terremoto2_submuestrado_trasf= np.abs((np.fft.fft(terremoto2_submuestrado)/4000)*2)
    
    suma_trafo = terremoto2_submuestrado_trasf + trasformadas[0]   #Hacemos suma de los vectores de la transformada 
    prod_trafo = terremoto2_submuestrado_trasf*trasformadas[0]     #Hacemos producto de los vectores de la transforma 

    is_max = np.argmax(suma_trafo)
    fsum_max = abs(frecuencias[0][is_max])               #Frecuencia mas alta de la sumatoria 
 
    ip_max = np.argmax(prod_trafo)
    fprod_max = abs(frecuencias[0][ip_max])              #Frecuencia mas alta de los productos 

    with open((ruta / "Outputs" / "Respuestas"), 'a') as archivo: #Lo guardamos en  el archivo Respuestas dentro de Outputs
            mensaje= f"La frecuencia mas afectada a travez de hacer la sumatoria es {fsum_max}.\n La frecuencia mas afectada a travez de hacer el producto es {fprod_max}\n"
            print(mensaje)
            archivo.write(mensaje)
    
        
    #e       
    correlacion13= np.correlate(trasformadas[0],trasformadas[2],mode="valid") #Utilizamos correlate de las ft guardadas anteriormente en trasformadas, este calcula la diferencia entre las trasformadas y devuelve un valor
    correlacion23= np.correlate(terremoto2_submuestrado_trasf,trasformadas[2],mode="valid") #Calculamos este valor para ambas ya que sera la diferencia entre los spectros de frecuencia de terremoto1-2 y terremoto3
   
    with open((ruta / "Outputs" / "Respuestas"), 'a') as archivo:
        if (np.max(correlacion13)> np.max(correlacion23)): #si correlacion13 es mayor la diferencia de espectros es menor y por ende las graficas 1 y 3 son mas similares que 2 y 3
            mensaje= f"El sismografo terremoto 3 esta mas cerca de terremoto 1.\n" #guardamos dentro de respuesta 
            print(mensaje)
            archivo.write(mensaje)
        elif (np.max(correlacion13)< np.max(correlacion23)):
            mensaje= f"El sismografo terremoto 3 esta mas cerca de terremoto 2.\n" #si correlacion13 es mayor la diferencia de espectros es menor y por ende las graficas 2 y 3 son mas similares que 1 y 3
            print(mensaje)
            archivo.write(mensaje)
        else:
            mensaje= f"El sismografo terremoto 3 esta a la misma distancia de terremoto 1 y terremoto 2.\n" #si correlacion13 es mayor la diferencia de espectros es menor y por ende las graficas 2 y 3 son mas similares que 1 y 3
            print(mensaje)
            archivo.write(mensaje)