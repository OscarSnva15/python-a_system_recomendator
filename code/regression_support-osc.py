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


def plot_scatter_bussines_acumulated(df, code = 312112):

    # Filter data by CODE
    df_filter_class = df[ df['Código_de_la_clase_de_actividad_SCIAN'] ==  code]
    df_filter_class_snaptime = []
    # Filter data by DATE
    df_filter_class_snaptime.append( df_filter_class[ df_filter_class['Fecha_de_incorporacion_al_DENUE'] < '2014-12' ] )
    df_filter_class_snaptime.append( df_filter_class[ (df['Fecha_de_incorporacion_al_DENUE'] >= '2014-12')  & \
                                                        (df['Fecha_de_incorporacion_al_DENUE'] < '2019-11') ] )
    df_filter_class_snaptime.append( df_filter_class[ df_filter_class['Fecha_de_incorporacion_al_DENUE']>= '2019-11' ] )

    # deltaTwo    = 0.00099
    delta = 0.0012

    # print( "radio KM: ",distance(0,deltaTwo,0,0) )
    print( "radio KM: ",distance(0,delta,0,0) ) 
    #codes = [311520, 311812, 311830, 311910, 312112, 315223, 321910, 322210, 322299, 323119, 326220, 332320, 332810, 335312, 337120, 434112, 434211, 434221, 434311, 434312, 434313, 434314, 434319, 435319, 461110, 461121, 461122, 461130, 461140, 461150, 461160, 461190, 461211, 461213, 462111, 462112, 463111, 463112, 463113, 463211, 463212, 463213, 463215, 463216, 463310, 464111, 464112, 464113, 465111, 465211, 465212, 465213, 465311, 465911, 465912, 465914, 465919, 466111, 466114, 466212, 466312, 466410, 467111, 467112, 467113, 467114, 467115, 468211, 468212, 468419, 531113, 531311, 532282, 532411, 532493, 541211, 541920, 541941, 561110, 561432, 561710, 611111, 611112, 611121, 611122, 611171, 611698, 621111, 621211, 621311, 621398, 624191, 624199, 624411, 711311, 713120, 713943, 713998, 722412, 722513, 722514, 722515, 722516, 722517, 722518, 722519, 811111, 811112, 811119, 811121, 811191, 811192, 811199, 811211, 811219, 811312, 811313, 811410, 811420, 811430, 811492, 811493, 811499, 812110, 812130, 812210, 812310, 813210, 931210, 931610]
    # __bussines_class = {}
    # for code in codes:
    #     __bussines_class[ code ] = 0
    all_class = set()
    
    for i, row_filter in df_filter_class_snaptime[1].iterrows():
        # bussines_class = __bussines_class.copy()
        lat= row_filter['Latitud']
        long=row_filter['Longitud']
        for i, row in df.iterrows():
            if abs( (row['Latitud'] - lat) ) < delta and  abs( (row['Longitud'] - long) ) < delta:
                # bussines_class[ row['Código_de_la_clase_de_actividad_SCIAN'] ] +=  1 
                all_class.add(row['Código_de_la_clase_de_actividad_SCIAN'])

        # print( row_filter['Nombre_de_la_Unidad_Económica'],  list(bussines_class.values()))
        # print( list(bussines_class.keys()))
        # print( list(bussines_class.values()))

    all_class = sorted( all_class )
    print( len(all_class) )


def main():
    df = pd.read_csv("../querys/crecimientoNicolasRomero.csv")
    BBox = (-99.3686, -99.2670, 19.58, 19.65)
    # mymap = plt.imread("../media/map_CDNR.png")
    plot_scatter_bussines_acumulated(df)

if __name__ == "__main__":
    main()