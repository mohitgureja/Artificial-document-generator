import os
import random
import re

doc = "default"
resource_file_path = f"data/{doc}/input/resources/"

NAME = "name"
LOGO_IMAGE = "logo_image"
TOTAL_AMOUNT = "total_amount"
AMOUNT_SENTENCE = "amount_sentence"
PRODUCT_NAME = "product_name"
PRODUCT_AMOUNT = "product_amount"
TITLE = "title"
ORGANIZATION = "organization"
PROFILE_IMAGE = "profile_image"


def update_gpt_data(fake_data, gpt_data):
    """
    Update gathered data from gpt to the generator data
    :param fake_data:
    :param gpt_data:
    :return:
    """
    for key, val in gpt_data.items():
        fake_data[key] = val
    return fake_data


# TODO: Make it generic with configurations
def update_profile_image(fake_data):
    """
    Add profile image path according to the name and gender of the person
    :param fake_data: all generated data
    :return: updated fake data with image file path
    """
    if NAME in fake_data:
        name = fake_data[NAME]
        names = name.split()
        if len(names) > 0:
            filepath = resource_file_path + "person/frau"
            if "herr" in names[0].lower():
                filepath = resource_file_path + "person/herr"
            images = os.listdir(filepath)
            sample = random.choice(images)
            filepath = filepath + "/" + sample
            fake_data[PROFILE_IMAGE] = filepath
    return fake_data


def update_logo_image(fake_data):
    """
    Add logo file path to the data field "logo_image"
    :param fake_data: all generated data
    :return: updated fake data with logo image file path
    """
    logo_path = resource_file_path + "Logo"
    images = os.listdir(logo_path)
    sample = random.choice(images)
    filepath = logo_path + "/" + sample
    fake_data[LOGO_IMAGE] = filepath
    return fake_data


def update_amount_sentence(fake_data):
    """
    Add random function to pick sentence from gpt generated sentences
    :param fake_data: all generated data
    :return: updated fake data
    """
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
    """
    Calculate total amount from a list of product amounts
    :param fake_data:
    :return: updated fake data with new total amount data field
    """
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


def get_same_data(fake_data, duplicate_fields):
    """
    Copy the value of already generated data fields to defined similar field
    :param fake_data:
    :param duplicate_fields: dictionary of duplicate key fields with already generated field values
    :return: updated fake data with addition of duplicate keys
    """
    for k, v in duplicate_fields.items():
        fake_data[k] = fake_data[v]
    return fake_data


def transform_data(fake_data, gen_config_data, doc_format):
    """
    Transform generated data according to the need of the output
    :param fake_data:
    :return:
    """
    global resource_file_path
    resource_file_path = f"data/{doc_format}/input/resources/"

    duplicate_fields = gen_config_data["duplicate_keys"]
    fake_data = get_same_data(fake_data, duplicate_fields)

    dependent_fields = gen_config_data["calculate_keys"]
    # If product key pairs exists in generated data
    # Returns random samples of product name and amount
    if TOTAL_AMOUNT in dependent_fields:
        fake_data = update_total_amount(fake_data)

    # If amount sentence exists in the generated data
    if AMOUNT_SENTENCE in dependent_fields:
        fake_data = update_amount_sentence(fake_data)

    if PROFILE_IMAGE in dependent_fields:
        fake_data = update_profile_image(fake_data)

    if "logo_image" in dependent_fields:
        fake_data = update_logo_image(fake_data)
    return fake_data
