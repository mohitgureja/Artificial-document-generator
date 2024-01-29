from components.orchestrator.models import params_method


def get_generator_config(data):
    config_params = {"count": data.count, "countries": data.countries}
    return config_params


def get_renderer_config(data):
    config_params = {"count": data.count, "groundtruth_type": data.groundtruth_type}
    return config_params

def is_rendering_required(data):
    return data.data_rendering

def is_augment_required(data):
    if not is_rendering_required(data):
        return False
    return data.augmentation


def transform_input(request_body, doc_format):
    params = None
    try:
        params = params_method[doc_format](request_body)
    except KeyError:
        message = f'Invalid document format in the Param enumeration: "{doc_format}"'
        print("%s" % message)
        raise ValueError(message)
    return params, get_generator_config(request_body), get_renderer_config(request_body)


def get_response(image_filepath, groundtruth_filepath, augment_image_filepath, doc_filepath):
    response = {"Generated data": doc_filepath}
    if image_filepath:
        response["Generated images"] = image_filepath
    if groundtruth_filepath:
        response["Ground truth data"] = groundtruth_filepath
    if augment_image_filepath:
        response["Augmented images"] = augment_image_filepath

    return response
