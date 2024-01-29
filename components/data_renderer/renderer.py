import os
import random

from components.data_renderer import image_service, helper

doc = "default"
style_config_file_path = f"data/{doc}/input/renderer/style_config.json"
ground_truth_file_path = f"data/{doc}/output/groundtruth/"
image_file_path = f"data/{doc}/output/images/"
position_config_file_path = f"data/{doc}/input/renderer/position_config.json"
page_config_file_path = f"data/{doc}/input/renderer/page_config.json"


def get_random_template(page_config_data, position_config_data):
    random_template_nr = random.choice(list(page_config_data.keys()))
    return page_config_data[random_template_nr], \
        position_config_data[random_template_nr]


def generate_documents(data_filepath, config_params, fields, doc_format):
    print("\n------------------- Starting data rendering -------------------\n")

    global style_config_file_path, ground_truth_file_path, image_file_path, position_config_file_path, page_config_file_path
    style_config_file_path = f"data/{doc_format}/input/renderer/style_config.json"
    ground_truth_file_path = f"data/{doc_format}/output/groundtruth/"
    image_file_path = f"data/{doc_format}/output/images/"
    position_config_file_path = f"data/{doc_format}/input/renderer/position_config.json"
    page_config_file_path = f"data/{doc_format}/input/renderer/page_config.json"

    # Read JSON Data file for documents data
    doc_data = helper.read_json(data_filepath)
    style_config = helper.read_json(style_config_file_path)
    page_config_data = helper.read_json(page_config_file_path)
    position_config_data = helper.read_json(position_config_file_path)
    # Render document person from this data
    images = []
    ground_truth_all = {}
    for i in range(config_params["count"]):

        # Pick random template from the available templates
        page_config, position_config = get_random_template(page_config_data,
                                                           position_config_data)

        # Generate image from configurations
        img, ground_truth = image_service.generate_textimage(doc_data[i], fields, style_config,
                                                             page_config, position_config, doc_format)
        images.append(img)
        filename = f"image{i}.png"
        if not os.path.exists(image_file_path):
            os.makedirs(image_file_path)
        img.save(image_file_path + filename)
        ground_truth_all[filename] = ground_truth
    if not os.path.exists(ground_truth_file_path):
        os.makedirs(ground_truth_file_path)
    # Write Ground truth file in output folder
    helper.write_json(ground_truth_all, "%s" % ground_truth_file_path + "ground_truth.json")

    return ground_truth_file_path, image_file_path
