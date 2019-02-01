import csv


def get_ingredients_frequency_list():
    ingredients_frequency = {}

    with open('dataset_region_recepies.csv', mode='r') as input_file:
        csv_reader = csv.reader(input_file, delimiter=',', quotechar='|')

        for row in csv_reader:
            recipe_ingredients = row[1:]
            for ingredient in recipe_ingredients:
                ingredients_frequency.setdefault(ingredient, 0)
                ingredients_frequency[ingredient] += 1

    ingredients_frequency_list = [(key, ingredients_frequency[key]) for key in ingredients_frequency.keys()]

    return ingredients_frequency_list


def write_ingredients_frequency():
    ingredients_frequency_list = get_ingredients_frequency_list()

    with open('ingredients_frequency.csv', mode='w', newline='') as outfile:
        csv_writer = csv.writer(outfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Ingredient', 'Value'])  # set header
        csv_writer.writerows(ingredients_frequency_list)


write_ingredients_frequency()  # execute writer
