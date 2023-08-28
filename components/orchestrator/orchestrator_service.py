from components.data_generator import generator
from components.data_renderer import renderer
from components.orchestrator import helper

"""
    :param request_data: 
    :return: 
"""


def orchestrate(request_data):
    # Transform data and configurations separately for different modules
    data_fields, generator_config, renderer_config = helper.transform_input(request_data)

    # Required data fields in documents
    data_field_names = {key: value for key, value in data_fields.items() if data_fields[key] is True}

    # Generate fake data according to the configurations
    doc_filepath = generator.generate_data(data_field_names, generator_config)

    # Generate fake document images according to the configurations
    doc_images, groundtruth_data = renderer.generate_documents(doc_filepath, renderer_config, data_field_names)
    # print(doc_images)
    return doc_images
