from cgi import print_form
import code
from codecs import latin_1_encode
from csv import writer
from dataclasses import dataclass
from math import dist, radians, cos, sin, asin, sqrt
from unittest.util import three_way_cmp
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
from dataclasses import dataclass

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

@dataclass
class data_business_filter:
    code_bussines : int
    epoch : int
    filter_bussines : pd.DataFrame
    df_complete : pd.DataFrame
    bussines_neighborhood_acc : dict
    influence_radio : float
    influence_radio_2 : float
    intradistances_target_bussines : pd.DataFrame
    accumulated_neighborhood_bussines : dict
    code_poles : set

    def __init__(self, df, code_bussines, epoch ):
        self.code_bussines = code_bussines
        self.epoch = epoch
        self.df_complete = df
        self.filter_bussines = self.__filter_by_code()
        self.bussines_neighborhood_acc = self.__get_bussines_neighborhood_acc()

    def __set_code_poles(self):
            self.code_poles = ( 311520, 311812, 311830, 311910, 312112, 321910, 323119, 332320, 337120, 434112, 434211, 434311, 461110, 461121, 461122, 461130, 461140, 461150, 461160, 461170, 461190, 461213, 462112, 463113, 463211, 463213, 463215, 463310, 464111, 464112, 464113, 465111, 465211, 465311, 465912, 466111, 466212, 466312, 466410, 467111, 467113, 467114, 467115, 468112, 468211, 468420, 531113, 532282, 541110, 541920, 541941, 561432, 611111, 611112, 611621, 621111, 621211, 621398, 621511, 713120, 713943, 722412, 722511, 722512, 722513, 722514, 722515, 722517, 722518, 722519, 811111, 811112, 811119, 811121, 811191, 811192, 811211, 811219, 811410, 811420, 811430, 811492, 811499, 812110, 812130, 812210, 812410, 813210, 813230, 931610)

    def __filter_by_code(self):
        #snaptime overview data
        df_filter_general = self.df_complete[ self.df_complete['Código_de_la_clase_de_actividad_SCIAN'] ==  self.code_bussines]

        #snaptime windows df
        filtered = None
        #apply filter time on overview data
        if self.epoch == 0:
            filtered =  df_filter_general[ df_filter_general['Fecha_de_incorporacion_al_DENUE'] < '2014-12' ]
        elif self.epoch == 1:
            # filtered =  df_filter_general[(df_filter_general['Fecha_de_incorporacion_al_DENUE'] >= '2014-12') & (df_filter_general['Fecha_de_incorporacion_al_DENUE'] < '2019-11') ]
            filtered =  df_filter_general[ df_filter_general['Fecha_de_incorporacion_al_DENUE'] < '2019-11' ]
        elif self.epoch == 2:
            # filtered =  df_filter_general[ df_filter_general['Fecha_de_incorporacion_al_DENUE'] >= '2019-11' ]
            filtered =  df_filter_general
        else:
            filtered = df_filter_general

        print( "epoch ", self.epoch, "  TOTAL CODE-BUSSINESS FOUND: ",len(filtered) )

        return filtered


    def plot_escenary(self, lat, long):
        fig, ax = plt.subplots(figsize = (22,12))
        ax.scatter(self.filter_bussines.Longitud, self.filter_bussines.Latitud, zorder=1, alpha= 0.4, c='r', s=10)
        mymap = plt.imread("./media/map_CDNR.png")
        BBox = ((-99.3686, -99.2670, 19.58, 19.65))

        x_values = [(BBox[0]+BBox[1])/2, (BBox[0]+BBox[1])/2 + self.influence_radio]
        y_values = [(BBox[3]+BBox[2])/2, (BBox[3]+BBox[2])/2  ]
        ax.plot(x_values, y_values, c='b' )

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

    def __get_bussines_neighborhood_acc(self):
        #obtain the dataframe that have data abouth rangeAverage and dataframe class business
        self.intradistances_target_bussines = self.__get_average_distance_for_BussinesCode()

        self.influence_radio_2 = float(self.intradistances_target_bussines.mode().mean()) / 2
        self.influence_radio = float(self.intradistances_target_bussines.mean()) / 2

        print("self.influence_radio mode mean: ", self.influence_radio_2)
        print("self.influence_radio mean: ", self.influence_radio)

        self.__set_code_poles()
        types_code = {}
        for code in self.code_poles:
            types_code[code] = 0

        return types_code

    def __get_average_distance_for_BussinesCode(self):
        list_distances = []
        #The one business by step to comparate with all them data
        for _, base in self.filter_bussines.iterrows():
            array = []

            #The all business to comparate with the step data
            for _, row in self.filter_bussines.iterrows():
                if (base['Latitud'] - row['Latitud'])!=0 and (base['Latitud'] - row['Latitud'])!=0:
                    # dlat = base['Latitud'] - row['Latitud']
                    # dlong = base['Longitud'] - row['Longitud']
                    # array.append(  sqrt( dlat**2 + dlong**2 ) )
                    array.append( max(abs(base['Latitud'] - row['Latitud']), abs(base['Longitud'] - row['Longitud'])))

            array.sort()
            list_distances.append(array[0])

        #once we obtained the distances we must save into dataframe
        df_distances = pd.DataFrame(list_distances, columns = ['Distances_Totals_Between_BusinessTypeClass'])

        # ploter histograma of datafram distances
        # plt.hist(list_distances, bins=40)
        # plt.show()


        return  df_distances

    def report_accumulated_bussines_support(self):
        Latitud = []
        Longitud = []
        posicion = 0
        dfExcel = pd.DataFrame(columns = ['snapTime','nameBussines','311520','311812','311830','311910','312112','321910','323119','332320','337120','434112','434211','434311','461110','461121','461122','461130','461140','461150','461160','461170','461190','461213','462112','463113','463211','463213','463215','463310','464111','464112','464113','465111','465211','465311','465912','466111','466212','466312','466410','467111','467113','467114','467115','468112','468211','468420','531113','532282','541110','541920','541941','561432','611111','611112','611621','621111','621211','621398','621511','713120','713943','722412','722511','722512','722513','722514','722515','722517','722518','722519','811111','811112','811119','811121','811191','811192','811211','811219','811410','811420','811430','811492','811499','812110','812130','812210','812410','813210','813230','931610'], index=range(12))
        list_codes = [468412]
        
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
            dfExcel.iloc[posicion]=(str(self.epoch), str(base['Nombre_de_la_Unidad_Económica']), str(code[0]), str(code[1]), str(code[2]),str(code[3]),str(code[4]),str(code[5]),str(code[6]),str(code[7]),str(code[8]),str(code[9]),str(code[10]),str(code[11]),str(code[12]),str(code[13]),str(code[14]),str(code[15]),str(code[16]),str(code[17]),str(code[18]),str(code[19]),str(code[20]),str(code[21]),str(code[22]),str(code[23]),str(code[24]),str(code[25]),str(code[26]),str(code[27]),str(code[28]),str(code[29]),str(code[30]),str(code[31]),str(code[32]),str(code[33]),str(code[34]),str(code[35]),str(code[36]),str(code[37]),str(code[38]),str(code[39]),str(code[40]),str(code[41]),str(code[42]),str(code[43]),str(code[44]),str(code[45]),str(code[46]),str(code[47]),str(code[48]),str(code[49]),str(code[50]),str(code[51]),str(code[52]),str(code[53]),str(code[54]),str(code[55]),str(code[56]),str(code[57]),str(code[58]),str(code[59]),str(code[60]),str(code[61]),str(code[62]),str(code[63]),str(code[64]),str(code[65]),str(code[66]),str(code[67]),str(code[68]),str(code[69]),str(code[70]),str(code[71]),str(code[72]),str(code[73]),str(code[74]),str(code[75]),str(code[76]),str(code[77]),str(code[78]),str(code[79]),str(code[80]),str(code[81]),str(code[82]),str(code[83]),str(code[84]),str(code[85]),str(code[86]),str(code[87]),str(code[88]),str(code[89]))
            posicion = posicion + 1
        
        averageList = []
        ListColumns  = []
        #add code only problabilyty
        ListColumns = dfExcel.columns
        for x in ListColumns:
            if x != 'snapTime' and x !='nameBussines':
                averageList.append(dfExcel[x].mean())

        self.cutoff = sum(averageList[3::])/len(averageList[3::])
        self.desc_bussines = self.filter_bussines.iloc[0]["Nombre_de_clase_de_la_actividad"]

        # VCDL = [ 10 if x > self.cutoff*0.75 else 0 for x in averageList ]
        VCDL = averageList
        VCDL.insert(0,self.code_bussines)
        VCDL.insert(1,self.filter_bussines.iloc[0]["Nombre_de_clase_de_la_actividad"])

        # averageList.insert(0,"")
        # averageList.insert(1,"Promedio")
        # dfExcel.loc[len(dfExcel)] = averageList
        
        # writer = pd.ExcelWriter('./querys/dataExceLCreated/pruebaUno.xlsx', engine='xlsxwriter')
        # dfExcel.to_excel(writer, sheet_name='sheet1', index = True)
        # writer.save()

        # self.plot_escenary(Latitud, Longitud)

        return VCDL


