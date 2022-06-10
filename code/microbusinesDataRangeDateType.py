from cgi import print_form
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import dist, radians, cos, sin, asin, sqrt
from dataclasses import dataclass

latitude1, longitude1 = [19.599472210151948, -99.30688849000485]

class Business:
    def __init__(self, id, name, clave_business, clase, agb, latitude, longitude, age):
        self.id = id
        self.name = name
        self.clave_business = clave_business
        self.clase = clase
        self.agb = agb
        self.latitude = latitude
        self.longitude = longitude
        self.age = age

def distance(lat1, lat2, lon1, lon2):
        lon1 = radians(lon1)
        lon2 = radians(lon2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        r = 6371
        return(c * r)

def plot_scatter_bussines_acumulated(df, BBox, mymap, code):
    df_filters = pd.DataFrame(columns=['Nombre_de_la_Unidad_Económica','Código_de_la_clase_de_actividad_SCIAN','Área_geoestadística_básica','Latitud','Longitud','Fecha_de_incorporacion_al_DENUE'])
    
    print(df_filters.head)
    for i in range(len(df)):
        # print(df.loc[i,"ID"],df.loc[i,"Nombre_de_la_Unidad_Económica"],df.loc[i,"Código_de_la_clase_de_actividad_SCIAN"],df.loc[i,"Área_geoestadística_básica"],df.loc[i,"Latitud"],df.loc[i,"Longitud"],df.loc[i,"Fecha_de_incorporacion_al_DENUE"])
        if(distance(latitude1, df.loc[i,"Latitud"], longitude1, df.loc[i,"Longitud"] ) < 0.250 ):
            
            # print("adios")
            df_filters=df_filters.append({
                                        'Nombre_de_la_Unidad_Económica': df.loc[i,"Nombre_de_la_Unidad_Económica"],
                                        'Código_de_la_clase_de_actividad_SCIAN': df.loc[i,"Código_de_la_clase_de_actividad_SCIAN"],
                                        'Área_geoestadística_básica': df.loc[i,"Área_geoestadística_básica"],
                                        'Latitud': df.loc[i,"Latitud"],
                                        'Longitud': df.loc[i,"Longitud"],
                                        'Fecha_de_incorporacion_al_DENUE': df.loc[i,"Fecha_de_incorporacion_al_DENUE"]
                                        }, ignore_index = True)
            # df_filters=df_filters.append({'Código_de_la_clase_de_actividad_SCIAN':df.loc[i,"Código_de_la_clase_de_actividad_SCIAN"]}, ignore_index = True)
            # df_filters=df_filters.append({'Área_geoestadística_básica':df.loc[i,"Área_geoestadística_básica"]}, ignore_index = True)
            # df_filters=df_filters.append({'Latitud':df.loc[i,"Latitud"]}, ignore_index = True)
            # df_filters=df_filters.append({'Longitud':df.loc[i,"Longitud"]}, ignore_index = True)
            # df_filters=df_filters.append({'Fecha_de_incorporacion_al_DENUE':df.loc[i,"Fecha_de_incorporacion_al_DENUE"]}, ignore_index = True)

def main():
    df = pd.read_csv("../querys/crecimientoNicolasRomero.csv")
    mymap = plt.imread("../media/map_CDNR.png")
    BBox = ((-99.3686, -99.2670, 19.58, 19.65))
    target_location = [19.599472210151948, -99.30688849000485]
    plot_scatter_bussines_acumulated( df, BBox, mymap, 461110)
    plt.show()

if __name__ == "__main__":
    main()