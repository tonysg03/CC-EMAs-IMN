# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 11:54:23 2021

@author: Anthony Segura García

e-mail: asegura@ucr.ac.cr

Instituto Meteorológico Nacional
Departamento de Red Meteorológica y Procesamiento de Datos
"""

import pandas as pd

file = pd.read_excel("../HG/69579_Prueba_2.xlsx")

def redondeo(variable, decimales):
    '''
    Redondea los datos según la cantidad de decimales que se determinen.

    Parameters
    ----------
    variable : string
        Nombre de la variable que se encuentra en el archivo de la estación.
    decimales : integer
        Número entero de decimales que se determinen por variable.

    Returns
    -------
    pandas.core.series.Series
        Columna de la serie de datos de la variable redondeada.

    '''
    
    return file[variable].round(decimales)

datos = redondeo("TEMP_C_Avg",0)
