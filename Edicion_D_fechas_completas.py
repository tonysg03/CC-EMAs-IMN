# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 18:31:05 2021

@author: Anthony Segura García

e-mail: asegura@ucr.ac.cr

Instituto Meteorológico Nacional
Departamento de Red Meteorológica y Procesamiento de Datos
"""

#Se carga la librería pandas
import pandas as pd
import numpy as np

#Se deshabilita la alerta por copia de datos
pd.options.mode.chained_assignment = None

#Se cargan los datos de temperatura
file_D = pd.read_csv("../Datos_T/Datos_Crudos/temp_max_min_69_abiertas.csv")

file_D_copia = file_D.copy()

#Se extraen los valores de las estaciones
num_est = list(file_D_copia["ESTACION"].unique())

#Se cambia el formato de la columna DATE a formato fecha
file_D_copia["FECHA"] = pd.to_datetime(file_D_copia["FECHA"], format = "%d/%m/%Y")

#Se crea un diccionario vacío para guardar los datos de cada estación
estaciones = {}

#Se crea un ciclo para agregar a cada key los valores de cada estación
for i in range(0, len(num_est)):
    print("Trabajando en la estación: 69%s" %num_est[i] + "\n")
    
    estaciones["69%s" %num_est[i]] = file_D_copia.loc[file_D_copia["ESTACION"] == num_est[i]]
    
    #Se completan las fechas faltantes
    r = pd.date_range(start = estaciones["69%s" %num_est[i]].FECHA.min(), 
                      end = estaciones["69%s" %num_est[i]].FECHA.max(), freq = "D")
    
    estaciones["69%s" %num_est[i]] = estaciones["69%s" %num_est[i]].set_index(["FECHA"])
    
    estaciones["69%s" %num_est[i]].index = pd.DatetimeIndex(estaciones["69%s" %num_est[i]].index)
    
    estaciones["69%s" %num_est[i]] = estaciones["69%s" %num_est[i]].reindex(r, fill_value = np.nan)
    
    estaciones["69%s" %num_est[i]] = estaciones["69%s" %num_est[i]].set_index(
        estaciones["69%s" %num_est[i]].index).reindex(r).rename_axis("FECHA").reset_index()
    
    out_file = pd.DataFrame(estaciones["69%s" %num_est[i]].values, columns = estaciones["69%s" %num_est[i]].columns)
    
    out_file.CUENCA = '69'
    
    out_file.ESTACION = str(num_est[i])
    
    out_file.to_csv('../Datos_T/D_T_69' + str(num_est[i]) + '.csv', sep=",", na_rep="NaN", index=False)
    
