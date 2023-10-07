from components.artifact_engine import helper

REQUEST_FILE = "data/Request/request.json"


def get_configuration(doc_format):
    config = helper.read_json(REQUEST_FILE)
    return config[doc_format]
