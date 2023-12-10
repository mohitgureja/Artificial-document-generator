from components.data_generator import generator
from components.data_renderer import renderer
from components.orchestrator import helper

"""
    :param request_data: 
    :return: 
"""


def orchestrate(request_data, doc_format):
    # Transform data and configurations separately for different modules
    data_fields, generator_config, renderer_config = helper.transform_input(request_data, doc_format)

    # Required data fields in documents
    data_field_names = {key: value for key, value in data_fields.items() if data_fields[key] is True}

    # Generate fake data according to the configurations
    doc_filepath = generator.generate_data(data_field_names, generator_config, doc_format)

    # Generate fake document person according to the configurations
    doc_images, groundtruth_data = renderer.generate_documents(doc_filepath, renderer_config, data_field_names,
                                                               doc_format)
    # print(doc_images)
    return doc_images
