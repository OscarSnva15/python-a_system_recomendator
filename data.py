from cProfile import label
import pandas as pd
#Density population on each municipal ()
dataset_density = pd.read_csv('../POBLACION/Poblacion_03.csv')

#National Survey of Demographic Dynamics
dataset_demographic = pd.read_csv('../INEGI/consultasIsidroFabela/C1_ISF_INEGI_DENUE.csv')

#clean our datas by removing duplicate values, and transforming columns into numerical values to make them

