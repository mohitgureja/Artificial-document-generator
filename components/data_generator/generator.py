from components.data_generator import dataService, fakerWrapper, helper, gptService

GPT_DATA_CONFIG = "data/input/generator/config.json"
WRITE_DATA_FILEPATH = "data/input/renderer/"
RESPONSE_FILE_PATH = "data/input/renderer/gpt_response.json"


def generate_gpt_data(config_data, data_fields):
    """
    Generate data for field variables using GPT model
    :param data_fields:
    :param config_data:
    :return:
    """
    data = {}
    if config_data["gpt_enabled"]:
        for key in config_data["gpt_keys"]:
            if key in data_fields:
                query = config_data["queries"][key]
                isKeyPair = key in config_data["gpt_key_pairs"]
                data[key] = gptService.generate_gpt_sentence(key, query, isKeyPair)
        helper.write_json(data, RESPONSE_FILE_PATH)
    else:
        gpt_response = helper.read_json("data/input/renderer/gpt_response.json")
        for key in gpt_response.keys():
            if key in data_fields:
                data[key] = gpt_response[key]
    return data


def generate_data(data_field_names, config_params, doc_format):
    """
    Generate fake data for required field variables
    :param doc_format:
    :param data_field_names:
    :param config_params:
    :return:
    """
    # JSON Data file for configurations
    gen_config_data = helper.read_json(GPT_DATA_CONFIG)
    gen_config_data = gen_config_data[doc_format]

    # Create data here
    generated_data = []

    # Generate gpt sentences for fields
    gpt_data = generate_gpt_data(gen_config_data, data_field_names.keys())

    for i in range(config_params["count"]):
        fake_data = {}
        # Generate fake data fields using Faker
        data = fakerWrapper.generate_fake_data(config_params["countries"])
        for data_field in data_field_names.keys():
            if data_field not in gen_config_data["gpt_keys"] and data_field not in gen_config_data["calculate_keys"]:
                fake_data[data_field] = data[data_field]

        # Update generated sentences from GPT into the fields
        fake_data = dataService.update_gpt_data(fake_data, gpt_data)

        # Invoke transformations in data
        fake_data = dataService.transform_data(fake_data)

        generated_data.append(fake_data)

    WRITE_DATA_FILENAME = WRITE_DATA_FILEPATH + doc_format + ".json"
    # Write data into JSON file
    helper.write_json(generated_data, "%s" % WRITE_DATA_FILENAME)
    return WRITE_DATA_FILENAME
