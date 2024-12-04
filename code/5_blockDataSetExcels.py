from cgi import print_form
import code
from codecs import latin_1_encode
from csv import writer
from dataclasses import dataclass
from math import dist, radians, cos, sin, asin, sqrt, atan2
from pickle import LIST
from unittest.util import three_way_cmp
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
from dataclasses import dataclass

from psutil import users
#this code can be improve, to algoritmo neihbohord
def distance(lat1, lat2, lon1, lon2):
        # The math module contains a function named radians which converts from degrees to radians.
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

def haversine(lat1, lon1, lat2, lon2):
    # Convertir grados a radianes
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Diferencias
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Fórmula de Haversine
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Radio de la Tierra en kilómetros
    radius = 6371.0

    # Distancia en kilómetros
    distance = radius * c
    return distance

#created a data class
@dataclass 
class data_business_filter:
    #attribute declaration
    code_bussines : list
    epoch : int
    filter_bussines : pd.DataFrame
    df_complete : pd.DataFrame
    bussines_neighborhood_acc : dict
    influence_radio : float
    influence_radio_2 : float
    intradistances_target_bussines : pd.DataFrame
    accumulated_neighborhood_bussines : dict
    code_poles : set

    #Attribute initialization by calling the INIT method, instantiating the class at the same time.
    def __init__(self, df, code_bussines, epoch ):
        self.code_bussines = code_bussines
        self.epoch = epoch
        self.df_complete = df
        self.filter_bussines = self.__filter_by_code()
        self.bussines_neighborhood_acc = self.__get_bussines_neighborhood_acc()

    #This Method helps show the count of microbusinesses at the required time by epoch.(retorna el DataFrame filtrado del último código procesado)
    def __filter_by_code(self):
        # snaptime overview data
        for code in self.code_bussines:
            print("codes:", code)
            df_filter_general = self.df_complete[self.df_complete['Código_de_la_clase_de_actividad_SCIAN'] == code]
            # snaptime windows df
            filtered = None
            # apply filter time on overview data
            if self.epoch == 0:
                filtered = df_filter_general[df_filter_general['Fecha_de_incorporacion_al_DENUE'] < '2014-12']
            elif self.epoch == 1:
                # filtered =  df_filter_general[(df_filter_general['Fecha_de_incorporacion_al_DENUE'] >= '2014-12') & (df_filter_general['Fecha_de_incorporacion_al_DENUE'] < '2019-11') ]
                filtered = df_filter_general[df_filter_general['Fecha_de_incorporacion_al_DENUE'] < '2019-11']
            elif self.epoch == 2:
                # filtered =  df_filter_general[ df_filter_general['Fecha_de_incorporacion_al_DENUE'] >= '2019-11' ]
                filtered = df_filter_general
            else:
                filtered = df_filter_general
            print("epoch", self.epoch, "  TOTAL CODE-BUSSINESS FOUND: ", len(filtered))
        return filtered

    #This method obtains the mode and statistical mean of distance between the two specified types of microbusinesses established by epoch.
    def __get_bussines_neighborhood_acc(self):
        #obtain the dataframe that have data abouth  and dataframe class business, The function calculates the minimum distance between each business and the other businesses in the filtered set
        self.intradistances_target_bussines = self.__get_average_distance_for_BussinesCode()

        self.influence_radio_2 = float(self.intradistances_target_bussines.mode().mean().iloc[0]) / 2
        self.influence_radio = float(self.intradistances_target_bussines.mean().iloc[0]) / 2

        print("self.influence_radio mode mean (mediana de la moda estadistica): ", self.influence_radio_2)
        print("self.influence_radio mean (media estadistica): ", self.influence_radio)

        self.__set_code_poles()
        types_code = {}
        for code in self.code_poles:
            types_code[code] = 0

        return types_code

    #This method obtains the distances between two specified type of microbussines established and found in method "__filter_by_code" by epoch of time.
    def __get_average_distance_for_BussinesCode(self):
        list_distances = []

        #información de los negocios filtrados por epoca señalada y codigo de clase de actividad, con su latitud y longitud.
        for _, base in self.filter_bussines.iterrows():
            #se inicia una lista vacia para almacenar distancias calculadas con respecto a otros negocios
            array = []

            #The all business to comparate with the step data
            for _, row in self.filter_bussines.iterrows():

                #Se checa que el negocio  no sea el mismo que el negocio base, viendo las diferencias lat. long. no == cero.
                if (base['Latitud'] - row['Latitud'])!=0 and (base['Latitud'] - row['Latitud'])!=0:
                    # dlat = base['Latitud'] - row['Latitud']
                    # dlong = base['Longitud'] - row['Longitud']
                    # array.append(  sqrt( dlat**2 + dlong**2 ) )

                    #Si las coordenadas son diferentes, se calcula una "distancia" (no euclidiana)
                    array.append( max(abs(base['Latitud'] - row['Latitud']), abs(base['Longitud'] - row['Longitud'])))

            #la lista se ordena de menor a mayor.
            array.sort()
            #Se almacena la distancia mínima (es decir, la primera en la lista ordenada)
            list_distances.append(array[0])

        #Una vez calculadas las distancias mínimas para cada negocio, se crean un DataFrame
        df_distances = pd.DataFrame(list_distances, columns = ['Distances_Totals_Between_BusinessTypeClass'])

        # ploter histograma of datafram distances
        # plt.hist(list_distances, bins=40)
        # plt.show()
        ##add this oscar, ploter histograma of datafram distances
        plt.hist(list_distances, bins=40)
        plt.xlabel('Distancias minimas')
        plt.ylabel('Frecuencia')
        plt.show()


        return  df_distances

    #We define the set of codes belonging to a type of activity that a microbusiness manages
    def __set_code_poles(self):
            # self.code_poles = ( 311520, 311812, 311830, 311910, 312112, 321910, 323119, 332320, 337120, 434112, 434211, 434311, 461110, 461121, 461122, 461130, 461140, 461150, 461160, 461170, 461190, 461213, 462112, 463113, 463211, 463213, 463215, 463310, 464111, 464112, 464113, 465111, 465211, 465311, 465912, 466111, 466212, 466312, 466410, 467111, 467113, 467114, 467115, 468112, 468211, 468420, 531113, 532282, 541110, 541920, 541941, 561432, 611111, 611112, 611621, 621111, 621211, 621398, 621511, 713120, 713943, 722412, 722511, 722512, 722513, 722514, 722515, 722517, 722518, 722519, 811111, 811112, 811119, 811121, 811191, 811192, 811211, 811219, 811410, 811420, 811430, 811492, 811499, 812110, 812130, 812210, 812410, 813210, 813230, 931610)
            self.code_poles = (461110, 465311, 812110, 463211, 722513, 461122, 461160, 722514, 461130, 311812, 467111, 311830, 722517, 467115, 561432, 722518, 464111, 461121, 811111, 722519, 722515, 621211, 332320, 461190, 465912, 466410, 713120, 531113, 811121, 813210, 468211, 461150, 811191, 463310, 713943, 321910, 465111, 722511, 467114, 466312, 611111, 812210, 621111, 461170, 811192, 811112, 461140, 312112, 465211, 811499, 811430, 466212, 461213, 811410, 464113, 722412, 466111, 434211, 434311, 611112, 434112, 463113, 462112, 464112, 811119, 463215, 811211, 541920, 541110, 323119, 467113, 811492, 337120, 812410, 463213, 813230, 931610, 468112, 811219, 811420, 541941, 311520, 722512, 621398, 311910, 812130, 621511, 532282, 611621, 468420)

    def report_accumulated_bussines_support(self):
        Latitud = []
        Longitud = []
        posicion = 0
        ListColumns  = []
        averageList = []
        # dfExcel = pd.DataFrame(columns = ['snapTime','nameBussines','311520','311812','311830','311910','312112','321910','323119','332320','337120','434112','434211','434311','461110','461121','461122','461130','461140','461150','461160','461170','461190','461213','462112','463113','463211','463213','463215','463310','464111','464112','464113','465111','465211','465311','465912','466111','466212','466312','466410','467111','467113','467114','467115','468112','468211','468420','531113','532282','541110','541920','541941','561432','611111','611112','611621','621111','621211','621398','621511','713120','713943','722412','722511','722512','722513','722514','722515','722517','722518','722519','811111','811112','811119','811121','811191','811192','811211','811219','811410','811420','811430','811492','811499','812110','812130','812210','812410','813210','813230','931610'], index=range(12))
        dfExcel = pd.DataFrame(columns = ['snapTime','nameBussines', '461110', '465311', '812110', '463211', '722513', '461122', '461160', '722514', '461130', '311812', '467111', '311830', '722517', '467115', '561432', '722518', '464111', '461121', '811111', '722519', '722515', '621211', '332320', '461190', '465912', '466410', '713120', '531113', '811121', '813210', '468211', '461150', '811191', '463310', '713943', '321910', '465111', '722511', '467114', '466312', '611111', '812210', '621111', '461170', '811192', '811112', '461140', '312112', '465211', '811499', '811430', '466212', '461213', '811410', '464113', '722412', '466111', '434211', '434311', '611112', '434112', '463113', '462112', '464112', '811119', '463215', '811211', '541920', '541110', '323119', '467113', '811492', '337120', '812410', '463213', '813230', '931610', '468112', '811219', '811420', '541941', '311520', '722512', '621398', '311910', '812130', '621511', '532282', '611621', '468420' ], index=range(len(self.filter_bussines)))
        print( "self.influence_radio :::: ",self.influence_radio)
        for i, base in self.filter_bussines.iterrows():
            types_code = self.bussines_neighborhood_acc.copy()
            for _, iter in self.df_complete.iterrows():
                if iter['Código_de_la_clase_de_actividad_SCIAN'] in types_code.keys():
                    dlat  = iter['Latitud'] - base['Latitud']
                    dlong = iter['Longitud']-base['Longitud']
                    # if abs((iter['Latitud'] - base['Latitud'])) < self.influence_radio  and \
                    #     abs((iter['Longitud']-base['Longitud'])) < self.influence_radio:
                    if sqrt(dlat**2 + dlong**2) < self.influence_radio:
                            types_code[iter['Código_de_la_clase_de_actividad_SCIAN']] +=  1
                            Latitud.append(iter['Latitud'])
                            Longitud.append(iter['Longitud'])
                            code = list(types_code.values())
            print(base['Nombre_de_la_Unidad_Económica'],', ', ', '.join(map(str,code)))
            temp = [ self.epoch, str(base['Nombre_de_la_Unidad_Económica']) ]
            temp.extend( code )
            dfExcel.iloc[posicion] = tuple( temp )
            posicion = posicion + 1
        #we obtain average for each columns
        ListColumns = dfExcel.columns
        for x in ListColumns:
            if x != 'snapTime' and x !='nameBussines':
                averageList.append(dfExcel[x].mean())
        averageList.insert(0,"")
        averageList.insert(1,"Promedio")
        dfExcel.loc[len(dfExcel)] = averageList
        
        writer = pd.ExcelWriter('../querys/dataExceLCreated/pruebaUno.xlsx', engine='xlsxwriter')
        dfExcel.to_excel(writer, sheet_name='sheet1', index = True)
        writer.close()
        self.plot_escenary(Latitud, Longitud)
        return

    def plot_escenary(self, lat, long):
        fig, ax = plt.subplots(figsize = (22,12))
        ax.scatter(self.filter_bussines.Longitud, self.filter_bussines.Latitud, zorder=1, alpha= 0.4, c='r', s=10)
        mymap = plt.imread("../media/map_CDNR.png")
        BBox = ((-99.3686, -99.2670, 19.58, 19.65))

        x_values = [(BBox[0]+BBox[1])/2, (BBox[0]+BBox[1])/2 + self.influence_radio]
        y_values = [(BBox[3]+BBox[2])/2, (BBox[3]+BBox[2])/2  ]
        ax.plot(x_values, y_values, c='b')

        x_values = [(BBox[0]+BBox[1])/2, (BBox[0]+BBox[1])/2 ]
        y_values = [(BBox[3]+BBox[2])/2, (BBox[3]+BBox[2])/2 + + self.influence_radio_2 ]
        ax.plot(x_values, y_values, c='r')


        ax.scatter(self.filter_bussines.Longitud, self.filter_bussines.Latitud, alpha= 0.4, facecolor='maroon', s=int(self.influence_radio*1450000))

        ax.scatter(long, lat, zorder=1, alpha= 0.4, c='b', s=10)

        ax.set_title('Plotting Spatial Data on Map')
        ax.set_xlim(BBox[0],BBox[1])
        ax.set_ylim(BBox[2],BBox[3])
        ax.imshow(mymap, zorder=0, extent = BBox, aspect = 'equal')
        plt.show()



