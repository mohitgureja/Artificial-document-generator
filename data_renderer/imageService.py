import random
import textwrap

from PIL import Image, ImageFont, ImageDraw

from data_renderer import helper

POSITION_CONFIG_FILE_PATH = "data/input/renderer/position_config.json"


def generate_textimage(data, fields, style_config_data):
    position_config_data = helper.read_json(POSITION_CONFIG_FILE_PATH)

    # Image size
    width_img, height_img = 2480, 3508
    img = Image.new('RGB', (width_img, height_img), "white")
    img_draw = ImageDraw.Draw(img)

    ground_truth = {}

    for block in position_config_data.keys():
        block = position_config_data[block]
        x1 = random.randint(block["position"]["x1"], block["position"]["x2"])
        y1 = random.randint(block["position"]["y1"], block["position"]["y2"])
        direction = block["direction"]
        w, h = 0, 0
        for data_field in block["data_fields"]:
            field = block["data_fields"][data_field]
            if data_field not in fields:
                continue
            text = data[data_field]

            if field["key"]:
                field_direction = field["key_direction"]
                rech_nr = random.choice(field["key_name"])
                if field_direction == "top":
                    text = rech_nr + "\n" + str(text)
                elif field_direction == "left":
                    text = rech_nr + str(text)
            config = style_config_data[data_field]
            if direction == "down":
                y1 = y1 + config["margin-top"] + h
            elif direction == "right":
                x1 = x1 + config["margin-left"] + w
                h = 0

            font = ImageFont.truetype(config["font"], size=config["font_size"])
            w = config["width"]

            split_text = str(text).split("\n")
            for text_line in split_text:
                wrapped_text = textwrap.wrap(text_line, width=w)
                for line in wrapped_text:
                    img_draw.text((x1, y1 + h), str(line), fill=(0, 0, 0), font=font)
                    h += font.getsize(line)[1]

            # Ground Truth Data for each field
            ground_truth[data_field] = {"content": text, "x1": x1, "x2": x1 + w, "y1": y1, "y2": y1 + h}
    return img, ground_truth
