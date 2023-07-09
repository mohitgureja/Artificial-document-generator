from data_renderer import helper, imageService

STYLE_CONFIG_FILE_PATH = "data/input/renderer/style_config.json"
GROUND_TRUTH_FILE_PATH = "data/output/groundtruth/ground_truth.json"
IMAGE_FILE_PATH = 'data/output/images/'


def generate_documents(data_filepath, config_params, fields):
    # Read JSON Data file for documents data
    doc_data = helper.read_json(data_filepath)
    style_config_data = helper.read_json(STYLE_CONFIG_FILE_PATH)

    # Render document images from this data
    images = []
    ground_truth_all = {}
    for i in range(config_params["invoice_count"]):
        img, ground_truth = imageService.generate_textimage(doc_data[i], fields, style_config_data[0])
        images.append(img)
        filename = f"image{i}.png"
        img.save(IMAGE_FILE_PATH + filename)
        ground_truth_all[filename] = ground_truth

    # Write Ground truth file in output folder
    helper.write_json(ground_truth_all, "%s" % GROUND_TRUTH_FILE_PATH)

    return doc_data, None
