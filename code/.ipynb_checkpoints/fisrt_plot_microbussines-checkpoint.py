import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#loa
df = pd.read_csv("./querys/crecimientoNicolasRomero.csv")
names = df['Nombre_de_la_Unidad_Económica']
print(names)