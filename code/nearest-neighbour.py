import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import seaborn as sb

# %matplotlib inline
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
# 1.- Calcular la distancia entre el item a clasificar y el resto de items del dataset de entrenamiento.
    # show neihgbour file code_19(the file is iterate wich one disctance an one type of bussines)
    # show neihgbour file code_3(the file is iterate wich one disctance an one type of bussines)