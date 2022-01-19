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


file = pd.read_excel("../HG/69579_Prueba_2.xlsx")

# Completo las fechas leyendo cada hora
r = pd.date_range(start=file.fecha.min(), end=file.fecha.max(), freq='H')

#Realizo un cambio del índice del dataframe, siendo la fecha ahora el índice
file = file.set_index(["fecha"])

#Realizo un cambio de formato del índice a formato fecha
file.index = pd.DatetimeIndex(file.index)

#Reorganizo las fechas y relleno los datos de las fechas faltantes con NaN
file = file.reindex(r, fill_value=np.nan)

#Reintegro el índice y la columna fecha
file = file.set_index(file.index).reindex(r).rename_axis('fecha').reset_index()

#Extraigo los datos y la fecha
dato = file["TEMP_C_Avg"]
date = file["fecha"]

#Cambio el formato de la fecha
file["fecha"] = pd.to_datetime(file["fecha"], format="%Y/%m/%d %H:%M:%S").dt.strftime('%d/%m/%Y,%H')