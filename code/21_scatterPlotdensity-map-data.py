from itertools import count
from typing import Counter
from wsgiref.handlers import IISCGIHandler
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import pandas as pd
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

def accumulated_geolocation_bussines(df,BBox):
    #Iterate data frame on rows
    delta=0.00025
    num_lat=int((BBox[1] - BBox[0])/delta)
    num_long=int((BBox[3] - BBox[2])/delta)
    
    location = {}
    l = df.count()[0]
    for i, row in df.iterrows():
        loc_latt = int( (row['Latitud'] - BBox[0]) / delta )
        loc_long = int( (row['Longitud'] - BBox[2]) / delta )
        location[ (loc_latt,loc_long) ] = location.get( (loc_latt,loc_long), 0 ) + 1 
        # print(i,"/",l)

    latituds = []
    longituds = []
    accumulated = []
    for key, value in location.items():
        if 4 < value < 160:
            latituds.append(key[0]*delta+BBox[0])
            longituds.append(key[1]*delta+BBox[2])
            accumulated.append(value)

    # latituds = [lat*delta+BBox[0] for (lat,_) in location ]
    # longituds = [long*delta+BBox[2] for (_,long) in location ]
    # accumulated = list(location.values())

    nx,ny = num_lat//10, num_long//10
    lon_bins = np.linspace(BBox[0],BBox[1],nx+1)
    lat_bins = np.linspace(BBox[2],BBox[3],ny+1)

    density, _, _ = np.histogram2d(longituds,latituds,[lon_bins,lat_bins])


    # fig = plt.figure(figsize=(18, 16))
    # ax = fig.add_subplot(131, title='imshow: square bins')
    # plt.imshow(density.T, interpolation='spline36', origin='lower',cmap='YlOrBr',  extent=[lon_bins[0], lon_bins[-1], lat_bins[0], lat_bins[-1]])
    # plt.show()

    # print((accumulated))
    # print(max(accumulated))

    # intervalos = range(min(accumulated), max(accumulated) + 2) #calculamos los extremos de los intervalos

    # plt.hist(x=accumulated, bins=intervalos, color='#F2AB6D', rwidth=0.85)
    # plt.title('Histograma de densidad')
    # plt.xlabel('Cantidad')
    # plt.ylabel('Frecuencia')
    # plt.xticks(intervalos)

    # plt.show() #dibujamos el histograma

    # color_value = [ acc for acc in accumulated ] 

    mymap = plt.imread("./media/map_CDNR.png")
    fig, ax = plt.subplots(figsize = (18,16))
    ax.scatter(longituds, latituds, s=10, c='r') #c=color_value, cmap='jet' )
    ax.set_title('Plotting Spatial Data on Map')
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])

    ax.imshow(mymap, extent = BBox, aspect= 'equal')
    plt.imshow(density.T, alpha=0.5,interpolation='spline36', origin='lower',cmap='YlOrBr',  extent=[lon_bins[0], lon_bins[-1], lat_bins[0], lat_bins[-1]])

    plt.show()

    


# Generate mapa density
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

            plt.savefig('./images_insights/test/'+'class_2_' + str(code)+'.png')
#---
def main():
    df = pd.read_csv("./querys/crecimientoNicolasRomero.csv")
    BBox = (-99.3686, -99.2670, 19.58, 19.65)

    # mymap = plt.imread("./media/map_CDNR.png")
    accumulated_geolocation_bussines(df, BBox )


if __name__ == "__main__":
    main()