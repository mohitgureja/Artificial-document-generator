from components.augmentator import augment
from components.data_generator import generator
from components.data_renderer import renderer
from components.orchestrator import helper


def orchestrate(request_data, doc_format):
    """
    Starting point of the request
    Delegates the workflow to the required component
    :param request_data: Request body
    :param doc_format: Document category
    :return: JSON response with filepaths of generated data
    """
    # Transform data and configurations separately for different modules
    data_fields, generator_config, renderer_config = helper.transform_input(request_data, doc_format)

    # Required data fields in documents
    data_field_names = {key: value for key, value in data_fields.items() if data_fields[key] is True}

    # Generate fake data according to the configurations
    doc_filepath = generator.generate_data(data_field_names, generator_config, doc_format)

    # Generate fake documents according to the generated data and configurations
    groundtruth_filepath, image_filepath = None, None
    if helper.is_rendering_required(request_data):
        groundtruth_filepath, image_filepath = renderer.generate_documents(doc_filepath, renderer_config,
                                                                           data_field_names,
                                                                           doc_format)
    # Data Augmentation
    augment_image_filepath = None
    if helper.is_augment_required(request_data): augment_image_filepath = augment.augment_dataset(image_filepath)

    return helper.get_response(image_filepath, groundtruth_filepath, augment_image_filepath, doc_filepath)
