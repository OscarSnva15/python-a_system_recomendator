import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import seaborn as sb


dataframe = pd.read_csv('../querys/crecimientoNicolasRomero.csv')
print(dataframe.head(10))