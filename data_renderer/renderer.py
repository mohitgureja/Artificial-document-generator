from data_renderer import helper, imageservice


def generate_documents(filepath, config):
    # Read JSON Data file for documents data
    doc_data = helper.read_json(filepath)

    # Render document images from this data
    images = imageservice.generate_textimage(doc_data[0])

    return doc_data, None
