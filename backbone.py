import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
import csv


def disparity_filter(G, weight='weight'):
    B = nx.Graph()
    for u in G:
        k = len(G[u])
        if k > 1:
            sum_w = sum(np.absolute(G[u][v][weight]) for v in G[u])
            for v in G[u]:
                w = G[u][v][weight]
                p_ij = float(np.absolute(w)) / sum_w
                alpha_ij = 1 - (k - 1) * integrate.quad(lambda x: (1 - x) ** (k - 2), 0, p_ij)[0]
                B.add_edge(u, v, weight=w, alpha=float('%.4f' % alpha_ij))
    return B


def disparity_filter_alpha_cut(G, weight='weight', alpha_t=0.4, cut_mode='or'):
    B = nx.Graph()  # Undirected case:
    for u, v, w in G.edges(data=True):

        try:
            alpha = w['alpha']
        except KeyError:  # there is no alpha, so we assign 1. It will never pass the cut
            alpha = 1

        if alpha < alpha_t:
            B.add_edge(u, v, weight=w[weight])
    return B


G = nx.read_edgelist('clean_dataset.csv', nodetype=str,
                     delimiter=',',
                     encoding="utf-8",
                     create_using=nx.Graph(),
                     data=(('weight', int),))

# weights = nx.get_edge_attributes(G, 'weight')

# prvo dodava alfa vrednosti so prvava funkcija
# so vtorata spored tie vrednosti brishe edges
# kolku da znaes sho se zbiva
G_alpha = disparity_filter(G)
G_slim = disparity_filter_alpha_cut(G_alpha)

# cleaned edges sho treba da gi parsirash
# vaka izgledaat a treba da se vo .csv so koloni
# Source Target Weight
# ingr1  ingr2  weight_value
# print(G_slim.edges(data=True))

slim_edges_list = [(item[0], item[1], item[2]['weight']) for item in G_slim.edges(data=True)]
header_of_cleaned_edges_csv = ['Source', 'Target', 'Weight']

with open('cleaned_edges.csv', mode='w', newline='') as outfile:
    csv_writer = csv.writer(outfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(header_of_cleaned_edges_csv)
    csv_writer.writerows(slim_edges_list)
        

# IGNORE DIS
# edgewidth = [d['weight'] for (u, v, d) in G_slim.edges(data=True)]
# pos = nx.spring_layout(G_slim, iterations=50)

# pos = nx.random_layout(G)

# plt.figure(1)
# plt.subplot(211)
# plt.axis('off')
# nx.draw_networkx_nodes(G_slim, pos)
# nx.draw_networkx_edges(G_slim, pos, width=edgewidth, )
#
# plt.show()
