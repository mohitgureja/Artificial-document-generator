import json


def read_json(filepath):
    with open(filepath) as f:
        json_data = json.load(f)
        return json_data


def write_json(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f)
