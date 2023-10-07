import os

from components.data_renderer import imageService, helper

STYLE_CONFIG_FILE_PATH = "data/input/renderer/style_config.json"
GROUND_TRUTH_FILE_PATH = "data/output/groundtruth/"
IMAGE_FILE_PATH = 'data/output/images/'
POSITION_CONFIG_FILE_PATH = "data/input/renderer/position_config.json"
PAGE_CONFIG_FILE_PATH = "data/input/renderer/page_config.json"


def generate_documents(data_filepath, config_params, fields, doc_format):
    # Read JSON Data file for documents data
    doc_data = helper.read_json(data_filepath)
    style_config_data = helper.read_json(STYLE_CONFIG_FILE_PATH)
    page_config = helper.read_json(PAGE_CONFIG_FILE_PATH)
    position_config_data = helper.read_json(POSITION_CONFIG_FILE_PATH)

    # Render document images from this data
    images = []
    ground_truth_all = {}
    for i in range(config_params["count"]):
        # Generate image from configurations
        img, ground_truth = imageService.generate_textimage(doc_data[i], fields, style_config_data[doc_format],
                                                            page_config[doc_format], position_config_data[doc_format])
        images.append(img)
        filename = f"image{i}.png"
        image_file_path = IMAGE_FILE_PATH + doc_format + "/"
        if not os.path.exists(image_file_path):
            os.makedirs(image_file_path)
        img.save(image_file_path + filename)
        ground_truth_all[filename] = ground_truth

    ground_truth_file_path = GROUND_TRUTH_FILE_PATH + doc_format + "/"
    if not os.path.exists(ground_truth_file_path):
        os.makedirs(ground_truth_file_path)
    # Write Ground truth file in output folder
    helper.write_json(ground_truth_all, "%s" % ground_truth_file_path + "ground_truth.json")

    return doc_data, None
