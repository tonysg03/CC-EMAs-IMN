# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 11:54:23 2021

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
file_H = pd.read_csv("../Datos_T/Datos_Crudos/temp_Hora_69_abiertas.csv")

file_H_copia = file_H.copy()

#Se extraen los valores de las estaciones
num_est = list(file_H_copia["ESTACION"].unique())

#Se crea un diccionario con el formato de las horas
replace_hours = {2400: '0000', 100: '0100', 200: '0200',
                 300: '0300', 400: '0400', 500: '0500',
                 600: '0600', 700: '0700', 800: '0800',
                 900: '0900'}

#Se cambia el formato de las horas del archivo utilizando el diccionario creado
file_H_copia.HORA = file_H_copia.HORA.replace(replace_hours)

#Se cambian el tipo de formato de las columnas HORA y FECHA a string
file_H_copia = file_H_copia.astype({'HORA': 'str', 'FECHA': 'str'})

#Se crea una columna nueva llamada DATE donde se unen la FECHA y la HORA
file_H_copia["DATE"] = file_H_copia["FECHA"] + " " + file_H_copia["HORA"]

#Se cambia el formato de la columna DATE a formato fecha
file_H_copia.DATE = pd.to_datetime(file_H_copia["DATE"], format = "%d/%m/%Y %H%M")

#Se extraen los índices de las filas donde hay hora 00
index_out24 = file_H_copia.DATE.loc[file_H_copia.DATE.dt.hour.eq(0)].index

#En las filas donde hay hora 00 se suma un día
for i in index_out24:
    file_H_copia.DATE[i] = file_H_copia.DATE[i] + pd.Timedelta(days=1)
    
#Se crea un diccionario vacío para guardar los datos de cada estación
estaciones = {}

#Se crea un ciclo para agregar a cada key los valores de cada estación
for i in range(0, len(num_est)):
    print("Trabajando en la estación: 69%s" %num_est[i] + "\n")
    
    estaciones["69%s" %num_est[i]] = file_H_copia.loc[file_H_copia["ESTACION"] == num_est[i]]
    
    #Se completan las fechas faltantes
    r = pd.date_range(start = estaciones["69%s" %num_est[i]].DATE.min(), 
                      end = estaciones["69%s" %num_est[i]].DATE.max(), freq = "H")
    
    estaciones["69%s" %num_est[i]] = estaciones["69%s" %num_est[i]].set_index(["DATE"])
    
    estaciones["69%s" %num_est[i]].index = pd.DatetimeIndex(estaciones["69%s" %num_est[i]].index)
    
    estaciones["69%s" %num_est[i]] = estaciones["69%s" %num_est[i]].reindex(r, fill_value = np.nan)
    
    estaciones["69%s" %num_est[i]] = estaciones["69%s" %num_est[i]].set_index(
        estaciones["69%s" %num_est[i]].index).reindex(r).rename_axis("DATE").reset_index()
    
    out_file = pd.DataFrame(estaciones["69%s" %num_est[i]].values, columns = estaciones["69%s" %num_est[i]].columns)
    
    out_file.CUENCA = '69'
    
    out_file.ESTACION = str(num_est[i])
    
    out_file.to_csv('../Datos_T/T_69' + str(num_est[i]) + '.csv', sep=",", na_rep="NaN", index=False)
    
