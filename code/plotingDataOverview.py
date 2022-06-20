import matplotlib.pyplot as plt
import pandas as pd

cy = []
cx = []

df = pd.read_csv("../querys/crecimientoNicolasRomero.csv")
for i in df.index:
    if df['Fecha_de_incorporacion_al_DENUE']<='2010-12':
        cx[i]=cx[i]+1
        cy[i]=cy[i]+1

# plotting the points 
plt.plot(cx, cy)
# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')
# giving a title to my graph
plt.title('My first graph!')
# function to show the plot
plt.show()