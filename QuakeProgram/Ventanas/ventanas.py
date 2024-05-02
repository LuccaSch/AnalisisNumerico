import numpy as np

def ventana_gaussiana():
    #Podemos variar el valor de suavizado para suavizar mas o menos la funcion
    suavizado=3
    ventana = np.exp(-0.5 * (np.arange(-30,31)/suavizado)**2)
    return ventana 