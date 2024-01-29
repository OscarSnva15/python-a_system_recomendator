import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import seaborn as sb

"""This function creates a data frame ,it does work with libraries pandas"""
def load_dataFrame():
    dataframe = pd.read_csv('./querys/crecimientoNicolasRomero.csv')
    print(dataframe.head(10))

def main():
    load_dataFrame()
    
if __name__ == "__main__":
    main()