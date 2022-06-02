from cgi import print_form
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import dist, radians, cos, sin, asin, sqrt
import csv

class Business:
    def __init__(self, name, type, clave, age):
        self.name = name
        self.type = type
        self.clave = clave
        self.age = age

#origin point
latitude1, longitude1 = [19.62054709688509, -99.31394730905744]
ratio=0.100
date='2014-12'

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

df = pd.read_csv("../consultas/crecimientoNicolasRomero.csv")

# print( BBox )
mymap = plt.imread("../media/map_CDNR.png")
BBox = ((-99.3097, -99.3186, 19.6410, 19.6462))

near_latitude = []
near_longitud = []
near_bussines = []


ancla = [461110,
465311,
812110,
467111,
311830,
461121,
463211,
461130,
464111,
461122,
811111,
311812,
611122,
461160,
722514,
621211,
813210,
561432,
611111,
463310,
611112,
468211,
722513,
722518,
722517]

# df_cut_1 = df[ df['Fecha_de_incorporacion_al_DENUE'] < '2014-12' ]
# df_cut_2 = df[  (df['Fecha_de_incorporacion_al_DENUE'] < '2019-11') ]
# df_cut_3 = df
# df_test = df

f = open("tickets_names_negocio.csv", "a")
# create the csv writer
writer = csv.writer(f)

for j in df.index:
    dict_counter = {}
    latitude1, longitude1 = df['Latitud'][j], df['Longitud'][j] 
    for i in df.index:
    # if df_test['Código_de_la_clase_de_actividad_SCIAN'][i] not in ancla:
    #     near_latitude.append(df_test['Latitud'][i])
    #     near_longitud.append(df_test['Longitud'][i])
        if (distance(latitude1, df['Latitud'][i], longitude1, df['Longitud'][i])<=ratio) and (df['Fecha_de_incorporacion_al_DENUE'][i]< date) :
            near_bussines.append(Business(df['Nombre_de_la_Unidad_Económica'][i],df['Nombre_de_clase_de_la_actividad'][i],df['Código_de_la_clase_de_actividad_SCIAN'][i],df['Fecha_de_incorporacion_al_DENUE'][i]))
            near_latitude.append(df['Latitud'][i])
            near_longitud.append(df['Longitud'][i])
            if df['Código_de_la_clase_de_actividad_SCIAN'][i] in dict_counter:
                dict_counter[ df['Código_de_la_clase_de_actividad_SCIAN'][i] ] +=1
            else:
                dict_counter[ df['Código_de_la_clase_de_actividad_SCIAN'][i] ] = 1


    if len(dict_counter)>1:
        writer.writerow(  list(dict_counter.keys()) )
        print(" site :", j)
    
print("BUSINES SET")
print("LEN : \n",  len(near_latitude))
# for j in range(len(near_latitude)):
#     print("-----------------------.")
#     print("Name: ", near_bussines[j].name)
#     print("Type: ", near_bussines[j].type)
#     print("Clave:", near_bussines[j].clave)
#     print("Age:  ", near_bussines[j].age)

# print(" total :", len(dict_counter))
# for key, value in dict_counter.items():
#     print( key, " : ", value )


# fig, ax = plt.subplots(figsize = (22,12))
# ax.scatter(near_longitud, near_latitude, zorder=1, alpha= 0.4, c='b', s=10)
# ax.set_title('Plotting Spatial Data on Map')
# ax.set_xlim(BBox[0],BBox[1])
# ax.set_ylim(BBox[2],BBox[3])
# ax.imshow(mymap, zorder=0, extent = BBox, aspect = 'equal')
# plt.show()

#df_cut_1 = df[ df['Fecha de incorporación al DENUE'] < '2014-12' ]
# df_cut_2 = df[  (df['Fecha de incorporación al DENUE'] >= '2014-12') &  (df['Fecha de incorporación al DENUE'] < '2019-11') ]
# df_cut_3 = df[ '2019-11' <= df['Fecha de incorporación al DENUE']   ]

# df_cut_1 = df[ df['Fecha de incorporación al DENUE'] < '2014-12' ]
# df_cut_2 = df[ df['Fecha de incorporación al DENUE'] < '2019-11' ]
# df_cut_3 = df

# print( len(df_cut_1) )
# print( len(df_cut_2) )
# print( len(df_cut_3) )


# fig, ax = plt.subplots(figsize = (22,12))
# # ax.scatter(df_cut_1.Longitud, df_cut_1.Latitud, zorder=1, alpha= 0.4, c='gray', s=10)
# # ax.scatter(df_cut_2.Longitud, df_cut_2.Latitud, zorder=1, alpha= 0.4, c='gray', s=10)
# ax.scatter(df_cut_3.Longitud, df_cut_3.Latitud, zorder=1, alpha= 0.4, c='gray', s=10)

# ax.set_title('Plotting Spatial Data on Map')
# ax.set_xlim(BBox[0],BBox[1])
# ax.set_ylim(BBox[2],BBox[3])
# ax.imshow(mymap, zorder=0, extent = BBox, aspect = 'equal')
# plt.show()