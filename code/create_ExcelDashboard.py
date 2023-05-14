from cgi import print_form
from csv import writer
from math import dist, radians, cos, sin, asin, sqrt
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.pyplot import cm
import numpy as np

def getDistances(lat1, lat2, lon1, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return (c * r)

def get_setBusinessClass(df,code,time_window):
    #snaptime overview data
    df_filter_general = df[ df['Código_de_la_clase_de_actividad_SCIAN'] ==  code]
    #snaptime windows df
    df_window_time = []
    #apply filter time on overview data
    df_window_time.append( df_filter_general[ df_filter_general['Fecha_de_incorporacion_al_DENUE'] < '2014-12' ] )
    df_window_time.append( df_filter_general[(df_filter_general['Fecha_de_incorporacion_al_DENUE'] >= '2014-12') & (df_filter_general['Fecha_de_incorporacion_al_DENUE'] < '2019-11') ] )
    df_window_time.append( df_filter_general[ df_filter_general['Fecha_de_incorporacion_al_DENUE'] >= '2019-11' ] )
    df_final = pd.DataFrame(df_window_time[time_window])
    writer = pd.ExcelWriter('Set_code:'+str(code)+'_TimeWindow_:'+str(time_window)+'_output.xlsx')
    df_final.to_excel(writer)
    writer.save()
    return df_final

def get_averageDistanceClass(df,code,time_window):
    obtain_df = get_setBusinessClass(df,code,time_window)
    obtain_dfCopy = obtain_df.copy()
    list_distances = []
    #The one business by step to comparate with all them data
    for __, base in obtain_df.iterrows():
    #The all business to comparate with the step data
        for _, row in obtain_dfCopy.iterrows():
            if (base['Latitud'] - row['Latitud'])!=0 and (base['Latitud'] - row['Latitud'])!=0:
                # print(base['Latitud'],row['Latitud'])
                list_distances.append(max(abs(base['Latitud'] - row['Latitud']), abs(base['Longitud'] - row['Longitud'])))
    #once we obtained the distances we must save into dataframe
    df_distances = pd.DataFrame(list_distances, columns = ['Distances_Totals_Between_BusinessTypeClass'])
    # print(df_distances.describe())
    #ploter histograma of datafram distances
    # plt.hist(list_distances, bins=40)
    # plt.show()
    return  df_distances

def get_bussinesNeighbours(df,code,time_window):
    #obtain the dataframe that have data abouth rangeAverage and dataframe class business
    df_distances = get_averageDistanceClass(df,code,time_window)
    df_setBusinesClass = get_setBusinessClass(df,code,time_window)
    #calculate the average distance into dataframe obtained
    ratioAverage = float(df_distances.mean())
    #define a type of set to collect class key
    all_class = set()
    #we start iter data how an tuples Inner Join 
    for _, pibot in df_setBusinesClass.iterrows():
        for _, iter in df.iterrows():
            if (getDistances(pibot['Latitud'], iter['Latitud'] , pibot['Longitud'], iter["Longitud"]) <= ratioAverage) and (iter['Código_de_la_clase_de_actividad_SCIAN']!= code):
                all_class.add(iter['Código_de_la_clase_de_actividad_SCIAN'])
    all_class = sorted( all_class )
    print("Neighbours meet of Type Class "+str(code)+ " are: ", all_class)
    list_Neighbours = list(all_class)
    return list_Neighbours

def get_dicionary(df,code,time_window):
    dictionaryBusinessNeighbours = get_bussinesNeighbours(df,code,time_window)
    types_code = {}
    for code in dictionaryBusinessNeighbours:
        types_code[code] = 0
    return types_code

def get_scaterPlotBusinessClass(df,code,time_window):
    df_setBusinesClass = get_setBusinessClass(df,code,time_window)
    df_distances = get_averageDistanceClass(df,code,time_window)
    types_code = get_dicionary(df,code,time_window)
    ratioAverage = float(df_distances.mean())
    print(ratioAverage)
    print(types_code)
    #iterate dataframe
    for _, base in df_setBusinesClass.iterrows():
        for _, iter in df.iterrows():
            
            if(base['Código_de_la_clase_de_actividad_SCIAN']!= code):
                if abs((iter['Latitud'] - base['Latitud'])) < ratioAverage  and  abs((iter['Longitud']-base['Longitud'])) < ratioAverage:
                    types_code[iter['Código_de_la_clase_de_actividad_SCIAN']] +=  1
                    print(iter['Código_de_la_clase_de_actividad_SCIAN'])
                    # all_class.add( row['Código_de_la_clase_de_actividad_SCIAN'] )
        print("\n", base['Nombre_de_la_Unidad_Económica'],  list(types_code.values()))
    return

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
        df_filter_class_location.append( snapshot_time[ snapshot_time.apply(lambda x: getDistances(x['Latitud'], latit, x['Longitud'], longit) < 0.250, axis=1) ]   )

    for i in range(3):
        ax[i].set_title(title[i])
        ax[i].set_xlim(BBox[0],BBox[1])
        ax[i].set_ylim(BBox[2],BBox[3])
        ax[i].imshow(mymap, zorder=0, extent = BBox, aspect = 'equal')
        for j in range(i+1):
            ax[i].scatter(df_filter_class_location[j]['Longitud'], df_filter_class_location[j]['Latitud'], zorder=1, alpha= 0.71, c=color[j], s=10)

        plt.savefig('../images_insights/'+str(code)+'.png')

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

        plt.savefig('../images_insights/test/' + "{:03d}".format(rank) + '_' + str(code)+'.png')
        plt.clf()

def main():
    code= 312112
    Latitud, Longitud = [19.62054709688509, -99.31394730905744]
    key_classType= 812110
    time_window = 2
    ratio = 0.000250
    df = pd.read_csv("./querys/crecimientoNicolasRomero.csv")
    mymap = plt.imread("../media/map_CDNR.png")
    BBox = ((-99.3686, -99.2670, 19.58, 19.65))
    code_list = [461110, 465311, 311830, 467111, 461122, 311812 ]
    # get_setBusinessClass(df,code,time_window)
    # get_averageDistanceClass(df,code,time_window)
    #Firts apply filter class snaptimes on typeClass
    #print("average distance: \n ",get_averageDistanceClass(df,code,time_window))
    #plot_scatter_bussines_by_code(df, BBox, mymap, code_list)
    get_scaterPlotBusinessClass(df,code,time_window)

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