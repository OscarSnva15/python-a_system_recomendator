import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import array
import dataframe_image as dfi

#1 load data fror file csv
df = pd.read_csv("./querys/crecimientoNicolasRomero.csv")

dataCodes = df['ID']
arrayCodes  = []
for Code in dataCodes:
    arrayCodes.append(Code)

dataNames = df['Nombre_de_la_Unidad_Económica']
arrayBussines = []
for type in dataNames:
    arrayBussines.append(type)

dataCollect = {
    'Code': arrayCodes,
    'nameBussines': arrayBussines
}

from IPython.display import display
num_of_rows_to_show = 1
with pd.option_context('display.max_rows', num_of_rows_to_show):
    display(dataCollect)
    
df = pd.DataFrame(dataCollect)
dfi.export(df.head(n=10), 'dataframeCollect.png')