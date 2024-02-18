import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import networkx as nx
import warnings
from itertools import permutations


sns.set(style="darkgrid", color_codes=True)
pd.set_option('display.max_columns', 75)

data = pd.read_csv('./querys/corte_zone_tickets.csv', header = None)
# data.info()
# data.info()

# print(data.head())
# print(data.describe())

color = plt.cm.rainbow(np.linspace(0, 1, 40))
data[0].value_counts().head(40).plot.bar(color = color, figsize=(13,5))
plt.title('frequency of most popular bussines', fontsize = 20)
plt.xticks(rotation = 90 )
plt.grid()
plt.show()

data['business'] = 'Business'
food = data.truncate(before = -1, after = 15)
food = nx.from_pandas_edgelist(food, source = 'business', target = 0, edge_attr = True)

warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (13, 13)
pos = nx.spring_layout(food)
color = plt.cm.Set1(np.linspace(0, 15, 1))
nx.draw_networkx_nodes(food, pos, node_size = 15000, node_color = color)
nx.draw_networkx_edges(food, pos, width = 3, alpha = 0.6, edge_color = 'black')
nx.draw_networkx_labels(food, pos, font_size = 20, font_family = 'sans-serif')
plt.axis('off')
plt.grid()
plt.title('Top 15 First Popular Bussines', fontsize = 20)
plt.show()

# Getting the list of transactions from the dataset
transactions = []
for i in range(0, len(data)):
    transactions.append([str(data.values[i,j]) for j in range(0, len(data.columns))])

flattened = [item for transactions in transactions for item in transactions]
items = list(set(flattened))

if 'Nan' in items: items.remove('Nan')

rules = list(permutations(items, 2))
print('\n# of rules:',len(rules))
print(rules[:5])