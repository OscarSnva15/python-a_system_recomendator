#The fisrt we need to obtain data from csv excel
import pandas as pd

df = pd.read_csv('../querys/crecimientoNicolasRomero.csv')

df.head(10)