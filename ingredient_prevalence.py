import csv
import networkx as nx
import numpy as np


def get_ingredient_list():
    G = nx.read_edgelist('clean_dataset.csv', nodetype=str,
                         delimiter=',',
                         encoding="utf-8",
                         create_using=nx.Graph(),
                         data=(('weight', int),))

    edges = nx.get_edge_attributes(G, 'weight')

    ingredients = []

    for edge in edges:
        ingr1 = edge[0]
        ingr2 = edge[1]

        ingredients.append(ingr1)
        ingredients.append(ingr2)

    return list(set(ingredients))


ingredients = get_ingredient_list()


def get_region_dict(ingredients=[]):
    ingredients_dict = {}

    with open('dataset_region_recepies.csv', mode='r') as input_file:
        csv_reader = csv.reader(input_file, delimiter=',', quotechar='|')

        for ingredient in ingredients:
            ingredients_dict.setdefault(ingredient, [])

            counter_per_country = 0
            region_name = 'African'
            for row in csv_reader:
                if row[0] == region_name:
                    if ingredient in row:
                        counter_per_country += 1
                else:
                    ingredients_dict[ingredient].append(
                        (region_name, counter_per_country)
                    )

                    region_name = row[0]
                    if ingredient in row:
                        counter_per_country = 1
                    else:
                        counter_per_country = 0

    return ingredients_dict


ingredient_dict = get_region_dict(ingredients)

for item in ingredient_dict.items():
    print(item)