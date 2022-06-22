import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from scipy import stats
from mpl_toolkits.basemap import Basemap
from math import dist, radians, cos, sin, asin, sqrt

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

def pĺot_density_business(df,BBox):
    #Iterate data frame on rows
    delta=0.0025
    location = {}
    num_lat=int((99.32098 - 99.31293)//0.00025)
    num_long=int((19.62356 - 19.62817)//0.00025)
    for long in range(0,num_long):
        for lat in range(0,num_lat):
            for _, row in df.iterrows():
                if row['Latitud'] - lat*0.00025-99.2670< delta and row['Longitud']+long*0.00025+19.58<delta:
                    location[(lat,long)]=location.get((lat,long),0)+1 
                    print('processing:')
    print(len(location))

def plot_scatter_bussines_by_code(df, BBox, mymap, diccionary):
    color=iter(cm.rainbow(np.linspace(0,1,20)))
    c=next(color)
    for code in diccionary:
        # Filter data by CODE
        df_filter_class = df[ df['Código_de_la_clase_de_actividad_SCIAN'] ==  code]
        df_filter_class_snaptime = []
        # Filter data by DATE
        df_filter_class_snaptime.append( df_filter_class[ df_filter_class['Fecha_de_incorporacion_al_DENUE'] < '2014-12' ] )
        df_filter_class_snaptime.append( df_filter_class[ (df['Fecha_de_incorporacion_al_DENUE'] >= '2014-12')  & \
                                                            (df['Fecha_de_incorporacion_al_DENUE'] < '2019-11') ] )
        df_filter_class_snaptime.append( df_filter_class[ df_filter_class['Fecha_de_incorporacion_al_DENUE']>= '2019-11' ] )

        # color = [ 'r', 'g', 'b' ]
        title = ["Fecha Nacimiento < 2014-12", "Fecha Nacimiento < 2019-11","Fecha Nacimiento< 2022-05" ]
        fig, ax = plt.subplots(nrows = 1, ncols= 3, figsize = (26,10))

        for i in range(3):
            ax[i].set_title(title[i])
            ax[i].set_xlim(BBox[0],BBox[1])
            ax[i].set_ylim(BBox[2],BBox[3])
            ax[i].imshow(mymap, zorder=0, extent = BBox, aspect = 'equal')
            for j in range(i+1):
                ax[i].scatter(df_filter_class_snaptime[j]['Longitud'], df_filter_class_snaptime[j]['Latitud'], zorder=1, alpha= 0.71, c=c, s=10)

            plt.savefig('../images_insights/test/'+'class_2_' + str(code)+'.png')

def main():
    #open my file data
    df = pd.read_csv("../querys/crecimientoNicolasRomero.csv")
    BBox = ((-99.3686, -99.2670, 19.58, 19.65))
    mymap = plt.imread("../media/map_CDNR.png")
    pĺot_density_business(df,BBox)
    #plot_scatter_bussines_by_code(df, BBox, mymap, diccionary)
if __name__ == "__main__":
    main()