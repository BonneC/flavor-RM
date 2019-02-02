import csv
import numpy as np


def get_region_dict():
    regions_dict = {}

    with open('dataset_region_recepies.csv', mode='r') as input_file:
        csv_reader = csv.reader(input_file, delimiter=',', quotechar='|')

        for row in csv_reader:
            region_name = row[0]
            regions_dict.setdefault(region_name, [])

            regions_dict[region_name].append(
                len(row[1:])
            )

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


def write_region_averages():
    region_average_list = get_region_averages(get_region_dict())
    with open('region_avg_num_recipe.csv', mode='w', newline='') as outfile:
        csv_writer = csv.writer(outfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Region', 'Average Ingredients'])  # set header
        csv_writer.writerows(region_average_list)


def get_ingredient_per_recipe():
    ingredient_per_recipe = {}
    region_dict = get_region_dict()

    for region in region_dict.keys():
        ingredient_per_recipe.setdefault(region, [])
        num_ingredients = list(set(region_dict[region]))  # get unique numbers only
        for num in num_ingredients:
            count = region_dict[region].count(num)
            ingredient_per_recipe[region].append((num, count))

    list_result = []
    for region in ingredient_per_recipe.keys():
        for item in ingredient_per_recipe[region]:
            list_result.append(
                (region, item[0], item[1])
            )

    return list_result


def write_ingredient_per_recipe():
    ingredient_per_recipe = get_ingredient_per_recipe()
    with open('ingredient_per_recipe.csv', mode='w', newline='') as outfile:
        csv_writer = csv.writer(outfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Region', ])
        csv_writer.writerows(ingredient_per_recipe)


# write_region_averages()  # execute writing to csv
write_ingredient_per_recipe()  # execute writing ingredient per recipe to csv

exit(0)

from pprint import pprint

pprint(get_ingredient_per_recipe())
