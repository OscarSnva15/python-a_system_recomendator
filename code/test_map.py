import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../consultas/nicolasRomero.csv")

print(df.head())

# BBocx = ((df.Longitud.min(),   df.Longitud.max(),      
#         df.Latitud.min(), df.Latitud.max()) )

BBox = ((-99.3080, -99.3260,      
        19.6311, 19.6458))

print( BBox )
mymap = plt.imread("../media/colonia_franciscoMadero.png")
fig, ax = plt.subplots(figsize = (8,7))
ax.scatter(df.Longitud, df.Latitud, zorder=1, alpha= 0.2, c='b', s=10)
ax.set_title('Plotting Spatial Data on Map')
ax.set_xlim(BBox[0],BBox[1])
ax.set_ylim(BBox[2],BBox[3])
ax.imshow(mymap, zorder=0, extent = BBox, aspect = 'equal')
plt.show()