from components.orchestrator.models import Params


def get_generator_config(data):
    config_params = {"count": data.count, "countries": data.countries}
    return config_params


def get_renderer_config(data):
    config_params = {"count": data.count, "groundtruth_type": data.groundtruth_type}
    return config_params


def get_invoice_params(request_body):
    request_body.invoice_params.set_variables()
    params = request_body.invoice_params.get_variables()
    return {k: v for k, v in params.items() if v is True}


def get_receipt_params(request_body):
    request_body.receipt_params.set_variables()
    params = request_body.receipt_params.get_variables()
    return {k: v for k, v in params.items() if v is True}


params_method = {
    Params.invoice: get_invoice_params,
    Params.receipt: get_receipt_params
}


# TODO: Test the enum code
def transform_input(request_body, doc_format):
    param = None
    try:
        param = Params(doc_format)
    except ValueError:
        print("Invalid document format in the Param enumeration")
    params = params_method[param](request_body)
    return params, get_generator_config(request_body), get_renderer_config(request_body)
