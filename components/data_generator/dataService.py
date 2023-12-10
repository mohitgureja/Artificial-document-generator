import os
import random
import re

HERR_IMAGE_FILEPATH = "data/input/generator/person/herr"
FRAU_IMAGE_FILEPATH = "data/input/generator/person/frau"

NAME = "name"

TOTAL_AMOUNT = "total_amount"

AMOUNT_SENTENCE = "amount_sentence"

PRODUCT_NAME = "product_name"

PRODUCT_AMOUNT = "product_amount"

TITLE = "title"

ORGANIZATION = "organization"

PROFILE_IMAGE = "profile_image"


def update_gpt_data(fake_data, gpt_data):
    """
    Update gathered data from gpt to the genereator data
    :param fake_data:
    :param gpt_data:
    :return:
    """
    for key, val in gpt_data.items():
        fake_data[key] = val
    return fake_data


def update_title(fake_data):
    if ORGANIZATION in fake_data:
        fake_data[TITLE] = fake_data[ORGANIZATION]
    return fake_data


# TODO: Make it generic with configurations
def update_profile_image(fake_data):
    if NAME in fake_data:
        name = fake_data[NAME]
        names = name.split()
        if len(names) > 0:
            filepath = FRAU_IMAGE_FILEPATH
            if "herr" in names[0].lower():
                filepath = HERR_IMAGE_FILEPATH
            images = os.listdir(filepath)
            sample = random.choice(images)
            print(sample)
            filepath = filepath + "/" + sample
            fake_data[PROFILE_IMAGE] = filepath
    return fake_data


def update_logo_image(fake_data):
    logo_path = "data/input/resources/Logo"
    images = os.listdir(logo_path)
    sample = random.choice(images)
    filepath = logo_path + "/" + sample
    fake_data["logo_image"] = filepath
    return fake_data


def transform_data(fake_data, gen_config_data):
    """
    Transform generated data according to the need of the output
    :param fake_data:
    :return:
    """
    dependent_fields = gen_config_data["calculate_keys"]
    # If product key pairs exists in generated data
    # Returns random samples of product name and amount
    if TOTAL_AMOUNT in dependent_fields:
        fake_data = update_total_amount(fake_data)

    # If organization exists in the generated data
    if TITLE in dependent_fields:
        fake_data = update_title(fake_data)

    # If amount sentence exists in the generated data
    if AMOUNT_SENTENCE in dependent_fields:
        fake_data = update_amount_sentence(fake_data)

    if PROFILE_IMAGE in dependent_fields:
        fake_data = update_profile_image(fake_data)

    if "logo_image" in dependent_fields:
        fake_data = update_logo_image(fake_data)
    return fake_data


def update_amount_sentence(fake_data):
    if TOTAL_AMOUNT in fake_data and AMOUNT_SENTENCE in fake_data:
        fake_data[AMOUNT_SENTENCE] = random.choice(
            fake_data[AMOUNT_SENTENCE])
        fake_data[AMOUNT_SENTENCE] = fake_data[AMOUNT_SENTENCE].replace("<amount>", str(fake_data[TOTAL_AMOUNT]))
        firstword, secondword = fake_data[AMOUNT_SENTENCE].split(' ', 1)
        # If first word of the sentence is a german word
        pattern = r'^[a-zA-ZäüöẞÖÜÄ]+$'
        if not re.match(pattern, firstword):
            fake_data[AMOUNT_SENTENCE] = secondword
    return fake_data


def update_total_amount(fake_data):
    if PRODUCT_NAME in fake_data:
        len_products = len(fake_data[PRODUCT_NAME])
        n = random.randint(5, 12)
        products_data = fake_data[PRODUCT_NAME]
        if n <= len_products:
            products_data = random.sample(products_data, n)
        fake_data[PRODUCT_NAME] = []
        fake_data[PRODUCT_AMOUNT] = []
        for product in products_data:
            fake_data[PRODUCT_NAME].append(product[0])
            fake_data[PRODUCT_AMOUNT].append(product[1])
        amount_list = fake_data[PRODUCT_AMOUNT]
        total = 0
        for val in amount_list:
            total += float(val[:-2].strip().replace(',', '.'))
        fake_data[TOTAL_AMOUNT] = "{:.2f}".format(total) + " €"
    return fake_data
