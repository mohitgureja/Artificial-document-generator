from components.artifact_engine import helper

REQUEST_FILE = "data/request/request.json"


# TODO: Need to use this module for providing recommended configurations to other components


def get_configuration(doc_format):
    config = helper.read_json(REQUEST_FILE)
    return config[doc_format]
