import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import dist, radians, cos, sin, asin, sqrt

#origin point microbusiness el charco
latitude1, longitude1 = [19.599472210151948, -99.30688849000485]


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
BBox = ((-99.3686, -99.2670, 19.58, 19.65))

#print( df.columns )

near_latitude = []
near_longitud = []

for i in df.index:
        if distance(latitude1, df['Latitud'][i], longitude1, df['Longitud'][i])<=0.250:
                print(df['Nombre_de_la_Unidad_Económica'][i])
                near_latitude.append(df['Latitud'][i])
                near_longitud.append(df['Longitud'][i])

print(" LEN : ",  len(near_latitude) )


fig, ax = plt.subplots(figsize = (22,12))

ax.scatter(near_longitud, near_latitude, zorder=1, alpha= 0.4, c='r', s=10)
ax.set_title('Plotting Spatial Data on Map')
ax.set_xlim(BBox[0],BBox[1])
ax.set_ylim(BBox[2],BBox[3])
ax.imshow(mymap, zorder=0, extent = BBox, aspect = 'equal')
plt.show()

# df_cut_1 = df[ df['Fecha de incorporación al DENUE'] < '2014-12' ]
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