def get_productExcel():
    writer = pd.ExcelWriter('demo.xlsx', engine='xlsxwriter')
    df = pd.read_csv("./querys/crecimientoNicolasRomero.csv")
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('demo.xlsx', engine='xlsxwriter')
    writer.save()
    return

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
    title = ["Fecha Nacimiento < 2014-12", "Fecha Nacimiento < 2019-11","Fecha Nacimiento< 2022-05" ]

    fig, ax = plt.subplots(nrows = 1, ncols= 3, figsize = (26,10))

    latit, longit = target_location[0],  target_location[1]

    df_filter_class_location = []
    for snapshot_time in df_filter_class_snaptime:
        df_filter_location_code = pd.DataFrame()
        # Filter data by NEIGHBORHOOD
        df_filter_class_location.append( snapshot_time[ snapshot_time.apply(lambda x: get_distance(x['Latitud'], latit, x['Longitud'], longit) < 0.250, axis=1) ]   )

    for i in range(3):
        ax[i].set_title(title[i])
        ax[i].set_xlim(BBox[0],BBox[1])
        ax[i].set_ylim(BBox[2],BBox[3])
        ax[i].imshow(mymap, zorder=0, extent = BBox, aspect = 'equal')
        for j in range(i+1):
            ax[i].scatter(df_filter_class_location[j]['Longitud'], df_filter_class_location[j]['Latitud'], zorder=1, alpha= 0.71, c=color[j], s=10)

        plt.savefig('./images_insights/'+str(code)+'.png')

