from data_generator import helper, fakerWrapper, gptService, dataService

DATA_CONFIG = "data/input/generator/config.json"
WRITE_INVOICE_FILENAME = "data/input/renderer/invoices.json"


def generate_gpt_data(config_data):
    """
    Generate data for field variables using GPT model
    :param config_data:
    :return:
    """
    data = {}
    if config_data["gpt_enabled"]:
        for key in config_data["gpt_keys"]:
            query = config_data["queries"][key]
            isKeyPair = key in config_data["gpt_key_pairs"]
            data[key] = gptService.generate_gpt_sentence(key, query, isKeyPair)
    else:
        gpt_response = helper.read_json("data/input/renderer/gpt_response.json")
        for key in gpt_response.keys():
            data[key] = gpt_response[key]
    return data


def generate_data(data_field_names, config_params):
    """
    Generate fake data for required field variables
    :param data_field_names:
    :param config_params:
    :return:
    """
    # JSON Data file for configurations
    config_data = helper.read_json(DATA_CONFIG)

    # Create data here
    generated_data = []

    # Generate gpt sentences for fields
    gpt_data = generate_gpt_data(config_data)

    for i in range(config_params["invoice_count"]):
        fake_data = {}
        for data_field in data_field_names.keys():
            if data_field not in config_data["gpt_keys"] and data_field not in config_data["calculate_keys"]:
                # Generate fake data fields using Faker
                data = fakerWrapper.generate_fake_data(data_field, config_params["countries"])
                fake_data[data_field] = data

        # Update generated sentences from GPT into the fields
        fake_data = dataService.update_gpt_data(fake_data, gpt_data)

        # Invoke transformations in data
        fake_data = dataService.transform_data(fake_data)

        generated_data.append(fake_data)

    # Write data into JSON file
    helper.write_json(generated_data, "%s" % WRITE_INVOICE_FILENAME)
    return WRITE_INVOICE_FILENAME
