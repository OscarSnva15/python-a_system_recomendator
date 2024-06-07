import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap

def main_():
    # Leemos nuestro data frame con las coordenadas adecuadas del espacio
    df = pd.read_excel("../querys/POBLACION_URBANA_NICOLAS_ROMERO2020.xlsx")

    # Cargamos nuestra imagen del mapa
    mymap = plt.imread("../media/map_CDNR.png")

    # Definimos dimensiones adecuadas a nuestro espacio visual de coordenadas
    BBox = ((-99.3686, -99.2670, 19.58, 19.65))

    # Crear una figura y un eje
    fig, ax = plt.subplots(figsize=(10, 10))

    # Mostrar la imagen del mapa
    ax.imshow(mymap, zorder=0, extent=BBox, aspect='equal')

    # Enviar datos para convertir

    # Crear el mapa de calor
    sns.kdeplot(
        x=df['longitud_decimal_x'], y=df['latitud_decimal_y'], weights=df['Poblacion_total'],
        cmap="Reds", fill=True, thresh=0, levels=100, alpha=0.6, ax=ax
    )

    # Añadir etiquetas y título
    ax.set_xlabel('Longitud')
    ax.set_ylabel('Latitud')
    ax.set_title('Mapa de calor sobre la Densidad de la población en el Municipio de Nicolás Romero para el Año 2020')

    plt.show()

def main__():
    # Leemos nuestro data frame con las coordenadas adecuadas del espacio
    df = pd.read_excel("../querys/POBLACION_URBANA_NICOLAS_ROMERO2020.xlsx")

    # Cargamos nuestra imagen del mapa
    mymap = plt.imread("../media/nicolasromero_denotado_y_con_vecinos.png")

    # Definimos dimensiones adecuadas a nuestro espacio visual de coordenadas
    #https://www.openstreetmap.org/export#map=12/19.5802/-99.2570
    #coordenadas primero x1 y luego x2 de iz a drcha. como aparece el exportador
    # coordenadas primero y1 y luego y2 de abajo hacia arriba. como aparece el exportador
    BBox = ((-99.5409, -99.0280, 19.4141, 19.7570))

    #definimos colores
    color = 'r'

    #definimos titulo
    title = 'Mapa de calor sobre la Densidad de la población en Nicolás Romero, Comparado con sus Mpos. circunvecinos'

    #traemos el subplots
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(26, 10))

    ax.set_title(title)
    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])
    ax.imshow(mymap, zorder=0, extent=BBox, aspect='equal')

    sns.kdeplot(
        x=df['Longitud x'], y=df['Latitud y'], weights=df['Poblacion'],
        cmap="Reds", fill=True, thresh=0, levels=100, alpha=0.6, ax=ax
    )
    plt.show()

def main():
    # Leemos nuestro data frame con las coordenadas adecuadas del espacio
    df = pd.read_excel("../querys/POBLACION_URBANA_NICOLAS_ROMERO2020.xlsx")
    # Crear un mapa centrado en el promedio de las coordenadas
    mapa = folium.Map(location=[df['Latitud y'].mean(), df['Longitud x'].mean()], zoom_start=5)
    # Preparar los datos para HeatMap
    # HeatMap requiere una lista de listas con formato [latitud, longitud, peso]
    heat_data = [[row['Latitud y'], row['Longitud x'], row['Poblacion']] for index, row in df.iterrows()]

    # Añadir la capa de calor al mapa
    HeatMap(heat_data).add_to(mapa)

    # Guardar el mapa en un archivo HTML
    mapa.save('mapa_de_calor.html')

if __name__ == "__main__":
    main()