def plot_scatter_bussines_by_code(df, BBox, mymap, code_list, influence_ratio, dir_dst ):
    fig, ax = plt.subplots(figsize=(11, 8))

    for rank, code in enumerate(code_list):
        print(" processsing ", code )
        # Filter data by CODE
        df_filter_class = df[ df['Código_de_la_clase_de_actividad_SCIAN'] ==  code]


        plt.title( df_filter_class.iloc[0]['Nombre_de_clase_de_la_actividad'] + "\n radio de influencia (km): " + str(influence_ratio))
        plt.xlim(BBox[0],BBox[1])
        plt.ylim(BBox[2],BBox[3])
        plt.imshow(mymap, zorder=0, extent = BBox, aspect = 'equal')
        plt.scatter(df_filter_class['Longitud'], df_filter_class['Latitud'], zorder=1, alpha= 0.71, c='g', s=10)

        ratioKmToGeo = (ax.get_xlim()[1]-ax.get_xlim()[0]) / 10.64 # ancho de latitud entre los kilometros
        for _, base in df_filter_class.iterrows():
            circ = plt.Circle( (base['Longitud'],base['Latitud'] ),  ratioKmToGeo*influence_ratio , color='maroon', alpha=0.2)
            ax.add_artist(circ)

        #plt.show()
        plt.savefig(dir_dst+str(code)+'.png')