def plot_scatter_bussines_by_code(df, BBox, mymap, code_list ):
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
    code= 468420
    Latitud, Longitud = [19.62054709688509, -99.31394730905744]
    time_window = 0
    # ratio = 0.000250
    df = pd.read_csv("./querys/crecimientoNicolasRomero.csv")

    mymap = plt.imread("./media/map_CDNR.png")
    BBox = ((-99.3686, -99.2670, 19.58, 19.65))

    bussines_snapshot =  data_business_filter( df, code, time_window)
    print( "bussines_snapshot.influence_radio : ", bussines_snapshot.influence_radio )
    print( "radio KM: ",distance(0,bussines_snapshot.influence_radio ,0,0) )
    print( "total bussines in radio: ", len(bussines_snapshot.bussines_neighborhood_acc) )
    print( "0.00099 to KM: ",distance(0,0.00099 ,0,0) )

    bussines_snapshot.report_accumulated_bussines_support()



    # code_list = [461110, 465311, 311830, 467111, 461122, 311812 ]
    # get_setBusinessClass(df,code,time_window)
    # get_averageDistanceClass(df,code,time_window)
    #Firts apply filter class snaptimes on typeClass
    #print("average distance: \n ",get_averageDistanceClass(df,code,time_window))
    #plot_scatter_bussines_by_code(df, BBox, mymap, code_list)
    # get_scaterPlotBusinessClass(df,code,time_window)

    # get_productExcel()
    return

if __name__ == "__main__":
    main()

    # class_1 = [ 461110, 465311, 311830, 467111, 461122, 311812 ]
    # class_2 = [ 812110, 461121, 461130, 811111, 468211, 811191, 312112, 811492, 221312, 485111,464111 ]
    # class_3 = [ 463211,463113,531113,713120,811410,722519,311520,811499,811211,461213,812910,431150,561431,465913,517311,522460,435419,813120]
    # class_4 = [ 621211,561432,463310,722517,467114,466212,461170,811119,434211,465111,466312,465211,321910,466410,465212,463212,811493,465313,463213,812310,713991,434311,112512]
    # class_5 = [ 464111,461160,722514,813210,611111,722513,722518,722515,461190,811121,811430,465912,467113,461140,466111,722511,811115,811116,811312,468112,722412,811199,465919,532282,811219,311214,463217,465312,431180,311611,432130,811314]
    # class_6 = [ 467115,332320,461150,811112,812210,621111,541941,713943,541920,434112,611112,465914,464121,811192,812410,811491,464112,337120,811420,466114,434224,722512,812130,463216,519122,811122,541190,611171,931210,813230]
    # class_7 = [ 468420,332710,464113,463215,323119,621511,931610,462112,541211,624191,466112,311910,541110,522452,434221,468412,461123,621398,461212,315225,434314,811129,811114,811113,315229,327121,621320,621331]
    # class_8 = [ 434312,327330,465215,465911,812990,461211,611621,465112,721112,467112,463111,624412,711312,621311,532281,463218,624411,465216,322299,326198,339111,517312,323111,541943,611421]
    # class_9 = [ 465915,468213,611611,621113,339999,466319,611691,337110,468413,468419,541890,624199,813110,314912,463112,466211,332310,435313,466311,468212,531114,611631,315192,811311,237131,237993]
    # class_10= [327111,485510,931310,463214,434219,517910,316991,431121,541310,434222,488493,488519,532122,623312,621411,711410]