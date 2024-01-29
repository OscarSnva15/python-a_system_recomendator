from pickle import TRUE
import numpy as np
import pandas as pd
import os

class Business:
    def __init__(self, name, type, clave, age):
        self.name = name
        self.type = type
        self.clave = clave
        self.age = age

df_VAGB = pd.read_csv('./category_data/DENSIDAD(1)_AGB_COLONIA/nicolas_romero_CDAGB.csv')
df_NAGB = pd.read_csv('./category_data/DENUE_DATOS_CRECIMIENTO/consultasNicolasRomero/crecimientoNicolasRomero.csv')
df = pd.DataFrame(columns=['region_name', 'agb', 'density'])

for i in df_VAGB.index:

#nicolas_romero_CDAGB: Clave de la AGEB
#nicolas_romero_CDNAGB: Área geoestadística básica