def average_distance_for_BussinesCode(df):
    list_distances = []
    print('average_distance_for_BussinesCode')
    #información de los negocios filtrados por epoca señalada y codigo de clase de actividad, con su latitud y longitud.
    for _, base in df.iterrows():
        #se inicia una lista vacia para almacenar distancias calculadas con respecto a otros negocios
        array = []

        #The all business to comparate with the step data
        for _, row in df.iterrows():

            #Se checa que el negocio  no sea el mismo que el negocio base, viendo las diferencias lat. long. no == cero.
            if (base['Latitud'] - row['Latitud'])!=0 and (base['Latitud'] - row['Latitud'])!=0:
                array.append(  haversine( base['Latitud'], base['Longitud'], row['Latitud'], row['Longitud'] ) )

        #la lista se ordena de menor a mayor.
        array.sort()

        #Se almacena la distancia mínima (es decir, la primera en la lista ordenada)
        list_distances.append(array[0])
        
    list_distances.sort()
    print('ends average_distance_for_BussinesCode')
    return sum(list_distances)/len(list_distances), list_distances
    #return list_distances[len(list_distances)//4], list_distances
    #return list_distances[0], list_distances
    #return sum(list_distances[0:len(list_distances)//4]) / (len(list_distances)//4), list_distances


def compute_influence_ratios( ):
    df = pd.read_csv("../querys/crecimientoNicolasRomero.csv")

    mymap = plt.imread("../media/map_CDNR.png")
    BBox = ((-99.3686, -99.2670, 19.58, 19.65))

    list_Codes_SATELLITE = [468211]
    
    ratios = { }

    for code in list_Codes_SATELLITE:
        print('code in list_Codes_SATELLITE')
        influence_ratio, _ = average_distance_for_BussinesCode( df[ df['Código_de_la_clase_de_actividad_SCIAN'] ==  code])
        influence_ratio = influence_ratio/2
        plot_scatter_bussines_by_code(df, BBox, mymap, [code], influence_ratio, '../ratios_influence/')
        ratios[ code ] = influence_ratio
    print('key, value in ratios.items()')
    for key, value in ratios.items():
        print(f"{key}, {value}")

    return ratios


