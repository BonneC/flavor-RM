import csv
import networkx as nx
import numpy as np


def get_compound_dict():
    G = nx.read_edgelist('clean_dataset.csv', nodetype=str,
                         delimiter=',',
                         encoding="utf-8",
                         create_using=nx.Graph(),
                         data=(('weight', int),))

    return nx.get_edge_attributes(G, 'weight')


weights_dict = get_compound_dict()


def get_region_dict():
    regions_dict = {}

    with open('dataset_region_recepies.csv', mode='r') as input_file:
        csv_reader = csv.reader(input_file, delimiter=',', quotechar='|')

        for row in csv_reader:
            region_name = row[0]
            regions_dict.setdefault(region_name, [])

            sum_weights = 0
            avg_compounds_in_recipe = 0.0
            for i in range(1, len(row[1:]) - 1):
                for j in range(i + 1, len(row[1:])):
                    key1 = (row[i], row[j])
                    key2 = (row[j], row[i])
                    weight1 = weights_dict.get(key1)
                    weight2 = weights_dict.get(key2)
                    if weight1 is not None:
                        sum_weights += weight1
                    elif weight2 is not None:
                        sum_weights += weight2

            if len(row[1:]) - 1 > 0:
                # n*(n+1)/2
                possible_links = ((len(row[1:]) - 1) * (len(row[1:]))) / 2

                avg_compounds_in_recipe = sum_weights / possible_links
                regions_dict[region_name].append(avg_compounds_in_recipe)

    return regions_dict


def get_region_averages(regions_dict={}):
    region_averages = []
    for key in regions_dict.keys():
        average_ingridients = round(np.average(regions_dict[key]), 2)
        row = (
            key, average_ingridients
        )
        region_averages.append(row)
    return region_averages


region_dict = get_region_dict()

for item in region_dict.items():
    print(item)

region_avg = get_region_averages(region_dict)

print(region_avg)
