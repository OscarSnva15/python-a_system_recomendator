import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
from requests import head
#origin point microbusiness
latitude1= 19.620550757350234
longitude1=-99.31328114851462

def distance(lat1, lat2, lon1, lon2):
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
    # calculate the result
    return(c * r)

#load cvs
df=pd.read_csv('../consultas/nicolasRomero.csv')
print(df.head())

print('---DISTANCES---')
for i in df.index:
    print(distance(latitude1, df['Latitud'][i], longitude1, df['Longitud'][i]), "K.M")
#coordenadas little cesar el charco
#19.621621977935146, -99.31497630458834