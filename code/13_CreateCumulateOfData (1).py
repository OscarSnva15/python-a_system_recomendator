from cgi import print_form
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
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

def plot_scatter_bussines_acumulated(df, BBox, mymap, code = 311812, target_location=[19.599472210151948, -99.30688849000485]):
    # Filter data by CODE
    df_filter_class = df[ df['Código_de_la_clase_de_actividad_SCIAN'] ==  code]
    df_filter_class_snaptime = []
    # Filter data by DATE
    df_filter_class_snaptime.append( df_filter_class[ df_filter_class['Fecha_de_incorporacion_al_DENUE'] < '2014-12' ] )
    df_filter_class_snaptime.append( df_filter_class[ (df['Fecha_de_incorporacion_al_DENUE'] >= '2014-12')  & \
                                                        (df['Fecha_de_incorporacion_al_DENUE'] < '2019-11') ] )
    df_filter_class_snaptime.append( df_filter_class[ df_filter_class['Fecha_de_incorporacion_al_DENUE']>= '2019-11' ] )

    color = [ 'r', 'g', 'b' ]
    title = ["Fecha Nacimiento < 2014-12", "Fecha Nacimiento < 2019-11","Fecha Nacimiento< 2022-05"]

    fig, ax = plt.subplots(nrows = 1, ncols= 3, figsize = (26,10))

    latit, longit = target_location[0],  target_location[1]

    df_filter_class_location = []
    for snapshot_time in df_filter_class_snaptime:
        df_filter_location_code = pd.DataFrame()
        # Filter data by NEIGHBORHOOD
        df_filter_class_location.append( snapshot_time[ snapshot_time.apply(lambda x: distance(x['Latitud'], latit, x['Longitud'], longit) < 0.250, axis=1) ]   ) 

    for i in range(3):
        ax[i].set_title(title[i])
        ax[i].set_xlim(BBox[0],BBox[1])
        ax[i].set_ylim(BBox[2],BBox[3])
        ax[i].imshow(mymap, zorder=0, extent = BBox, aspect = 'equal')
        for j in range(i+1):
            ax[i].scatter(df_filter_class_location[j]['Longitud'], df_filter_class_location[j]['Latitud'], zorder=1, alpha= 0.71, c=color[j], s=10)

        plt.savefig('./images_insights/'+str(code)+'.png')


def plot_scatter_bussines_by_code(df, BBox, mymap, code_list  ):
    color=iter(cm.rainbow(np.linspace(0,1,20)))
    c=next(color)

    # __code_list = df['Código_de_la_clase_de_actividad_SCIAN'].unique()
    # code_list = __code_list[0:10]
    # print(code_list)


    for rank, code in enumerate(code_list):
        print(" processsing ", code )
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

        fig, ax = plt.subplots(nrows = 1, ncols= 3, figsize = (24,6))
        
        fig.suptitle(df_filter_class.iloc[0]['Nombre_de_clase_de_la_actividad'], fontsize="x-large")
        
        for i in range(3):
            ax[i].set_title(title[i])
            ax[i].set_xlim(BBox[0],BBox[1])
            ax[i].set_ylim(BBox[2],BBox[3])
            ax[i].imshow(mymap, zorder=0, extent = BBox, aspect = 'equal')
            for j in range(i+1):
                ax[i].scatter(df_filter_class_snaptime[j]['Longitud'], df_filter_class_snaptime[j]['Latitud'], zorder=1, alpha= 0.71, c=c, s=10)

        plt.savefig('./images_insights/test/' + "{:03d}".format(rank) + '_' + str(code)+'.png')
        plt.clf()

def main():
    df = pd.read_csv("./querys/crecimientoNicolasRomero.csv")
    mymap = plt.imread("./media/map_CDNR.png")
    BBox = ((-99.3686, -99.2670, 19.58, 19.65))

    # target_location = [19.599472210151948, -99.30688849000485]
    # plot_scatter_bussines_acumulated( df, BBox, mymap, 461110, target_location )
    class_1 = [461110, 465311, 311830, 467111, 461122, 311812 ] 
    class_2 = [ 812110, 461121, 461130, 811111, 468211, 811191, 312112, 811492, 221312, 485111,464111 ]
    class_test = [ 
        461110	,
        465311	,
        812110	,
        463211	,
        722513	,
        461122	,
        461160	,
        722514	,
        461130	,
        311812	,
        467111	,
        311830	,
        722517	,
        467115	,
        561432	,
        722518	,
        464111	,
        461121	,
        811111	,
        722519	,
        722515	,
        621211	,
        332320	,
        461190	,
        465912	,
        466410	,
        713120	,
        531113	,
        811121	,
        813210	,
        468211	,
        461150	,
        811191	,
        463310	,
        713943	,
        321910	,
        465111	,
        722511	,
        467114	,
        466312	,
        611111	,
        812210	,
        621111	,
        461170	,
        811192	,
        811112	,
        461140	,
        312112	,
        465211	,
        811499	,
        811430	,
        466212	,
        461213	,
        811410	,
        464113	,
        722412	,
        466111	,
        434211	,
        434311	,
        611112	,
        434112	,
        463113	,
        462112	,
        464112	,
        811119	,
        463215	,
        811211	,
        541920	,
        541110	,
        323119	,
        467113	,
        811492	,
        337120	,
        812410	,
        463213	,
        813230	,
        931610	,
        468112	,
        811219	,
        811420	,
        541941	,
        311520	,
        722512	,
        621398	,
        311910	,
        812130	,
        621511	,
        532282	,
        611621	,
        468420	,
        811491	,
        465914	,
        466114	,
        465212	,
        812990	,
        464121	,
        811493	,
        463212	,
        811312	,
        461212	,
        811199	,
        465215	,
        811115	,
        812310	,
        465911	,
        621311	,
        468311	,
        332710	,
        624191	,
        465915	,
        621331	,
        315225	,
        434314	,
        327330	,
        611122	,
        621320	,
        468412	,
        541211	,
        463216	,
        461211	,
        931210	,
        315223	,
        811114	,
        434312	,
        465313	,
        112512	,
        611611	,
        522452	,
        811129	,
        465112	,
        434224	,
        434319	,
        339999	,
        468213	,
        611691	,
        621113	,
        466319	,
        624411	,
        811116	,
        713991	,
        434221	,
        465919	,
        466112	,
        611121	,
        611182	,
        434225	,
        467112	,
        532281	,
        463112	,
        466211	,
        435319	,
        314991	,
        434229	,
        315229	,
        722516	,
        463217	,
        611511	,
        463214	,
        532411	,
        713998	,
        221312	,
        931410	,
        466311	,
        621341	,
        332310	,
        532493	,
        721113	,
        811113	,
        221311	,
        238210	,
        463111	,
        337110	,
        611171	,
        461123	
    ]
    plot_scatter_bussines_by_code( df, BBox, mymap, class_test )

    # plt.show()

    # for i, code in enumerate(class_test):
    #     print( "{:03d}".format(i), " ", code)

if __name__ == "__main__":
    main()