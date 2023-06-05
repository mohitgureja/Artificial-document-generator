from data_renderer import helper, imageservice


def generate_documents(filepath, config_params, fields):
    # Read JSON Data file for documents data
    doc_data = helper.read_json(filepath)
    field_config_data = helper.read_json("data/test_config.json")

    # Render document images from this data
    images = []
    for i in range(config_params["invoice_count"]):
        images.append(imageservice.generate_textimage(doc_data[0], fields, field_config_data[i]))

    return doc_data, None
