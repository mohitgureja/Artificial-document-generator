from data_generator import helper, fakerWrapper

TEST_DATA_FILENAME = "data/test.json"
WRITE_INVOICE_FILENAME = "data/invoices.json"


def generate_data(data_fields, config_params):
    # # JSON Data file for testing
    # json_data = helper.read_json(TEST_DATA_FILENAME)

    # Required data fields in documents
    data_field_names = [key for key in data_fields.keys() if data_fields[key] is True]

    # Create data here
    generated_data = []
    # Need this data for test purpose for data renderer
    for i in range(config_params["invoice_count"]):
        fake_data = {}
        for data_field in data_field_names:
            data = fakerWrapper.generate_fake_data(data_field, config_params["countries"])
            fake_data[data_field] = data
        generated_data.append(fake_data)

    # Write data into JSON file
    helper.write_json(generated_data, "%s" % WRITE_INVOICE_FILENAME)
    return WRITE_INVOICE_FILENAME
