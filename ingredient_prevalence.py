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


def get_region_dict(ingredients=[]):
    ingredients_dict = {}
    with open('dataset_region_recepies.csv', mode='r') as input_file:
        csv_reader = csv.reader(input_file, delimiter=',', quotechar='|')
        rows = list(csv_reader)  # get the reader content

        for ingredient in ingredients:
            ingredients_dict.setdefault(ingredient, [])
            counter_per_country = 0
            region_name = 'African'
            for row in rows:
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

    clean_ingredients_dict = {}
    for key in ingredients_dict.keys():
        count = 0;
        for item in ingredients_dict[key]:
            count += item[1]
        if count > 0:
            clean_ingredients_dict[key] = ingredients_dict[key]

    return clean_ingredients_dict


def get_num_recipes_regions():
    region_num_recepies_dict = {}
    with open('dataset_region_recepies.csv', mode='r') as input_file:
        csv_reader = csv.reader(input_file, delimiter=',', quotechar='|')

        for row in csv_reader:
            country_name = row[0]
            region_num_recepies_dict.setdefault(country_name, 0)

            if country_name in row:
                region_num_recepies_dict[country_name] += 1
    return region_num_recepies_dict


def get_prevalence_dict(recipes_count_region={}, number_recipes_dict={}):
    """
    Returns dictionary with ingredients as keys, and dictionary as value, where each key is a region
    and each value is the prevalence in that region
    :param recipes_count_region:
    :param number_recipes_dict:
    :return: Dictionary
    """
    prevalence_dict = {}  # final result dictionary with prevalence

    for ingredient in get_ingredient_list():  # go through each ingredient

        if ingredient not in recipes_count_region.keys(): continue  # skip when all 0s

        ingredient_in_recipes = recipes_count_region[ingredient]  # get the list with (region, count)
        prevalence_dict.setdefault(ingredient, {})

        for region in number_recipes_dict.keys():  # go through each region
            n = 0  # find n
            for item in ingredient_in_recipes:
                if item[0] == region:
                    n = item[1]

            N = number_recipes_dict[region]  # get the number of recipes in region
            prevalence = n / N
            prevalence_dict[ingredient][region] = prevalence

    return prevalence_dict


# testing ##################
import pprint

pprint.pprint(
    get_prevalence_dict(
        get_region_dict(get_ingredient_list()),
        get_num_recipes_regions()
    )
)
# pprint.pprint(get_region_dict(get_ingredient_list()))

exit(0)

ingredients = get_ingredient_list()
ingredient_dict = get_region_dict(ingredients)

for item in ingredient_dict.items():
    print(item)
