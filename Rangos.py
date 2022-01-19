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
import glob
from os.path import splitext
import fnmatch


#Lee todos los archivos de Rangos máximos y mínimos
filenames = glob.glob('../HG/Rangos/*.xlsx')

#Lee todos los archivos de las estaciones
file = glob.glob("../HG/*.xlsx")

#Crea listas vacías para luego igualar los números de estaciones
text = []
var_est = []

def rangos(filenames, file):
    '''
    Verifica si los datos de una variable para cada mes se encuentra fuera de los rangos climatológicos
    de la estación

    Parameters
    ----------
    filenames : List
        Lista de los archivos que se encuentran en el directorio de las estaciones.
    file : List
        Lista de los archivos que se encuentran en el directorio de rangos.

    Returns
    -------
    dataframes2 : dataframe
        Dataframe con columnas agregadas con los cambios realizados según los rangos por meses.

    '''

    for i in range(len(filenames)):

        text = splitext(filenames[i])[0].split('-')
        text = splitext(text[0])[0].split('\\')[1]

        var_est = splitext(file[i])[0].split('_')[0]
        var_est = splitext(var_est)[0].split('\\')[1]
 
        if text == var_est:
            print("Trabajando en estación: " + var_est + "\n")
            
            dataframes = pd.read_excel(fnmatch.filter(filenames,"*"+var_est+"*")[0])
            
            dataframes2 = pd.read_excel(fnmatch.filter(file,"*"+var_est+"*")[0])
            
            var_vars = dataframes.Variable

            dataframes2["fecha"] = pd.to_datetime(dataframes2["fecha"])

            meses = np.sort(list(set(["%.2d" % i for i in dataframes2["fecha"].dt.month])))
    
            dataframes.set_index("Variable", inplace=True)
 
            limits_max = {}
            limits_min = {}
            
            for p in var_vars:
                
                if p in dataframes2.columns.values:
                    
                    for j in range(len(meses)):

                        limits_max[int(meses[j])] = dataframes.loc[p]["X"+meses[j]+".max"]
                        limits_min[int(meses[j])] = dataframes.loc[p]["X"+meses[j]+".min"]

                        dataframes2 = dataframes2.assign(**{f"Prueba {p}":np.select(
                                [dataframes2.fecha.dt.month.eq(m) & dataframes2[p].gt(l) for m,l in limits_max.items()], 
                                [np.nan for m in limits_max.keys()], dataframes2[p])}) 

                        dataframes2 = dataframes2.assign(**{f"Prueba {p}":np.select(
                                [dataframes2.fecha.dt.month.eq(k) & dataframes2["Prueba " + p].lt(g) for k,g in limits_min.items()], 
                                [np.nan for k in limits_min.keys()], dataframes2["Prueba " + p])})
        else:
            print("Estaciones no son iguales")

        var_est = []
        text= []
        
    return dataframes2

data = rangos(filenames, file)
