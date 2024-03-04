import json

from PIL import ImageFont


def read_json(filepath):
    with open(filepath) as f:
        json_data = json.load(f)
        return json_data


def write_json(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f)


def get_font(field_config):
    font = ImageFont.truetype(field_config["font"], size=field_config["font_size"])
    return font


def update_ground_truth(ground_truth_data, update_keys, diff):
    """
    Update the ground truth data for all the fields with provided pixel difference
    :param ground_truth_data: original ground data
    :param update_keys: keys to be updated
    :param diff: difference in pixels
    :return: updated ground data
    """

    def update_key_in_nested_structure(data, key_to_find, diff):
        if isinstance(data, dict):
            if key_to_find in data:
                if isinstance(data[key_to_find], dict):
                    if "x1" in data[key_to_find]:
                        data[key_to_find]["x1"] = data[key_to_find]["x1"] + diff[0]
                        data[key_to_find]["x2"] = data[key_to_find]["x2"] + diff[1]
                        data[key_to_find]["y1"] = data[key_to_find]["y1"] + diff[2]
                        data[key_to_find]["y2"] = data[key_to_find]["y2"] + diff[3]
                        return data
                elif isinstance(data[key_to_find], list):
                    for i in range(len(data[key_to_find])):
                        if isinstance(data[key_to_find][i], dict):
                            if "x1" in data[key_to_find][i]:
                                data[key_to_find][i]["x1"] = data[key_to_find][i]["x1"] + diff[0]
                                data[key_to_find][i]["x2"] = data[key_to_find][i]["x2"] + diff[1]
                                data[key_to_find][i]["y1"] = data[key_to_find][i]["y1"] + diff[2]
                                data[key_to_find][i]["y2"] = data[key_to_find][i]["y2"] + diff[3]
                                return data
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    data[key] = update_key_in_nested_structure(value, key_to_find, diff)
        elif isinstance(data, list):
            for i in range(len(data)):
                if isinstance(data[i], (dict, list)):
                    data[i] = update_key_in_nested_structure(data[i], key_to_find, diff)
        return data

    for key in set(update_keys):
        ground_truth_data = update_key_in_nested_structure(ground_truth_data, key, diff)

    return ground_truth_data
