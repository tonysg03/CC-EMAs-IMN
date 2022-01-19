# -*- coding: utf-8 -*-

"""
Created on Thu Jan 21 15:03:25 2021

@author: Anthony Segura García

e-mail: asegura@ucr.ac.cr

Instituto Meteorológico Nacional
Departamento de Red Meteorológica y Procesamiento de Datos
"""

import pandas as pd
import numpy as np
from itertools import groupby


file = pd.read_excel("../HG/69579_Prueba_2.xlsx")

dato = file["TEMP_C_Avg"]

def valores_repetidos(dato):
    '''
    Verifica si existen valores iguales repetidos consecutivamente a lo largo de la serie. Si hay más
    de 4 valores repetidos los cambia por NA, si no, los deja igual.

    Parameters
    ----------
    dato : pandas.core.series.Series
        Columna de la serie de datos de la variable.

    Returns
    -------
    list1 : list
        Lista con la serie de datos sin valores repetidos.

    '''

    Contador = [(k, sum(1 for i in g)) for k,g in groupby(dato)]
    
    list1 = []
    for i,j in Contador:
        if j > 3:
            list1.extend([np.nan]*j)
        else:
            list1.extend([i]*j)
            
    return list1

datos = valores_repetidos(dato)