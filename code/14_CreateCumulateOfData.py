from cgi import print_form
import numpy as np
from scipy.spatial import cKDTree
import pandas as pd
import matplotlib.pyplot as plt
from math import dist, radians, cos, sin, asin, sqrt
from dataclasses import dataclass
import itertools

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


from scipy.spatial import cKDTree


def plot_scatter_bussines_acumulated(df, BBox, mymap, codes=[812110]):
    # Definir los colores para diferentes códigos
    color_map = ['r', 'g', 'b']  # Agregar más colores si es necesario

    # Títulos para las diferentes secciones del tiempo
    title = ["Fecha Nacimiento < 2014-12"]

    # Crear el gráfico con un tamaño grande
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(30, 12))

    #for i in range(1):
    ax.set_title('Fecha Nacimiento < 2014-12')
    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])
    ax.imshow(mymap, zorder=0, extent=BBox, aspect='equal')

    # Iterar sobre cada código y añadir los puntos al gráfico
    for idx, code in enumerate(codes):
        df_filter_class = df[df['Código_de_la_clase_de_actividad_SCIAN'] == code]

        # Filtrar los datos según el tiempo
        df_filter_class_snaptime = []
        df_filter_class_snaptime.append(
            df_filter_class[df_filter_class['Fecha_de_incorporacion_al_DENUE'] < '2014-12'])


        # Ploteo de los puntos para cada intervalo de tiempo y código
        for j in range(1):
            longitud = df_filter_class_snaptime[j]['Longitud'].values
            latitud = df_filter_class_snaptime[j]['Latitud'].values

            # Ploteo de los puntos
            ax.scatter(longitud, latitud, zorder=1, alpha=0.71, c=color_map[j], s=10,
                          label=f'Código {code}' if j == 0 else "")

            # Encontrar el vecino más cercano y dibujar las líneas
            if len(longitud) > 1:  # Para evitar errores en caso de un solo punto
                points = list(zip(longitud, latitud))
                tree = cKDTree(points)
                distances, indices = tree.query(points, k=len(points))

                # Simular las distancias desde un solo punto de interés (por ejemplo, el primero)
                point_idx = 0  # Puedes cambiar este valor para seleccionar otro punto
                point = points[point_idx]

                min_dist = np.inf
                min_neighbor_idx = None

                for k in range(1, len(points)):
                    neighbor_idx = indices[point_idx][k]  # Índice del vecino
                    dist_to_neighbor = distances[point_idx][k]

                    # Dibujar todas las líneas de distancia
                    ax.plot([longitud[point_idx], longitud[neighbor_idx]],
                               [latitud[point_idx], latitud[neighbor_idx]],
                               color='black', linewidth=0.5, alpha=0.7)

                    # Identificar la distancia mínima
                    if dist_to_neighbor < min_dist:
                        min_dist = dist_to_neighbor
                        min_neighbor_idx = neighbor_idx

                # Resaltar la línea con la distancia más corta
                if min_neighbor_idx is not None:
                    ax.plot([longitud[point_idx], longitud[min_neighbor_idx]],
                               [latitud[point_idx], latitud[min_neighbor_idx]],
                               color='yellow', linewidth=5, alpha=1)

    plt.suptitle(f'Comercio al por menor de ropa, excepto de bebé y lencería', fontsize=16)
    plt.savefig('../images_insights/codigos_acumulados.png')
    plt.show()

def main():

    df = pd.read_csv("../querys/crecimientoNicolasRomero.csv")
    mymap = plt.imread("../media/map_CDNR.png")
    BBox = ((-99.3686, -99.2670, 19.58, 19.65))
    # Lista de códigos a procesar
    lista_codigos = [463211]
    plot_scatter_bussines_acumulated( df, BBox, mymap, lista_codigos)
    plt.show()

if __name__ == "__main__":
    main()