def graficar_scatter(valores, name_satellite, code_satellite, name_base, code_base, ri, media, dir_dst ):
    eje_x = range(len(valores))
    
    plt.scatter(eje_x, valores)
    
    plt.xlabel('No. UE ' + name_satellite)
    plt.ylabel('#Frecuencia \n'+ name_base)
    plt.title( str(code_satellite) + " vs " + str(code_base)+"\n radio influencia (km): "+ str( round(ri,2)) )
    
    plt.axhline(y=media, color='r', linestyle='--', label=f'media: '+str( round(media,1)))
    plt.legend()  # Agrega una leyenda para la línea

    # Guardamos la gráfica como imagen
    plt.savefig(dir_dst+ str(code_satellite) + "_" + str(code_base)+ ".png")
    
    # Opcionalmente, puedes mostrar la gráfica
    #plt.show()
    plt.clf() 


def generate_table_medias():
    df = pd.read_csv("crecimientoNicolasRomero.csv",encoding="iso-8859-1")
    df_complete = df[  ['Código de la clase de actividad SCIAN', 'Latitud', 'Longitud', 'Nombre de clase de la actividad'] ]
    
    code2name  = df.set_index('Código de la clase de actividad SCIAN')['Nombre de clase de la actividad'].to_dict()
    del df

    list_Codes_SATELLITE = [ 465912, 466410, 813210, 468211, 811121, 531113, 713120, 461150, 463310, 811191, 611111, 467114, 713943, 465111, 321910, 722511, 812210, 466312, 621111, 461170, 811112, 461140, 312112, 811430, 811192, 611112, 465211, 811499, 466212, 811410, 463113, 434211, 466111, 461213, 464113, 434112, 811119, 462112, 722412, 434311, 811211, 464112, 463215, 541920, 467113, 323119, 541110, 541941, 337120, 812410, 811492, 463213, 931610, 311520, 468112, 811420, 722512, 813230, 811219, 621511, 468420, 311910, 465914]
    list_Codes_BASE = [461110, 465311, 812110, 463211, 461122, 722513, 461160, 467111, 311830, 461130, 722514, 311812, 461121, 464111, 722517, 561432, 467115, 722518, 811111, 722515, 722519, 621211, 332320, 461190 ]
    ratio_influence_SATELLITE = { 465912 : 0.121126344, 466410 : 0.12752349, 813210 : 0.163361379, 468211 : 0.099962165, 811121 : 0.157266395, 531113 : 0.144464962, 713120 : 0.150989829, 461150 : 0.166928025, 463310 : 0.097882493, 811191 : 0.214959794, 611111 : 0.185657038, 467114 : 0.201398088, 713943 : 0.154197849, 465111 : 0.210970494, 321910 : 0.221392644, 722511 : 0.127702353, 812210 : 0.1649506, 466312 : 0.188739827, 621111 : 0.170418864, 461170 : 0.172570689, 811112 : 0.248902659, 461140 : 0.242521817, 312112 : 0.28876988, 811430 : 0.255405019, 811192 : 0.219373273, 611112 : 0.302974674, 465211 : 0.142577109, 811499 : 0.196457891, 466212 : 0.083315844, 811410 : 0.266078754, 463113 : 0.240934112, 434211 : 0.205423727, 466111 : 0.279897263, 461213 : 0.294931482, 464113 : 0.23574913, 434112 : 0.216485951, 811119 : 0.228313805, 462112 : 0.254092545, 722412 : 0.149439043, 434311 : 0.296791918, 811211 : 0.245884804, 464112 : 0.283661328, 463215 : 0.291303877, 541920 : 0.234342586, 467113 : 0.294552405, 323119 : 0.264497231, 541110 : 0.130691374, 541941 : 0.262354962, 337120 : 0.381125224, 812410 : 0.150702616, 811492 : 0.37516341, 463213 : 0.292623173, 931610 : 0.285965711, 311520 : 0.255348256, 468112 : 0.154848176, 811420 : 0.288078314, 722512 : 0.235491623, 813230 : 0.354325492, 811219 : 0.266988038, 621511 : 0.297904553, 468420 : 0.426459679, 311910 : 0.183169631, 465914 : 0.415535121 }

    df_UEs_BASE = df_complete[ df_complete['Código de la clase de actividad SCIAN'].isin( list_Codes_BASE ) ]
    df_UEs_SATELLITE = df_complete[ df_complete['Código de la clase de actividad SCIAN'].isin( list_Codes_SATELLITE ) ]

    print("\t",end=",")
    for c in list_Codes_BASE[:-1]:
        print(c,end=",  ")
    print(list_Codes_BASE[-1],"\n")

    for code_satellite_X in list_Codes_SATELLITE:

        df_UE_SATELLITE_with_code_X = df_UEs_SATELLITE[ df_UEs_SATELLITE['Código de la clase de actividad SCIAN'] ==  code_satellite_X ]
        ratio_influence = ratio_influence_SATELLITE[ code_satellite_X ]

        print( code_satellite_X, end=",  ")
        
        for code_base_Y in list_Codes_BASE:
            
            df_UE_BASE_with_code_Y = df_UEs_BASE[ df_UEs_BASE['Código de la clase de actividad SCIAN'] ==  code_base_Y ]

            num_UEs_BASE_in_ratio_influence_by_UE_SATELLITE_XY = []
            for _, ue_satellite in df_UE_SATELLITE_with_code_X.iterrows():
                count = 0
                for _, ue_base in df_UE_BASE_with_code_Y.iterrows():
                    if haversine( ue_satellite['Latitud'],ue_satellite['Longitud'], ue_base['Latitud'], ue_base['Longitud'] ) < ratio_influence:
                        count += 1
                num_UEs_BASE_in_ratio_influence_by_UE_SATELLITE_XY.append( count )
            

            media = sum(num_UEs_BASE_in_ratio_influence_by_UE_SATELLITE_XY) / len(num_UEs_BASE_in_ratio_influence_by_UE_SATELLITE_XY)
            num_UEs_BASE_in_ratio_influence_by_UE_SATELLITE_XY.sort()

            graficar_scatter( num_UEs_BASE_in_ratio_influence_by_UE_SATELLITE_XY, 
                                code2name[ code_satellite_X ], code_satellite_X,
                                code2name[ code_base_Y ], code_base_Y,
                                ratio_influence, media,
                                 "./plots_hst_poles/" )
            
            print( media, end=",  ")
        print("\n")

    return


def main():
    pass
    #Lista de dos microtipos  de actividad
    #312112 = Purificación y embotellado de agua
    #434211 = Comercio al por mayor de cemento, tabique y grava
    #463215 = comercio al por menor de bisuteria y accesorios para vestir.
    #463113 = Comercio al por menor de artículos de mercería y bonetería
    
    #mymap = plt.imread("./media/map_CDNR.png")
    #BBox = ((-99.3686, -99.2670, 19.58, 19.65))


if __name__ == "__main__":
    #main()
    #correr primero solo esta funcion
    compute_influence_ratios()
    
    #despues solo esta
    #generate_table_medias()
    
