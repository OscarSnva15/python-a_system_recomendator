import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("./DENUE/test.csv")

print(df.head())

BBox = ((df.Longitud.min(),   df.Longitud.max(),      
        df.Latitud.min(), df.Latitud.max()) )

print( BBox )


mymap = plt.imread("./map.png")
fig, ax = plt.subplots(figsize = (8,7))
ax.scatter(df.Longitud, df.Latitud, zorder=1, alpha= 0.2, c='b', s=10)
ax.set_title('Plotting Spatial Data on Map')
ax.set_xlim(BBox[0],BBox[1])
ax.set_ylim(BBox[2],BBox[3])
ax.imshow(mymap, zorder=0, extent = BBox, aspect= 'equal')
plt.show()