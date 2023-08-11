import random
import re

TOTAL_AMOUNT = "total_amount"

AMOUNT_SENTENCE = "amount_sentence"

PRODUCT_NAME = "product_name"

PRODUCT_AMOUNT = "product_amount"


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


def update_total_amount(fake_data):
    amount_list = fake_data[PRODUCT_AMOUNT]
    total = 0
    for val in amount_list:
        total += float(val[:-2].strip().replace(',', '.'))
    fake_data[TOTAL_AMOUNT] = str(total) + " €"
    return fake_data


def transform_data(fake_data):
    """
    Transform generated data according to the need of the output
    :param fake_data:
    :return:
    """

    # If product key pairs exists in generated data
    # Returns random samples of product name and amount
    if PRODUCT_AMOUNT in fake_data and PRODUCT_NAME in fake_data:
        len_products = len(fake_data[PRODUCT_NAME])
        n = random.randint(2, 6)
        products_data = fake_data[PRODUCT_NAME]
        if n <= len_products:
            products_data = random.sample(products_data, n)
        fake_data[PRODUCT_NAME] = []
        fake_data[PRODUCT_AMOUNT] = []
        for product in products_data:
            print(product[0])
            fake_data[PRODUCT_NAME].append(product[0])
            fake_data[PRODUCT_AMOUNT].append(product[1])
        fake_data = update_total_amount(fake_data)

    # If amount sentence exists in the generated data
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
