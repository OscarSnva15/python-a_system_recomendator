import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../consultas/crecimientoNicolasRomero.csv")

# print(df.head())

# BBox = ((df.Longitud.min(),   df.Longitud.max(),      
#         df.Latitud.min(), df.Latitud.max()) )

#BBox = ((-99.3080, -99.3260, 19.6311, 19.6458))
# BBox = ((-99.3243, -99.3091, 19.6303, 19.6206))

# print( BBox )
mymap = plt.imread("../media/map_CDNR.png")
BBox = ((-99.3686, -99.2670, 19.58, 19.65))

print( df.columns )


# df_cut_1 = df[ df['Fecha de incorporación al DENUE'] < '2014-12' ]
# df_cut_2 = df[  (df['Fecha de incorporación al DENUE'] >= '2014-12') &  (df['Fecha de incorporación al DENUE'] < '2019-11') ]
# df_cut_3 = df[ '2019-11' <= df['Fecha de incorporación al DENUE']   ]

df_cut_1 = df[ df['Fecha de incorporación al DENUE'] < '2014-12' ]
df_cut_2 = df[ df['Fecha de incorporación al DENUE'] < '2019-11' ]
df_cut_3 = df

print( len(df_cut_1) )
print( len(df_cut_2) )
print( len(df_cut_3) )


fig, ax = plt.subplots(figsize = (22,12))
# ax.scatter(df_cut_1.Longitud, df_cut_1.Latitud, zorder=1, alpha= 0.4, c='gray', s=10)
# ax.scatter(df_cut_2.Longitud, df_cut_2.Latitud, zorder=1, alpha= 0.4, c='gray', s=10)
ax.scatter(df_cut_3.Longitud, df_cut_3.Latitud, zorder=1, alpha= 0.4, c='gray', s=10)

ax.set_title('Plotting Spatial Data on Map')
ax.set_xlim(BBox[0],BBox[1])
ax.set_ylim(BBox[2],BBox[3])
ax.imshow(mymap, zorder=0, extent = BBox, aspect = 'equal')
plt.show()