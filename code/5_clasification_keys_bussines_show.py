from turtle import width
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import dist, radians, cos, sin, asin, sqrt
import os

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


def plot_scatter_bussines_partition( df, BBox, mymap, code = 311812 ):
  df_filter_class = df[ df['Código_de_la_clase_de_actividad_SCIAN'] ==  code]

  df_filter_class_snaptime = []
  df_filter_class_snaptime.append( df_filter_class[ df_filter_class['Fecha_de_incorporacion_al_DENUE'] < '2014-12' ] )
  df_filter_class_snaptime.append( df_filter_class[ (df['Fecha_de_incorporacion_al_DENUE'] >= '2014-12')  & \
                                                (df['Fecha_de_incorporacion_al_DENUE'] < '2019-11') ] )
  df_filter_class_snaptime.append( df_filter_class[ df_filter_class['Fecha_de_incorporacion_al_DENUE'] >= '2019-11' ] )

  color = [ 'r', 'g', 'b' ]
  title = ["Fecha Incorporación DENUE 2010-07 -- < 2014-12", 
            "Fecha Incorporación DENUE  2014-12 --- < 2019-11",
            "Fecha Incorporación DENUE  2019-11 --- 2022-05" ]

  fig, ax = plt.subplots(nrows = 1, ncols= 3, figsize = (26,10))
  for i in range(3):
    ax[i].set_title(title[i])
    ax[i].set_xlim(BBox[0],BBox[1])
    ax[i].set_ylim(BBox[2],BBox[3])
    ax[i].imshow(mymap, zorder=0, extent = BBox, aspect = 'equal')
    ax[i].scatter(df_filter_class_snaptime[i]['Longitud'], df_filter_class_snaptime[i]['Latitud'], zorder=1, alpha= 0.71, c=color[i], s=10)


def plot_scatter_bussines_acumulated( df, BBox, mymap, code = 311812 ):
  df_filter_class = df[ df['Código_de_la_clase_de_actividad_SCIAN'] ==  code]

  df_filter_class_snaptime = []
  df_filter_class_snaptime.append( df_filter_class[ df_filter_class['Fecha_de_incorporacion_al_DENUE'] < '2014-12' ] )
  df_filter_class_snaptime.append( df_filter_class[ (df['Fecha_de_incorporacion_al_DENUE'] >= '2014-12')  & \
                                                    (df['Fecha_de_incorporacion_al_DENUE'] < '2019-11') ] )
  df_filter_class_snaptime.append( df_filter_class[ df_filter_class['Fecha_de_incorporacion_al_DENUE'] >= '2019-11' ] )

  color = [ 'r', 'g', 'b' ]
  title = ["Fecha Incorporación DENUE < 2014-12", 
            "Fecha Incorporación DENUE < 2019-11",
            "Fecha Incorporación DENUE < 2022-05" ]

  fig, ax = plt.subplots(nrows = 1, ncols= 3, figsize = (26,10))
  for i in range(3):
    ax[i].set_title(title[i])
    ax[i].set_xlim(BBox[0],BBox[1])
    ax[i].set_ylim(BBox[2],BBox[3])
    ax[i].imshow(mymap, zorder=0, extent = BBox, aspect = 'equal')
    for j in range(i+1):
      ax[i].scatter(df_filter_class_snaptime[j]['Longitud'], df_filter_class_snaptime[j]['Latitud'], zorder=1, alpha= 0.71, c=color[j], s=10)
  
  plt.savefig('./images_insights/'+str(code)+'.png')


def main():
  df = pd.read_csv("./querys/crecimientoNicolasRomero.csv")
  mymap = plt.imread("./media/map_CDNR.png")
  BBox = ((-99.3686, -99.2670, 19.58, 19.65))
  code_business = []
  plot_scatter_bussines_acumulated(df, BBox, mymap, 461110)
  plt.show()


if __name__ == "__main__":
  main()