import random
import re


def update_gpt_data(fake_data, gpt_data):
    for key, val in gpt_data.items():
        fake_data[key] = random.choice(val)
    return fake_data


def transform_data(fake_data):
    if "product_amount" in fake_data and "amount_sentence" in fake_data:
        fake_data["amount_sentence"] = fake_data["amount_sentence"].replace("<amount>", fake_data["product_amount"])
        firstword, secondword = fake_data["amount_sentence"].split(' ', 1)
        pattern = r'^[a-zA-ZäüöẞÖÜÄ]+$'
        if not re.match(pattern, firstword):
            fake_data['amount_sentence'] = secondword
    return fake_data
