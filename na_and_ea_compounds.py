import csv
import networkx as nx


def get_compound_dict():
    G = nx.read_edgelist('clean_dataset.csv', nodetype=str,
                         delimiter=',',
                         encoding="utf-8",
                         create_using=nx.Graph(),
                         data=(('weight', int),))

    return nx.get_edge_attributes(G, 'weight')


weights_dict = get_compound_dict()


def get_ingredients_frequency_list(region):
    ingredients = []

    with open(region, mode='r') as input_file:
        csv_reader = csv.reader(input_file, delimiter=',', quotechar='|')

        for row in csv_reader:
            recipe_ingredients = row[1:]
            for ingredient in recipe_ingredients:
                ingredients.append(row[0])

        ingredients = ingredients[1:]

        sum_weights = 0
        avg_compounds_in_recipe = 0.0
        for i in range(0, len(ingredients) - 1):
            for j in range(i + 1, len(ingredients)):
                key1 = (ingredients[i], ingredients[j])
                key2 = (ingredients[j], ingredients[i])

                weight1 = weights_dict.get(key1)
                weight2 = weights_dict.get(key2)
                if weight1 is not None:
                    sum_weights += weight1
                elif weight2 is not None:
                    sum_weights += weight2

            # n*(n+1)/2
            possible_links = ((len(ingredients) - 1) * (len(ingredients))) / 2

            avg_compounds_in_recipe = sum_weights / possible_links

    return ingredients, avg_compounds_in_recipe


print(get_ingredients_frequency_list('north_american_ingredients2.csv'))
print(get_ingredients_frequency_list('east_asian_ingredients2.csv'))
