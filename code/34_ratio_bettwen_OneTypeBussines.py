from calendar import c
from cgi import print_arguments
import code
from statistics import mean
from time import time
import pandas as pd
import numpy as np
from math import dist, radians, cos, sin, asin, sqrt
from matplotlib import pyplot as plt

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

def ratio_bettwen_OneTypeBussiness(df,code,time_window=0):
    #snaptime overview data
    df_filter_general = df[ df['Código_de_la_clase_de_actividad_SCIAN'] ==  code]
    #snaptime windows df
    df_window_time=[]
    #apply filter time on overview data
    df_window_time.append( df_filter_general[ df_filter_general['Fecha_de_incorporacion_al_DENUE'] < '2014-12' ] )
    df_window_time.append( df_filter_general[(df['Fecha_de_incorporacion_al_DENUE'] >= '2014-12')  & \
                                                        (df['Fecha_de_incorporacion_al_DENUE'] < '2019-11') ] )
    df_window_time.append( df_filter_general[ df['Fecha_de_incorporacion_al_DENUE'] >= '2019-11' ] )
    #we get list code types from dictionary
    ratio=0.0024
    codes_Neighbours = [311520, 311812, 311830, 311910, 312112, 315223, 321910, 322210, 322299, 323119, 326220, 332320, 332810, 335312, 337120, 434112, 434211, 434221, 434311, 434312, 434313, 434314, 434319, 435319, 461110, 461121, 461122, 461130, 461140, 461150, 461160, 461190, 461211, 461213, 462111, 462112, 463111, 463112, 463113, 463211, 463212, 463213, 463215, 463216, 463310, 464111, 464112, 464113, 465111, 465211, 465212, 465213, 465311, 465911, 465912, 465914, 465919, 466111, 466114, 466212, 466312, 466410, 467111, 467112, 467113, 467114, 467115, 468211, 468212, 468419, 531113, 531311, 532282, 532411, 532493, 541211, 541920, 541941, 561110, 561432, 561710, 611111, 611112, 611121, 611122, 611171, 611698, 621111, 621211, 621311, 621398, 624191, 624199, 624411, 711311, 713120, 713943, 713998, 722412, 722513, 722514, 722515, 722516, 722517, 722518, 722519, 811111, 811112, 811119, 811121, 811191, 811192, 811199, 811211, 811219, 811312, 811313, 811410, 811420, 811430, 811492, 811493, 811499, 812110, 812130, 812210, 812310, 813210, 931210, 931610]
    types_code = {}
    for code in codes_Neighbours:
        types_code[ code ] = 0

    print(types_code)
    #iterate time window
    for _, row_filter in df_window_time[time_window].iterrows():
        types_code = types_code.copy()
        lat = row_filter['Latitud']
        long= row_filter['Longitud']
        for _, row in df.iterrows():
            if abs((row['Latitud'] - lat) ) < ratio and  abs((row['Longitud'] - long)) < ratio:
                types_code[ row['Código_de_la_clase_de_actividad_SCIAN']] +=  1 
                # all_class.add( row['Código_de_la_clase_de_actividad_SCIAN'])
        print( row_filter['Nombre_de_la_Unidad_Económica'],  list(types_code.values()))

def average_distance(df,type_code):
    list_distances=[]
    df_filter_code = df[ df['Código_de_la_clase_de_actividad_SCIAN'] == type_code]
    df_filter_codeCopy = df_filter_code.copy()
    print(df_filter_code)
    for __, base in df_filter_code.iterrows():
        array = []
        for _, row in df_filter_codeCopy.iterrows():
            array.append(max(abs(row['Latitud']- base['Latitud']), abs(row['Longitud']-base['Longitud'])))
        array.sort()
        list_distances.append(array[1])
    df_distances = pd.DataFrame(list_distances, columns = ['DistancesTotals'])
    # plt.xlim([min(data)-5, max(data)+5])
    plt.hist(list_distances, bins=40)
    plt.show()
    print(df_distances.describe()/2)
    return  df_distances

def main():
    df = pd.read_csv("../querys/crecimientoNicolasRomero.csv")
    code= 312112
    time_window=2
    # codes_Neighbours = [311520, 311812, 311830, 311910, 312112, 315223, 321910, 322210, 322299, 323119, 326220, 332320, 332810, 335312, 337120, 434112, 434211, 434221, 434311, 434312, 434313, 434314, 434319, 435319, 461110, 461121, 461122, 461130, 461140, 461150, 461160, 461190, 461211, 461213, 462111, 462112, 463111, 463112, 463113, 463211, 463212, 463213, 463215, 463216, 463310, 464111, 464112, 464113, 465111, 465211, 465212, 465213, 465311, 465911, 465912, 465914, 465919, 466111, 466114, 466212, 466312, 466410, 467111, 467112, 467113, 467114, 467115, 468211, 468212, 468419, 531113, 531311, 532282, 532411, 532493, 541211, 541920, 541941, 561110, 561432, 561710, 611111, 611112, 611121, 611122, 611171, 611698, 621111, 621211, 621311, 621398, 624191, 624199, 624411, 711311, 713120, 713943, 713998, 722412, 722513, 722514, 722515, 722516, 722517, 722518, 722519, 811111, 811112, 811119, 811121, 811191, 811192, 811199, 811211, 811219, 811312, 811313, 811410, 811420, 811430, 811492, 811493, 811499, 812110, 812130, 812210, 812310, 813210, 931210, 931610]  
    # BBox = (-99.3686, -99.2670, 19.58, 19.65)
    # mymap = plt.imread("../media/map_CDNR.png")
    ratio = 0.0002
    #print(average_distance(df, code).mean())
    
    # average_distance(df,code)
    ratio_bettwen_OneTypeBussiness(df,code,time_window)
if __name__ == "__main__":
    main()