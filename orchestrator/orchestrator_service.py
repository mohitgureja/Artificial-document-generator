from data_generator import generator
from data_renderer import renderer
from orchestrator import helper


def orchestrate(request_data):
    # Transform data and configurations separately for different modules
    params, generator_config, renderer_config = helper.transform_input(request_data)

    # Generate fake data according to the configurations
    doc_filepath = generator.generate_data(params, generator_config)

    # Generate fake document images according to the configurations
    doc_images, groundtruth_data = renderer.generate_documents(doc_filepath, renderer_config)
    # print(doc_images)
    return doc_images
