from components.data_generator import data_service, faker_wrapper, helper, gpt_service

doc = "default"
data_gen_config = f"data/{doc}/input/generator/config.json"
write_data_filepath = f"data/{doc}/input/renderer/"
response_file_path = f"data/{doc}/input/renderer/gpt_response.json"


def generate_gpt_data(config_data, data_fields):
    """
    Generate data for field variables using GPT model
    :param data_fields:
    :param config_data:
    :return:
    """
    data = {}
    if config_data["gpt_enabled"]:
        print("Generating data from GPT\n")
        print("It might take a few minutes.")
        config_data = config_data["gpt_config"]
        for key in config_data["gpt_keys"]:
            if key in data_fields:
                query = config_data["queries"][key]
                data = gpt_service.generate_gpt_data(data, key, query,
                                                     config_data["gpt_output"][key])
        print(response_file_path)
        helper.write_json(data, response_file_path)
    else:
        print("Getting already generated data from gpt response file")
        gpt_response = helper.read_json(response_file_path)
        for key in gpt_response.keys():
            # if key in data_fields:
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
    print("\n------------------- Starting data generation -------------------\n")
    global data_gen_config, write_data_filepath, response_file_path
    data_gen_config = f"data/{doc_format}/input/generator/config.json"
    write_data_filepath = f"data/{doc_format}/input/renderer/"
    response_file_path = f"data/{doc_format}/input/renderer/gpt_response.json"

    # JSON Data file for configurations
    gen_config_data = helper.read_json(data_gen_config)

    # Create data here
    generated_data = []

    # Generate gpt sentences for fields
    data_field_keys = data_field_names.keys()
    gpt_data = generate_gpt_data(gen_config_data, data_field_keys)

    # Total number of data person
    for i in range(config_params["count"]):
        fake_data = {}
        # Generate fake data fields using Faker
        data = faker_wrapper.generate_fake_data(config_params["countries"])

        for data_field in data_field_keys:
            # if (data_field not in gen_config_data["gpt_keys"] and data_field not in gen_config_data["calculate_keys"]) or data_field in gen_config_data["faker_keys"]:
            if data_field in gen_config_data["faker_keys"]:
                faker_key = gen_config_data["faker_keys"][data_field]
                fake_data[data_field] = data[faker_key]

        # Update generated sentences from GPT into the fields
        fake_data = data_service.update_gpt_data(fake_data, gpt_data)

        # Invoke transformations in data
        fake_data = data_service.transform_data(fake_data, gen_config_data, doc_format)

        generated_data.append(fake_data)

    WRITE_DATA_FILENAME = write_data_filepath + doc_format + ".json"
    # Write data into JSON file
    helper.write_json(generated_data, "%s" % WRITE_DATA_FILENAME)
    return WRITE_DATA_FILENAME
