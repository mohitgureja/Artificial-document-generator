import json


def read_json(filename):
    with open(filename) as f:
        json_data = json.load(f)
        return json_data
