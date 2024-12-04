from scipy.spatial import cKDTree
import pandas as pd
from dataclasses import dataclass
from geopy.distance import geodesic
from math import dist, radians, cos, sin, asin, sqrt
from matplotlib import pyplot as plt
import numpy as np
import statistics
from typing import Tuple
from typing import List
from matplotlib.patches import Circle
from cartopy import crs as ccrs
from math import dist, radians, cos, sin, asin, sqrt, atan2



@dataclass
class Recomender:
    df: pd.DataFrame
    time_window: int
    mymap: np.ndarray
    BBox: Tuple[float, float, float, float]
    filter_bussines_code_class: pd.DataFrame
    filter_bussines_code_class_acumulated: pd.DataFrame
    filter_bussines_code_class_support: pd.DataFrame
    filter_bussines_code_class_support_acumulated: pd.DataFrame
    bussines_suport_into_radio_for_each_bussines_class : pd.DataFrame
    list_dist: List[pd.DataFrame]
    influence_radio: float
    #
    code_poles: set
    def __init__(self, df, code_class, time_window ):
        self.df = df
        self.code_class = code_class
        self.time_window = time_window
        self.mymap = plt.imread("../media/map_CDNR.png")
        self.BBox = ((-99.3686, -99.2670, 19.58, 19.65))
        # get the dataframe filter_bussines_code_class
        self.filter_bussines_code_class = self.filter_by_code()
        self.filter_bussines_code_class_acumulated = self.filter_by_code_acumulated()
        # get the dataframe filter_bussines_code_class_neighbors
        self.filter_bussines_code_class_support = self.filter_by_code_support()
        self.filter_bussines_code_class_support_acumulated = self.filter_by_code_support_acumulated()
        self.list_dist = []
        #
        self.code_poles = (465311,
                            812110,
                            463211,
                            461122,
                            722513,
                            467111,
                            461130,
                            461160,
                            311830,
                            311812,
                            722514,
                            461121,
                            464111,
                            722517,
                            561432,
                            467115,
                            811111,
                            722518,
                            722515,
                            722519,
                            621211,
                            332320,
                            461190,
                            813210,
                            465912,
                            466410,
                            468211,
                            531113,
                            811121)

    def filter_by_code(self):
        df_filter_general = self.df[ self.df['Código_de_la_clase_de_actividad_SCIAN'] ==  self.code_class]
        filtered = None
        if self.time_window == 1:
            filtered =  df_filter_general[df_filter_general['Fecha_de_incorporacion_al_DENUE'] < '2014-12']
        elif self.time_window == 2:
            filtered =  df_filter_general[(df_filter_general['Fecha_de_incorporacion_al_DENUE'] >= '2014-12') & (df_filter_general['Fecha_de_incorporacion_al_DENUE'] < '2019-11')]
        elif self.time_window == 3:
            filtered =  df_filter_general[df_filter_general['Fecha_de_incorporacion_al_DENUE'] >= '2019-11']
        else:
            filtered = df_filter_general

        print("INIT Time Window:", self.time_window, "  TOTAL BUSSINESS FOUND: ", len(filtered))

        output_file = "../querys/distancias/reporte_distancias/filter_bussines_code_class.xlsx"
        df = pd.DataFrame(filtered)
        df.to_excel(output_file, index=False)

        return filtered

    def filter_by_code_acumulated(self):
        df_filter_general = self.df[ self.df['Código_de_la_clase_de_actividad_SCIAN'] ==  self.code_class]


        print("INIT Time Window:", self.time_window, "  TOTAL BUSSINESS ACUMULATED FOUND: ", len(df_filter_general))

        output_file = "../querys/distancias/reporte_distancias/filter_bussines_code_class_acumulated.xlsx"
        df = pd.DataFrame(df_filter_general)
        df.to_excel(output_file, index=False)

        return df_filter_general

    def filter_by_code_support(self):
        codes_support = [461110, 465311, 812110, 463211, 461122, 722513, 467111, 461130, 461160, 311830, 311812, 722514, 461121, 464111, 722517, 561432, 467115, 811111, 722518, 722515, 722519, 621211, 332320, 461190, 813210, 465912, 466410, 468211]
        df_filter_general = self.df[self.df['Código_de_la_clase_de_actividad_SCIAN'].isin(codes_support)]
        filtered = None
        if self.time_window == 1:
            filtered =  df_filter_general[df_filter_general['Fecha_de_incorporacion_al_DENUE'] < '2014-12']
        elif self.time_window == 2:
            filtered =  filtered =  df_filter_general[(df_filter_general['Fecha_de_incorporacion_al_DENUE'] >= '2014-12') & (df_filter_general['Fecha_de_incorporacion_al_DENUE'] < '2019-11')]
        elif self.time_window == 3:
            filtered =  filtered =  df_filter_general[df_filter_general['Fecha_de_incorporacion_al_DENUE'] >= '2019-11']
        else:
            filtered = df_filter_general

        print("INIT Time Window:", self.time_window, "  TOTAL BUSSINESS SUPPORT FOUND:", len(filtered))

        output_file = "../querys/distancias/reporte_distancias/filter_bussines_code_class_support.xlsx"
        df = pd.DataFrame(filtered)
        df.to_excel(output_file, index=False)

        return filtered

    def filter_by_code_support_acumulated(self):
        codes_support = [461110, 465311, 812110, 463211, 461122, 722513, 467111, 461130, 461160, 311830, 311812, 722514, 461121, 464111, 722517, 561432, 467115, 811111, 722518, 722515, 722519, 621211, 332320, 461190, 813210, 465912, 466410, 468211]
        df_filter_general = self.df[self.df['Código_de_la_clase_de_actividad_SCIAN'].isin(codes_support)]


        print("INIT Time Window:", self.time_window, "  TOTAL BUSSINESS SUPPORT ACUMULATED FOUND:", len(df_filter_general))

        output_file = "../querys/distancias/reporte_distancias/filter_bussines_code_class_support_acumulated.xlsx"
        df = pd.DataFrame(df_filter_general)
        df.to_excel(output_file, index=False)

        return df

    def filter_by_code_show_plot(self):
        # Filter data by CODE
        df_filter_class = self.df[self.df['Código_de_la_clase_de_actividad_SCIAN'] == self.code_class]
        #list df_filter_class_snaptime
        df_filter_class_snaptime = []
        # Filter data by DATE
        df_filter_class_snaptime.append(df_filter_class[df_filter_class['Fecha_de_incorporacion_al_DENUE'] < '2014-12'])
        df_filter_class_snaptime.append(df_filter_class[(df_filter_class['Fecha_de_incorporacion_al_DENUE'] >= '2014-12') & (df_filter_class['Fecha_de_incorporacion_al_DENUE'] < '2019-11')])
        df_filter_class_snaptime.append(df_filter_class[df_filter_class['Fecha_de_incorporacion_al_DENUE'] >= '2019-11'])

        color = ['r', 'g', 'b']
        title = ["Fecha Nacimiento<2014-12", " 2014-12>=Fecha Nacimiento<2019-11", "2019-11>=Fecha Nacimiento<2022-05"]
        subtitle = 'Código_de_la_clase_de_actividad ' + str( self.filter_bussines_code_class['Código_de_la_clase_de_actividad_SCIAN'].iloc[1]) + ': ' + str(self.filter_bussines_code_class['Nombre_de_clase_de_la_actividad'].iloc[1])
        fig, ax = plt.subplots(nrows=1, ncols=self.time_window, figsize=(26, 10))

        if (self.time_window>1):
            for i in range(self.time_window):
                ax[i].set_title(title[i])
                ax[i].set_xlabel('Longitud')
                ax[i].set_ylabel('Latitud')
                ax[i].set_xlim(self.BBox[0], self.BBox[1])
                ax[i].set_ylim(self.BBox[2], self.BBox[3])
                ax[i].imshow(self.mymap, zorder=0, extent=self.BBox, aspect='equal')
                for j in range(i + 1):
                    ax[i].scatter(df_filter_class_snaptime[j]['Longitud'], df_filter_class_snaptime[j]['Latitud'], zorder=1,alpha=0.71, c=color[j], s=10)
        else:

            ax.set_title(title[0])
            ax.set_xlabel('Longitud')
            ax.set_ylabel('Latitud')
            ax.set_xlim(self.BBox[0], self.BBox[1])
            ax.set_ylim(self.BBox[2], self.BBox[3])
            ax.imshow(self.mymap, zorder=0, extent=self.BBox, aspect='equal')
            for j in range(self.time_window):
                ax.scatter(df_filter_class_snaptime[j]['Longitud'], df_filter_class_snaptime[j]['Latitud'], zorder=1,alpha=0.71, c=color[j], s=10)

        fig.suptitle(subtitle)
        plt.savefig("../images_insights/plots_filter_by_code_show_plot/plots_filter_by_code_show_plot.png")
        plt.show()

        if len(self.filter_bussines_code_class) > 0:
            response = {
                "status": 'TRUE',
                "code": 200,
                "mensaje": 'successfull'
            }
        else:
                response = {
                    "status": 'FALSE',
                    "code": 505,
                    "mensaje": 'unsuccessfull'
                }

        return response

    def filter_by_code_acumulated_show_plot(self):
        color = 'b'
        title = ["Acumulado Fecha Nacimiento 2014-12, 2019-11, 2022-05"]
        subtitle = 'Código_de_la_clase_de_actividad ' + str( self.filter_bussines_code_class_acumulated['Código_de_la_clase_de_actividad_SCIAN'].iloc[1]) + ': ' + str(self.filter_bussines_code_class_support['Nombre_de_clase_de_la_actividad'].iloc[1])
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(26, 10))

        for idx_otros, row_f in self.filter_bussines_code_class_acumulated.iterrows():
            lat_f = row_f['Latitud']
            lon_f = row_f['Longitud']
            ax.scatter(lon_f ,
                       lat_f, color=color, label='BusinessClass',
                       marker='o', s=10, alpha=0.71)
            #ax.text(lon_f,
                    #lat_f,
                    #row_f['Nombre_de_la_Unidad_Económica'], fontsize=9)


        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')
        ax.set_xlim(self.BBox[0], self.BBox[1])
        ax.set_ylim(self.BBox[2], self.BBox[3])
        ax.imshow(self.mymap, zorder=0, extent=self.BBox, aspect='equal')
        ax.set_title(title)
        fig.suptitle(subtitle)
        plt.savefig("../images_insights/plots_filter_by_code_show_plot/plots_filter_by_code_show_plot.png")
        plt.show()

        if len(self.filter_bussines_code_class_acumulated) > 0:
            response = {
                "status": 'TRUE',
                "code": 200,
                "mensaje": 'successfull',
                "plots" : self.filter_bussines_code_class_acumulated.shape
            }
        else:
                response = {
                    "status": 'FALSE',
                    "code": 505,
                    "mensaje": 'unsuccessfull',
                    "plots": 0
                }

        return response

    def filter_by_code_support_show_plot(self):
        codes_support = [461110, 465311, 812110, 463211, 461122, 722513, 467111, 461130, 461160, 311830, 311812, 722514, 461121, 464111, 722517, 561432, 467115, 811111, 722518, 722515, 722519, 621211, 332320, 461190, 813210, 465912, 466410, 468211]
        df_filter_class = self.df[self.df['Código_de_la_clase_de_actividad_SCIAN'].isin(codes_support)]
        # list df_filter_class_snaptime
        df_filter_class_snaptime = []
        # Filter data by DATE
        df_filter_class_snaptime.append(df_filter_class[df_filter_class['Fecha_de_incorporacion_al_DENUE'] < '2014-12'])
        df_filter_class_snaptime.append(df_filter_class[ (df_filter_class['Fecha_de_incorporacion_al_DENUE'] >= '2014-12') & ( df_filter_class[ 'Fecha_de_incorporacion_al_DENUE'] < '2019-11')])
        df_filter_class_snaptime.append( df_filter_class[df_filter_class['Fecha_de_incorporacion_al_DENUE'] >= '2019-11'])

        color = ['r', 'g', 'b']
        title = ["Fecha Nacimiento<2014-12", " 2014-12>=Fecha Nacimiento<2019-11", "2019-11>=Fecha Nacimiento<2022-05"]
        subtitle = 'Códigos_de_la_clase_de_actividad_base_encontrados'
        fig, ax = plt.subplots(nrows=1, ncols=self.time_window, figsize=(26, 10))

        if (self.time_window > 1):

            for i in range(self.time_window):
                ax[i].set_title(title[i])
                ax[i].set_xlabel('Longitud')
                ax[i].set_ylabel('Latitud')
                ax[i].set_xlim(self.BBox[0], self.BBox[1])
                ax[i].set_ylim(self.BBox[2], self.BBox[3])
                ax[i].imshow(self.mymap, zorder=0, extent=self.BBox, aspect='equal')
                for j in range(i + 1):
                    ax[i].scatter(df_filter_class_snaptime[j]['Longitud'], df_filter_class_snaptime[j]['Latitud'],
                                  zorder=1, c=color[j], s=10, label='BusinessClass', marker='o',alpha=0.71)
        else:

            ax.set_title(title[0])
            ax.set_xlabel('Longitud')
            ax.set_ylabel('Latitud')
            ax.set_xlim(self.BBox[0], self.BBox[1])
            ax.set_ylim(self.BBox[2], self.BBox[3])
            ax.imshow(self.mymap, zorder=0, extent=self.BBox, aspect='equal')
            for j in range(self.time_window):
                ax.scatter(df_filter_class_snaptime[j]['Longitud'], df_filter_class_snaptime[j]['Latitud'], zorder=1, c=color[j], s=10, label='BusinessClass', marker='o',alpha=0.71)

        fig.suptitle(subtitle)
        plt.savefig("../images_insights/plots_filter_by_code_show_plot/plots_filter_by_code_support_show_plot.png")
        plt.show()

        if len(df_filter_class_snaptime) > 0:
            response = {
                "status": 'TRUE',
                "code": 200,
                "mensaje": 'successfull'
            }
        else:
            response = {
                "status": 'FALSE',
                "code": 505,
                "mensaje": 'unsuccessfull'
            }

        return response

    def filter_by_code_support_acumulated_show_plot(self):
        color = 'b'
        title = ["Acumulado de micronegocios base Fecha Nacimiento 2014-12, 2019-11, 2022-05"]
        subtitle = 'Código_de_la_clase_de_actividad 461110, 465311, 812110, 463211, 461122, 722513, 467111, 461130, 461160, 311830, 311812, 722514, 461121, 464111, 722517, 561432, 467115, 811111, 722518, 722515, 722519, 621211, 332320, 461190, 813210, 465912, 466410, 468211'
        fig, ax = plt.subplots(nrows=int(1), ncols=int(1), figsize=(26, 10))

        for idx_otros, row_f in self.filter_bussines_code_class_support_acumulated.iterrows():
            lat_f = row_f['Latitud']
            lon_f = row_f['Longitud']
            ax.scatter(lon_f,
                       lat_f, color=color, label='BusinessClass',
                       marker='o', s=10, alpha=0.71)
            #ax.text(lon_f,
                    #lat_f,
                    #row_f['Nombre_de_la_Unidad_Económica'], fontsize=5)

        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')
        ax.set_xlim(self.BBox[0], self.BBox[1])
        ax.set_ylim(self.BBox[2], self.BBox[3])
        ax.imshow(self.mymap, zorder=0, extent=self.BBox, aspect='equal')
        ax.set_title(title)
        fig.suptitle(subtitle)
        plt.savefig("../images_insights/plots_filter_by_code_show_plot/plots_filter_by_code_support_acumulated_show_plot.png")
        plt.show()

        if len(self.filter_bussines_code_class_support_acumulated) > 0:
            response = {
                "status": 'TRUE',
                "code": 200,
                "mensaje": 'successfull',
                "plots": self.filter_bussines_code_class_support_acumulated.shape
            }
        else:
            response = {
                "status": 'FALSE',
                "code": 505,
                "mensaje": 'unsuccessfull',
                "plots": 0
            }

        return response

    #mecanismo para obtener ratio de influencia de tipo de clase de actividad económica(oscar)
    def show_distances_for_each_business_false(self):
        for x in range(len(self.filter_bussines_code_class_acumulated)):
            #print("*graph_distances_for_each_bussines *\n")
            #df_dist = bussines_snapshot.show_distances_for_each_bussines(mymap, BBox, x)
            color = ['r', 'g', 'b']
            title = "Acumulado de micronegocios registrados en 2014-12, 2019-11, 2022-05"
            subtitle = 'Código_de_la_clase_de_actividad ' + str(self.code_class) + ':' + self.filter_bussines_code_class_acumulated['Nombre_de_clase_de_la_actividad'].iloc[1]
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(26, 10))

            all_distances = []  # Para almacenar las distancias en un dataframe

            ax.set_title(title)  # Usar un string en lugar de lista
            ax.set_xlabel('Longitud')
            ax.set_ylabel('Latitud')
            ax.set_xlim(self.BBox[0], self.BBox[1])
            ax.set_ylim(self.BBox[2], self.BBox[3])
            ax.imshow(self.mymap, zorder=0, extent=self.BBox, aspect='equal')

            longitud = self.filter_bussines_code_class_acumulated['Longitud'].values
            latitud = self.filter_bussines_code_class_acumulated['Latitud'].values
            ax.scatter(longitud, latitud, zorder=1, alpha=0.71, c=color[2], s=10)
            # generamos dataframe que contendra los dataframe generados de distancias
            # Calcular las distancias desde un solo negocio
            if len(longitud) > 1:
                points = list(zip(latitud, longitud))
                point_idx = int(x)  # Seleccionar el primer negocio para simular las distancias
                point_idx_name = self.filter_bussines_code_class_acumulated['Nombre_de_la_Unidad_Económica'].iloc[int(x)]
                point = points[point_idx]

                for k in range(len(points)):  # Cambiar el rango para incluir todos los puntos
                    neighbor_idx = k  # Índice del vecino
                    neighbor_idx_name = self.filter_bussines_code_class_acumulated['Nombre_de_la_Unidad_Económica'].iloc[k]  # Nombre del vecino
                    neighbor_idx_type = self.filter_bussines_code_class_acumulated['Nombre_de_clase_de_la_actividad'].iloc[k]  # Nombre del vecino
                    neighbor_idx_code = self.filter_bussines_code_class_acumulated['Código_de_la_clase_de_actividad_SCIAN'].iloc[k]  # Nombre del vecino

                    point_lat, point_lon = point
                    neighbor_lat, neighbor_lon = points[neighbor_idx]

                    # Usar la fórmula de Haversine para calcular la distancia en metros
                    distance_to_neighbor = geodesic((point_lat, point_lon), (neighbor_lat, neighbor_lon)).meters
                    # se inicia una lista vacia para almacenar distancias calculadas con respecto a otros negocios

                    # Dibujar línea de distancia
                    ax.plot([point_lon, neighbor_lon], [point_lat, neighbor_lat], color='black', linewidth=0.5,
                            alpha=0.7)

                    # Almacenar la distancia en la lista
                    all_distances.append({
                        'Negocio_Principal': point_idx_name,
                        'Negocio_Vecino': neighbor_idx_name,
                        'Distancia_m': distance_to_neighbor,
                        'Tipo': neighbor_idx_type,
                        'Codigo_class': neighbor_idx_code
                    })

                # Agregar subtítulo a la figura fuera del bucle
                fig.suptitle(subtitle)

                # Mostrar la figura (opcional)
                #plt.show()

                # Guardar la imagen para cada negocio-------------------------------------------------------
                #plt.savefig(
                    #'../querys/distancias/imagenes_distancias/CODE_CLASS_' + str(self.code_class) + '_' + str(
                        #point_idx) + '.-IMG_DISTANCIAS_DEL_NEGOCIO_' + str(point_idx_name) + '.png')
                plt.close()
                # -------------------------------------------------------------------------------------------

                # Convertir la lista de distancias en un DataFrame y guardar como Excel---------------------
                df_distances = pd.DataFrame(all_distances)
                #df_distances.to_excel(
                    #'../querys/distancias/reporte_distancias/CODE_CLASS_' + str(self.code_class) + '_' + str(
                        #point_idx) + '.-DISTANCIAS_DEL_NEGOCIO_' + str(point_idx_name) + '.xlsx')
                # -------------------------------------------------------------------------------------------
                self.list_dist.append(df_distances)

        if len(self.list_dist) > 0:
            data = self.get_influence_radio_from_list_distances_for_code_class()
            if data['code'] == 200:
                self.influence_radio = round(data['influence_ratio'], 2)
                #self.influence_radio = 1230.00
                response = {
                    "status": 'TRUE',
                    "code": 200,
                    "mensaje": 'successfull_graph_distances_acumulated_and_influence_ratio',
                    "influence_ratio": self.influence_radio
                }
            else:
                self.influence_radio = 0
                response = {
                    "status": 'TRUE',
                    "code": 200,
                    "mensaje": 'successfull_graph_distances_acumulated_but_ratio_not_found',
                    "influence_ratio": float(0.0)
                }
        else:
            response = {
                "status": 'FALSE',
                "code": 505,
                "mensaje": 'unsuccessfull'
            }
        return response
    def show_distances_for_each_business(self):
        list_distances = []

        # información de los negocios filtrados por epoca señalada y codigo de clase de actividad, con su latitud y longitud.
        for _, base in self.filter_bussines_code_class_acumulated.iterrows():
            # se inicia una lista vacia para almacenar distancias calculadas con respecto a otros negocios
            array = []

            # The all business to comparate with the step data
            for _, row in self.filter_bussines_code_class_acumulated.iterrows():

                # Se checa que el negocio  no sea el mismo que el negocio base, viendo las diferencias lat. long. no == cero.
                if (base['Latitud'] - row['Latitud']) != 0 and (base['Latitud'] - row['Latitud']) != 0:
                    array.append(self.haversine(base['Latitud'], base['Longitud'], row['Latitud'], row['Longitud']))

            # la lista se ordena de menor a mayor.
            array.sort()

            # Se almacena la distancia mínima (es decir, la primera en la lista ordenada)
            list_distances.append(array[0])

        list_distances.sort()
        self.influence_radio = (sum(list_distances) / len(list_distances))/2
        print("Influence ratio = ", self.influence_radio)
        return self.influence_radio
    def show_distances_for_each_business_(self):
        list_distances = []

        # información de los negocios filtrados por epoca señalada y codigo de clase de actividad, con su latitud y longitud.
        for _, base in self.filter_bussines_code_class_acumulated.iterrows():
            # se inicia una lista vacia para almacenar distancias calculadas con respecto a otros negocios
            array = []

            # The all business to comparate with the step data
            for _, row in self.filter_bussines_code_class_acumulated.iterrows():

                # Se checa que el negocio  no sea el mismo que el negocio base, viendo las diferencias lat. long. no == cero.
                if (base['Latitud'] - row['Latitud']) != 0 and (base['Latitud'] - row['Latitud']) != 0:
                    array.append(self.haversine(base['Latitud'], base['Longitud'], row['Latitud'], row['Longitud']))

            # la lista se ordena de menor a mayor.
            array.sort()

            # Se almacena la distancia mínima (es decir, la primera en la lista ordenada)
            list_distances.append(array[0])

        list_distances.sort()
        #*******OBTNECION OFICIAL DEL RADIO DE INFLUENCIA_DOC TESYS*********
        self.influence_radio = (sum(list_distances) / len(list_distances))/2

        print("Influence ratio = ", self.influence_radio)
        df_distances = pd.DataFrame(list_distances)

        df_distances.to_excel('../querys/distancias/reporte_distancias/CODE_CLASS_' + str(self.code_class) + '.-DISTANCIAS_DEL_NEGOCIO_' + str(self.code_class) + '.xlsx')
        return self.influence_radio


    def haversine(self, lat1, lon1, lat2, lon2):
        # Convertir grados a radianes
        lat1_rad = radians(lat1)
        lon1_rad = radians(lon1)
        lat2_rad = radians(lat2)
        lon2_rad = radians(lon2)

        # Diferencias
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Fórmula de Haversine
        a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Radio de la Tierra en kilómetros
        radius = 6371.0

        # Distancia en kilómetros
        distance = radius * c
        return distance
    def get_influence_radio_from_list_distances_for_code_class(self):
        medias = []  # Lista para almacenar las medias
        medianas = []  # Lista para almacenar las medianas
        minimas = []  # Lista para almacenar las minima
        distanciasTotals = []
        for i, df in enumerate(self.list_dist):
            df['Distancia_m'] = pd.to_numeric(df['Distancia_m'], errors='coerce')
            distanciasTotals.append(df['Distancia_m'])
            media = df['Distancia_m'].mean()
            mediana = df['Distancia_m'].median()
            minima = df[df['Distancia_m'] != 0]['Distancia_m'].min()
            medias.append(media)  # Almacenar la media
            medianas.append(mediana)  # Almacenar la mediana
            minimas.append(minima)  # Almacenar la minima
            #business_name = df.iloc[i, 0]
            #print(f"La media del bussines {business_name} de todas sus distancias obtenidas es: {media} metros, su mediana es {mediana}")

        reportDistanciasTotals = pd.DataFrame(distanciasTotals)
        reportDistanciasTotals.to_excel('../querys/distancias/reporte_distancias/REPORT_DISTANCIAS_TOTALS_FOUND_DELA_CLASE_DE_NEGOCIO.xlsx')

        reportDistanciasMinimasTotals = pd.DataFrame(minimas)
        reportDistanciasMinimasTotals.to_excel(
            '../querys/distancias/reporte_distancias/REPORT_DISTANCIAS_MINIMAS_TOTALS_FOUND_DELA_CLASE_DE_NEGOCIO.xlsx')

        #De toda la lista obtenida de medias y medianas se procede nuevamente a sacar sus mediana
        media_medias = statistics.mean(medias)
        median_medias = statistics.median(medias)

        media_medians = statistics.mean(medianas)
        median_medians = statistics.median(medianas)

        #print(f"La media de la mediana\n", media_medians)
        #print(f"La mediana de la mediana(influence_radio_choose)\n", median_medians)

        #print(f"La media de la media\n", media_medias)
        #print(f"La mediana de la media\n", median_medias)

        if median_medians > 0:
            response = {
                "status": 'TRUE',
                "code": 200,
                "mensaje": 'successfull',
                "influence_ratio": float(median_medians/2)
            }

        else:
            response = {
                "status": 'FALSE',
                "code": 505,
                "mensaje": 'unsuccessfull',
                "influence_ratio": 'no_iter'
            }
        return response


    def find_business_into_radius_original_osc(self):
        results = []
        # Recorremos cada ue de la clase filtrada de interes
        for _, row_class_interes in self.filter_bussines_code_class_acumulated.iterrows():
            coords_class_interes = (row_class_interes['Latitud'], row_class_interes['Longitud'])
            negocios_dentro_radio = []

            # Lista para almacenar los índices de las unidades económicas encontradas
            # negocios_a_eliminar = []

            for idx_negocio, row_negocio in self.filter_bussines_code_class_support_acumulated.iterrows():
                coords_negocio = (row_negocio['Latitud'], row_negocio['Longitud'])

                # Calcular la distancia entre la clase y el otro negocio
                distancia = geodesic(coords_class_interes, coords_negocio).meters

                # Verificar si está dentro del radio
                if distancia < self.influence_radio:
                    negocios_dentro_radio.append({
                        'Negocio_de_interes': row_class_interes['Nombre_de_la_Unidad_Económica'],
                        'Radio_influencia': self.influence_radio,
                        'Negocio_vecino_encontrado': row_negocio['Nombre_de_la_Unidad_Económica'],
                        'Codigo': row_negocio['Código_de_la_clase_de_actividad_SCIAN'],
                        'Tipo': row_negocio['Nombre_de_clase_de_la_actividad'],
                        'Distancia_(m)': distancia,
                        'Longitud': row_negocio['Longitud'],
                        'Latitud': row_negocio['Latitud']
                    })
                    # Marcar el negocio encontrado para ser eliminado después
                    # negocios_a_eliminar.append(idx_negocio)


            # Eliminar las unidades económicas encontradas del dataframe
            #df_to_bucle.drop(negocios_a_eliminar, inplace=True)

            # Agregar los negocios encontrados para esta ue
            if negocios_dentro_radio:
                results.extend(negocios_dentro_radio)

        output_file = "../querys/distancias/reporte_distancias/business_suport_acumulated_into_radius.xlsx"
        df = pd.DataFrame(results)
        # eliminar negocios duplicados
        #df = df.drop_duplicates(subset='Negocio_vecino_encontrado')
        df.to_excel(output_file, index=False)
        self.bussines_suport_into_radio_for_each_bussines_class = df
        if len(df) > 0:
            response = {
                "status": 'TRUE',
                "code": 200,
                "mensaje": 'successfull',
                "businesses_support_into_radius": self.bussines_suport_into_radio_for_each_bussines_class.shape[0]
            }

        else:
            response = {
                "status": 'FALSE',
                "code": 505,
                "mensaje": 'unsuccessfull',
                "businesses_into_radius": 'no_iter'
            }
        return response

    def find_business_into_radius(self):
        results = []
        # Recorremos cada ue de la clase filtrada de interes
        for _, row_class_interes in self.filter_bussines_code_class_acumulated.iterrows():
            coords_class_interes = (row_class_interes['Latitud'], row_class_interes['Longitud'])
            negocios_dentro_radio = []

            # Lista para almacenar los índices de las unidades económicas encontradas
            # negocios_a_eliminar = []

            for idx_negocio, row_negocio in self.filter_bussines_code_class_support_acumulated.iterrows():
                coords_negocio = (row_negocio['Latitud'], row_negocio['Longitud'])

                # Calcular la distancia entre la clase y el otro negocio
                distancia = geodesic(coords_class_interes, coords_negocio).meters

                # Verificar si está dentro del radio
                if distancia < self.influence_radio:
                    negocios_dentro_radio.append({
                        'Negocio_de_interes': row_class_interes['Nombre_de_la_Unidad_Económica'],
                        'Radio_influencia': self.influence_radio,
                        'Negocio_vecino_encontrado': row_negocio['Nombre_de_la_Unidad_Económica'],
                        'Codigo': row_negocio['Código_de_la_clase_de_actividad_SCIAN'],
                        'Tipo': row_negocio['Nombre_de_clase_de_la_actividad'],
                        'Distancia_(m)': distancia,
                        'Longitud': row_negocio['Longitud'],
                        'Latitud': row_negocio['Latitud']
                    })
                    # Marcar el negocio encontrado para ser eliminado después
                    # negocios_a_eliminar.append(idx_negocio)

            # Eliminar las unidades económicas encontradas del dataframe
            # df_to_bucle.drop(negocios_a_eliminar, inplace=True)

            # Agregar los negocios encontrados para esta ue
            if negocios_dentro_radio:
                results.extend(negocios_dentro_radio)

        output_file = "../querys/distancias/reporte_distancias/business_suport_acumulated_into_radius.xlsx"
        df = pd.DataFrame(results)
        # eliminar negocios duplicados
        # df = df.drop_duplicates(subset='Negocio_vecino_encontrado')
        df.to_excel(output_file, index=False)
        self.bussines_suport_into_radio_for_each_bussines_class = df
        if len(df) > 0:

            response = {
                "status": 'TRUE',
                "code": 200,
                "mensaje": 'successfull',
                "businesses_support_into_radius": self.bussines_suport_into_radio_for_each_bussines_class
            }

        else:
            response = {
                "status": 'FALSE',
                "code": 505,
                "mensaje": 'unsuccessfull',
                "businesses_into_radius": 'no_iter'
            }
        return response

    # inicia mecanismo para obtener ratio de influencia de tipo de clase de actividad económica(heriberto)---------------------
    def compute_influence_ratios(self):
        print("Computing influence ratios")
        #df = pd.read_csv("crecimientoNicolasRomero.csv", encoding="iso-8859-1")

        #mymap = plt.imread("./media/map_CDNR.png")
        #BBox = ((-99.3686, -99.2670, 19.58, 19.65))

        #list_Codes_SATELLITE = [465912, 466410, 813210, 468211, 811121, 531113, 713120, 461150, 463310, 811191, 611111,
        #                        467114, 713943, 465111, 321910, 722511, 812210, 466312, 621111, 461170, 811112, 461140,
        #                        312112, 811430, 811192, 611112, 465211, 811499, 466212, 811410, 463113, 434211, 466111,
        #                        461213, 464113, 434112, 811119, 462112, 722412, 434311, 811211, 464112, 463215, 541920,
        #                        467113, 323119, 541110, 541941, 337120, 812410, 811492, 463213, 931610, 311520, 468112,
        #                        811420, 722512, 813230, 811219, 621511, 468420, 311910, 465914]

        ratios = {}

        # for code in list_Codes_SATELLITE:
        return_influence_ratio, _ = self.average_distance_for_BussinesCode()

        self.influence_radio = return_influence_ratio / 2
        self.plot_scatter_bussines_by_code()
        ratios[self.code_class] = self.influence_radio

        for key, value in ratios.items():
            print(f"{key}, {value}")

        return ratios

    def average_distance_for_BussinesCode(self):
        print("average_distance_for_BussinesCode")
        list_distances = []

        # información de los negocios filtrados por epoca señalada y codigo de clase de actividad, con su latitud y longitud.
        for _, base in self.filter_bussines_code_class_support_acumulated.iterrows():
            # se inicia una lista vacia para almacenar distancias calculadas con respecto a otros negocios
            array = []

            # The all business to comparate with the step data
            for _, row in self.filter_bussines_code_class_support_acumulated.iterrows():
                print("procesin")
                # Se checa que el negocio  no sea el mismo que el negocio base, viendo las diferencias lat. long. no == cero.
                if (base['Latitud'] - row['Latitud']) != 0 and (base['Latitud'] - row['Latitud']) != 0:
                    array.append(self.haversine(base['Latitud'], base['Longitud'], row['Latitud'], row['Longitud']))

            # la lista se ordena de menor a mayor.
            array.sort()

            # Se almacena la distancia mínima (es decir, la primera en la lista ordenada)
            list_distances.append(array[0])

        list_distances.sort()

        return sum(list_distances) / len(list_distances), list_distances
        # return list_distances[len(list_distances)//4], list_distances
        # return list_distances[0], list_distances
        # return sum(list_distances[0:len(list_distances)//4]) / (len(list_distances)//4), list_distances

    def haversine(self, lat1, lon1, lat2, lon2):
        # Convertir grados a radianes
        lat1_rad = radians(lat1)
        lon1_rad = radians(lon1)
        lat2_rad = radians(lat2)
        lon2_rad = radians(lon2)

        # Diferencias
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Fórmula de Haversine
        a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Radio de la Tierra en kilómetros
        radius = 6371.0

        # Distancia en kilómetros
        distance = radius * c
        return distance

    def plot_scatter_bussines_by_code(self):
        fig, ax = plt.subplots(figsize=(11, 8))

        #for rank, code in enumerate(code_list):
        print(" processsing ", self.code_class)
        # Filter data by CODE
        #df_filter_class = df[df['Código de la clase de actividad SCIAN'] == code]

        plt.title(self.filter_bussines_code_class_acumulated.iloc[0]['Nombre de clase de la actividad'] + "\n radio de influencia (km): " + str(self.influence_radio))
        plt.xlim(self.BBox[0], self.BBox[1])
        plt.ylim(self.BBox[2], self.BBox[3])
        plt.imshow(self.mymap, zorder=0, extent=self.BBox, aspect='equal')
        plt.scatter(self.filter_bussines_code_class_acumulated['Longitud'], self.filter_bussines_code_class_acumulated['Latitud'], zorder=1, alpha=0.71, c='g', s=10)

        ratioKmToGeo = (ax.get_xlim()[1] - ax.get_xlim()[0]) / 10.64  # ancho de latitud entre los kilometros
        for _, base in self.filter_bussines_code_class_acumulated.iterrows():
            circ = plt.Circle((base['Longitud'], base['Latitud']), ratioKmToGeo * self.influence_radio, color='maroon', alpha=0.2)
            ax.add_artist(circ)

        # plt.show()
        plt.savefig('../images_insights/plots_filter_by_code_show_plot/ratios_influence/' + str(self.code_class) + '.png')

    # termina mecanismo para obtener ratio de influencia de tipo de clase de actividad económica(heriberto)-------------
    def plot_business_into_radius_original_osc(self):
        # Cargar la imagen de fondo
        fig, ax = plt.subplots(figsize=(22, 12))

        #Plotear las unidades económicas filtradas de la clase de interes
        for idx_otros, row_f in self.filter_bussines_code_class_acumulated.iterrows():
            lat_f = row_f['Latitud']
            lon_f = row_f['Longitud']
            ax.scatter(lon_f ,lat_f, color='blue', label='BusinessClass',marker='o', s=20, alpha=0.99)
            ax.text(lon_f,lat_f,row_f['Nombre_de_la_Unidad_Económica'], fontsize=12)

        # Abrimos archivo generado de las unidades económicas base encontradas dentro del radio de influencia
        df_bussines_into_ratio = pd.read_excel('../querys/distancias/reporte_distancias/businesses_suport_acumulated_into_radius.xlsx')
        #eliminamos duplicados respecto al nombre del negocio
        df_bussines_into_ratio_clean = df_bussines_into_ratio.drop_duplicates(subset='Negocio_vecino_encontrado')
        #Plotear las unidades económicas base encontradas dentro del radio de influencia
        for idx_otros, row_f in df_bussines_into_ratio_clean.iterrows():
            lat_f = row_f['Latitud']
            lon_f = row_f['Longitud']
            ax.scatter(lon_f, lat_f, color='red', label='BusinessClass', marker='x', s=20, alpha=0.45)
            print('iterando bussines de', idx_otros)

        #graficar radio de influencia de los negocios de la clase de interes acumulada
        for idx_otros, row_nintor in self.filter_bussines_code_class_acumulated.iterrows():
            latr_otro = row_nintor['Latitud']
            lonr_otro = row_nintor['Longitud']

            circle = Circle((lonr_otro, latr_otro), radius=(self.influence_radio/1000), edgecolor='maroon', facecolor='none', linewidth=2)
            # Agregar el círculo al mapa
            ax.add_patch(circle)

        # Configurar el gráfico
        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')
        plt.title(f'Negocios dentro de un radio de {self.influence_radio} metros alrededor de la clase de actividad interesada  {self.code_class}')
        ax.set_xlim(self.BBox[0], self.BBox[1])
        ax.set_ylim(self.BBox[2], self.BBox[3])
        ax.imshow(self.mymap, zorder=0, extent=self.BBox, aspect='equal')
        plt.show()

        if len(self.filter_bussines_code_class):
            response = {
                "status": 'TRUE',
                "code": 200,
                "mensaje": 'successfull',
                "plot_businesses_into_radius": self.filter_bussines_code_class_support.shape
            }

        else:
            response = {
                "status": 'FALSE',
                "code": 505,
                "mensaje": 'unsuccessfull',
                "plot_businesses_into_radius": 'no_iter'
            }
        return response

    def plot_business_into_radius(self):
        # Cargar la imagen de fondo
        fig, ax = plt.subplots(figsize=(22, 12))

        #Plotear las unidades económicas filtradas de la clase de interes
        for idx_otros, row_f in self.filter_bussines_code_class_acumulated.iterrows():
            lat_f = row_f['Latitud']
            lon_f = row_f['Longitud']
            ax.scatter(lon_f ,lat_f, color='blue', label='BusinessClass',marker='o', s=20, alpha=0.99)

        # Abrimos archivo generado de las unidades económicas base encontradas dentro del radio de influencia
        df_bussines_into_ratio = pd.read_excel('../querys/distancias/reporte_distancias/business_suport_acumulated_into_radius.xlsx')
        #eliminamos duplicados respecto al nombre del negocio
        df_bussines_into_ratio_clean = df_bussines_into_ratio.drop_duplicates(subset='Negocio_vecino_encontrado')
        #Plotear las unidades económicas base encontradas dentro del radio de influencia
        for idx_otros, row_f in df_bussines_into_ratio_clean.iterrows():
            lat_f = row_f['Latitud']
            lon_f = row_f['Longitud']
            ax.scatter(lon_f, lat_f, color='red', label='BusinessClass', marker='x', s=20, alpha=0.45)
            print('iterando bussines de', idx_otros)

        ratioKmToGeo = (ax.get_xlim()[1]-ax.get_xlim()[0]) / 10.64 # ancho de latitud entre los kilometros
        #graficar radio de influencia de los negocios de la clase de interes acumulada
        for idx_otros, row_nintor in self.filter_bussines_code_class_acumulated.iterrows():
            circ = plt.Circle((row_nintor['Longitud'], row_nintor['Latitud']), ratioKmToGeo * self.influence_radio, color='maroon',
                              alpha=0.2)
            ax.add_artist(circ)

        # Configurar el gráfico
        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')
        plt.title(f'Negocios dentro de un radio de {self.influence_radio} metros alrededor de la clase de actividad interesada  {self.code_class}')
        ax.set_xlim(self.BBox[0], self.BBox[1])
        ax.set_ylim(self.BBox[2], self.BBox[3])
        ax.imshow(self.mymap, zorder=0, extent=self.BBox, aspect='equal')
        plt.show()
        plt.savefig('../images_insights/plots_filter_by_code_show_plot/ratios_influence/' + str(self.code_class) + '.png')

        if len(self.filter_bussines_code_class):
            response = {
                "status": 'TRUE',
                "code": 200,
                "mensaje": 'successfull',
                "plot_businesses_into_radius": self.filter_bussines_code_class_support.shape
            }

        else:
            response = {
                "status": 'FALSE',
                "code": 505,
                "mensaje": 'unsuccessfull',
                "plot_businesses_into_radius": 'no_iter'
            }
        return response

    def report_accumulated_business_support_original_osc(self):
        # Inicializamos variables y creamos el DataFrame con las columnas especificadas
        posicion_repor = 0
        dfExcel = pd.DataFrame(
            columns=['name_class_business','ratio','code_class_business'] + list(self.code_poles),
            index=range(len(self.filter_bussines_code_class_acumulated))
        )

        print("self.influence_radio :::: ", self.influence_radio)

        # Diccionario para conteo de cada código de negocio
        types_code = {code: 0 for code in self.code_poles}

        for i, base in self.filter_bussines_code_class_acumulated.iterrows():
            # Reseteamos los conteos para cada unidad económica base
            local_counts = types_code.copy()

            coords_pivote = (base['Latitud'], base['Longitud'])

            # Conteo de unidades económicas dentro del radio de influencia
            for _, iter in self.filter_bussines_code_class_support_acumulated.iterrows():
                business_code = iter['Código_de_la_clase_de_actividad_SCIAN']

                if business_code in local_counts:
                    coords_neigboor = (iter['Latitud'], iter['Longitud'])
                    distancia = geodesic(coords_pivote, coords_neigboor).meters

                    if distancia < self.influence_radio:
                        local_counts[business_code] += 1

            # Crear la fila a partir del conteo local
            print(str(base['Nombre_de_la_Unidad_Económica']), ', ', ', '.join(map(str, local_counts.values())))

            row = [base['Nombre_de_clase_de_la_actividad'],self.influence_radio,self.code_class] + list(local_counts.values())
            # Asignamos la fila en el DataFrame
            dfExcel.iloc[posicion_repor] = row
            posicion_repor += 1


        # Calcular el conteo total por columna, excluyendo las columnas 'snapTime' y 'nameBussines'
        total_counts = [len(self.filter_bussines_code_class_acumulated),self.influence_radio,self.code_class]
        total_counts.extend([dfExcel[col].sum() for col in dfExcel.columns[3:]])

        # Agregar la fila de totales al DataFrame
        dfExcel.loc[len(dfExcel)] = total_counts

        # Guardamos el DataFrame en un archivo Excel
        with pd.ExcelWriter(f'../querys/distancias/reporte_distancias/report_accumulated_bussines_support_into_ratio_class_interes_{self.code_class}.xlsx',
                            engine='xlsxwriter') as writer:
            dfExcel.to_excel(writer, sheet_name='sheet1', index=True)

        return total_counts

    def report_accumulated_business_support(self):
        # Inicializamos variables y creamos el DataFrame con las columnas especificadas
        posicion_repor = 0
        dfExcel = pd.DataFrame(
            columns=['Name_class_business','name_ue_business','ratio','code_class_business'] + list(self.code_poles),
            index=range(len(self.filter_bussines_code_class_acumulated))
        )

        print("self.influence_radio :::: ", self.influence_radio)

        # Diccionario para conteo de cada código de negocio
        types_code = {code: 0 for code in self.code_poles}

        for i, base in self.filter_bussines_code_class_acumulated.iterrows():
            # Reseteamos los conteos para cada unidad económica base
            local_counts = types_code.copy()

            #coords_pivote = (base['Latitud'], base['Longitud'])
            #business_pivote_name = base['Nombre_de_clase_de_la_actividad']
            # Conteo de unidades económicas dentro del radio de influencia
            for _, iter in self.filter_bussines_code_class_support_acumulated.iterrows():
                business_code = iter['Código_de_la_clase_de_actividad_SCIAN']

                if business_code in local_counts:
                    #coords_neigboor = (iter['Latitud'], iter['Longitud'])
                    distancia = self.haversine(base['Latitud'], base['Longitud'], iter['Latitud'], iter['Longitud'])
                    # distancia = geodesic(coords_pivote, coords_neigboor).meters

                    if distancia < self.influence_radio:
                        local_counts[business_code] += 1

            # Crear la fila a partir del conteo local
            print(str(base['Nombre_de_la_Unidad_Económica']), ', ', ', '.join(map(str, local_counts.values())))

            row = [base['Nombre_de_clase_de_la_actividad'],base['Nombre_de_la_Unidad_Económica'],self.influence_radio,self.code_class] + list(local_counts.values())
            # Asignamos la fila en el DataFrame
            dfExcel.iloc[posicion_repor] = row
            posicion_repor += 1

        # Calcular el conteo total por columna, excluyendo las columnas 'snapTime' y 'nameBussines'
        total_counts = [self.filter_bussines_code_class_acumulated['Nombre_de_clase_de_la_actividad'].iloc[1],int(len(self.filter_bussines_code_class_acumulated)),self.influence_radio,self.code_class]
        total_counts.extend([round((dfExcel[col].sum()/int(len(self.filter_bussines_code_class_acumulated))),2) for col in dfExcel.columns[4:]])

        # Agregar la fila de totales al DataFrame
        dfExcel.loc[len(dfExcel)] = total_counts

        # Guardamos el DataFrame en un archivo Excel
        with pd.ExcelWriter(f'../querys/distancias/reporte_distancias/report_accumulated_bussines_support_into_ratio_class_interes_{self.code_class}.xlsx',
                            engine='xlsxwriter') as writer:
            dfExcel.to_excel(writer, sheet_name='sheet1', index=True)

        return total_counts

    def graficar_scatter(self, valores, name_satellite, code_satellite, name_base, code_base, ri, media, dir_dst):
        eje_x = range(len(valores))

        plt.scatter(eje_x, valores)

        plt.xlabel('No. UE ' + name_satellite)
        plt.ylabel('#Frecuencia \n' + name_base)
        plt.title(str(code_satellite) + " vs " + str(code_base) + "\n radio influencia (km): " + str(round(ri, 2)))

        plt.axhline(y=media, color='r', linestyle='--', label=f'media: ' + str(round(media, 1)))
        plt.legend()  # Agrega una leyenda para la línea

        # Guardamos la gráfica como imagen
        plt.savefig(dir_dst + str(code_satellite) + "_" + str(code_base) + ".png")

        # Opcionalmente, puedes mostrar la gráfica
        # plt.show()
        plt.clf()
def main():
    df = pd.read_csv("../querys/crecimientoNicolasRomero.csv")
    code_class = 311520

    time_window = 3
    bussines_snapshot = Recomender(df, code_class, time_window)
    print("*filter_by_code_show_plot:*\n", bussines_snapshot.filter_by_code_show_plot())
    print("*filter_by_code_acumulated_show_plot:*\n", bussines_snapshot.filter_by_code_acumulated_show_plot())
    print("*filter_by_code_support_show_plot:*\n", bussines_snapshot.filter_by_code_support_show_plot())
    #print("*filter_by_code_support_acumulated_show_plot:*\n", bussines_snapshot.filter_by_code_support_acumulated_show_plot())
    print('*show_distances_for_each_bussines_in_code_class:\n',bussines_snapshot.show_distances_for_each_business())
    #print('*find_businesses_into_radius_for_each_code_class:\n',bussines_snapshot.find_business_into_radius())
    #print('*plot_businesses_into_radius_for_each_code_class:\n',bussines_snapshot.plot_business_into_radius())
    print('report_accumulated_bussines_support',bussines_snapshot.report_accumulated_business_support())
    return 1

#creamos main
if __name__ == "__main__":
    main()