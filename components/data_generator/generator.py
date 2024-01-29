from components.data_generator import dataService, fakerWrapper, helper, gptService

DATA_GEN_CONFIG = "data/input/generator/config.json"
WRITE_DATA_FILEPATH = "data/input/renderer/"
RESPONSE_FILE_PATH = "data/input/renderer/gpt_response.json"


def generate_gpt_data(config_data, data_fields, doc_format):
    """
    Generate data for field variables using GPT model
    :param doc_format:
    :param data_fields:
    :param config_data:
    :return:
    """
    data = {doc_format: {}}
    if config_data["gpt_enabled"]:
        print("Generating data from GPT\n")
        print("It might take a few minutes.")
        config_data = config_data["gpt_config"]
        for key in config_data["gpt_keys"]:
            if key in data_fields:
                query = config_data["queries"][key]
                data[doc_format] = gptService.generate_gpt_data(data[doc_format], key, query,
                                                                config_data["gpt_output"][key])
        helper.write_json(data, RESPONSE_FILE_PATH)
    else:
        print("Getting already generated data from gpt response file")
        gpt_response = helper.read_json("data/input/renderer/gpt_response.json")
        for key in gpt_response[doc_format].keys():
            # if key in data_fields:
            data[doc_format][key] = gpt_response[doc_format][key]
    return data[doc_format]


def assign_field_data(data, data_field_keys, gen_config_data):
    return data


def generate_data(data_field_names, config_params, doc_format):
    """
    Generate fake data for required field variables
    :param doc_format:
    :param data_field_names:
    :param config_params:
    :return:
    """
    print("\n------------------- Starting data generation -------------------\n")

    # JSON Data file for configurations
    gen_config_data = helper.read_json(DATA_GEN_CONFIG)
    gen_config_data = gen_config_data[doc_format]

    # Create data here
    generated_data = []

    # Generate gpt sentences for fields
    data_field_keys = data_field_names.keys()
    gpt_data = generate_gpt_data(gen_config_data, data_field_keys, doc_format)

    # Total number of data person
    for i in range(config_params["count"]):
        fake_data = {}
        # Generate fake data fields using Faker
        data = fakerWrapper.generate_fake_data(config_params["countries"])
        # Assign general generated fake data to required fields
        data = assign_field_data(data, data_field_keys, gen_config_data["faker_keys"])
        for data_field in data_field_keys:
            # if (data_field not in gen_config_data["gpt_keys"] and data_field not in gen_config_data["calculate_keys"]) or data_field in gen_config_data["faker_keys"]:
            if data_field in gen_config_data["faker_keys"]:
                faker_key = gen_config_data["faker_keys"][data_field]
                fake_data[data_field] = data[faker_key]

        # Update generated sentences from GPT into the fields
        fake_data = dataService.update_gpt_data(fake_data, gpt_data)

        # Invoke transformations in data
        fake_data = dataService.transform_data(fake_data, gen_config_data)

        generated_data.append(fake_data)

    WRITE_DATA_FILENAME = WRITE_DATA_FILEPATH + doc_format + ".json"
    # Write data into JSON file
    helper.write_json(generated_data, "%s" % WRITE_DATA_FILENAME)
    return WRITE_DATA_FILENAME
