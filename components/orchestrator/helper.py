def get_generator_config(data):
    config_params = {"invoice_count": data.count, "countries": data.countries}
    return config_params

def get_renderer_config(data):
    config_params = {"invoice_count": data.count, "groundtruth_type": data.groundtruth_type}
    return config_params


def get_invoice_params(request_body):
    request_body.invoice_params.set_variables()
    params = request_body.invoice_params.get_variables()
    return {k: v for k, v in params.items() if v is True}


def transform_input(request_body, doc_format):
    invoice_params = get_invoice_params(request_body)
    return invoice_params, get_generator_config(request_body), get_renderer_config(request_body)
