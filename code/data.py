import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# Python 3 program to calculate Distance Between Two Points on Earth
from math import radians, cos, sin, asin, sqrt
from requests import head
#origin_cordenate
cx= 53.32055555555556
cy=-1.7297222222222221

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

# load cvs
df=pd.read_csv('../DENUE/test.csv')

# print(pd.unique(df['Latitud']))
# print(pd.unique(df['Longitud']))
print('------')
for longitud in df['Longitud']:
    for latitud in df['Latitud']:
        print(distance(latitud, cy, longitud, cx), "K.M")