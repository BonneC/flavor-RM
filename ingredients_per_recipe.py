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


print(get_region_averages(get_region_dict()))
