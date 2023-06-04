from data_generator import helper

TEST_DATA_FILENAME = "data/test.json"
WRITE_INVOICE_FILENAME = "data/invoices.json"


def generate_data(data_fields, config_params):
    # JSON Data file for testing
    json_data = helper.read_json(TEST_DATA_FILENAME)

    # Required data fields in documents
    data_field_names = [key for key in data_fields.keys() if data_fields[key] is True]
    print(data_field_names)

    # Create data here
    generated_data = []
    # Need this data for test purpose for data renderer
    for i in range(config_params["invoice_count"]):
        generated_data.append({key: json_data[i][key] for key in data_fields.keys() if data_fields[key] is True})

    # Write data into JSON file
    helper.write_json(generated_data, "%s" % WRITE_INVOICE_FILENAME)
    return WRITE_INVOICE_FILENAME
