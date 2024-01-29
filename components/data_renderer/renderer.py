import os
import random

from components.data_renderer import imageService, helper

STYLE_CONFIG_FILE_PATH = "data/input/renderer/style_config.json"
GROUND_TRUTH_FILE_PATH = "data/output/groundtruth/"
IMAGE_FILE_PATH = 'data/output/images/'
POSITION_CONFIG_FILE_PATH = "data/input/renderer/position_config.json"
PAGE_CONFIG_FILE_PATH = "data/input/renderer/page_config.json"


def get_random_template(style_config_data, page_config_data, position_config_data, doc_format):
    random_template_nr = random.choice(list(page_config_data[doc_format].keys()))
    return style_config_data[doc_format], page_config_data[doc_format][random_template_nr], \
        position_config_data[doc_format][random_template_nr]


def generate_documents(data_filepath, config_params, fields, doc_format):
    print("\n------------------- Starting data rendering -------------------\n")

    # Read JSON Data file for documents data
    doc_data = helper.read_json(data_filepath)
    style_config_data = helper.read_json(STYLE_CONFIG_FILE_PATH)
    page_config_data = helper.read_json(PAGE_CONFIG_FILE_PATH)
    position_config_data = helper.read_json(POSITION_CONFIG_FILE_PATH)
    image_file_path = IMAGE_FILE_PATH + doc_format + "/"
    ground_truth_file_path = GROUND_TRUTH_FILE_PATH + doc_format + "/"
    # Render document person from this data
    images = []
    ground_truth_all = {}
    for i in range(config_params["count"]):

        # Pick random template from the available templates
        style_config, page_config, position_config = get_random_template(style_config_data, page_config_data,
                                                                         position_config_data, doc_format)

        # Generate image from configurations
        img, ground_truth = imageService.generate_textimage(doc_data[i], fields, style_config,
                                                            page_config, position_config)
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
