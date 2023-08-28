import random
import textwrap

from PIL import Image, ImageFont, ImageDraw

from components.data_renderer import tableService, helper, pageService

PAGE_CONFIG_FILE_PATH = "data/input/renderer/page_config.json"

POSITION_CONFIG_FILE_PATH = "data/input/renderer/position_config.json"


def generate_textimage(data, fields, style_config_data):
    """
    Render image according to the data and field_config provided
    :param data:
    :param fields:
    :param style_config_data:
    :return:
    """
    position_config_data = helper.read_json(POSITION_CONFIG_FILE_PATH)
    page_config = helper.read_json(PAGE_CONFIG_FILE_PATH)

    page_matrix = pageService.create_page_matrix(page_config)  # Matrix of the form [[[tuple(x1, y1), tuple(x2, y2)]]]

    top_margin = page_matrix[0][0][1][1]
    l = len(page_matrix[0])
    y2_prev = [top_margin] * l
    x2_prev = [page_matrix[0][l - 1][1][0]] * l
    x1_prev = [page_matrix[0][0][0][0]] * l

    def test_side_semantics(x1_c, x2_c):
        for i in range(l):
            if x2_prev[i] > x1_c:
                if x2_c > x1_prev[i] or x1_prev[i] < x1_c:
                    return True
            elif x2_c > x2_prev[i] > x1_c:
                return True
        return False

    def test_layout_semantics(x1_c, y1_c, x2_c, y2_c, row, column, cropped, count=0):
        if count == 10:
            raise ValueError("Maximum recursion limit reached. Creating default coordinates")

        # If the column is not used earlier
        if y2_prev[column] == top_margin:
            if y2_prev[column] > y1_c and test_side_semantics(x1_c, x2_c):
                print("Semantic Layout test failed at unused column: ", row, column)
                x1_c = random.randint(page_matrix[row][column][0][0], page_matrix[row][column][1][0])
                y1_c = random.randint(page_matrix[row][column][0][1], page_matrix[row][column][1][1])
                x2_c, y2_c = create_b_box(cropped, x1_c, y1_c)
                count += 1
                x1_c, y1_c, x2_c, y2_c, count = test_layout_semantics(x1_c, y1_c, x2_c, y2_c, row, column, cropped,
                                                                      count)
            else:
                x1_prev[column], x2_prev[column], y2_prev[column] = x1_c, x2_c, y2_c
        else:
            x1_c = x1_prev[column]
            x2_c, y2_c = create_b_box(cropped, x1_c, y1_c)
            if y2_prev[column] > y1_c and test_side_semantics(x1_c, x2_c):
                print("Semantic Layout test failed at already used column: ", row, column)
                y1_c = random.randint(page_matrix[row][column][0][1], page_matrix[row][column][1][1])
                count += 1
                x1_c, y1_c, x2_c, y2_c, count = test_layout_semantics(x1_c, y1_c, x2_c, y2_c, row, column, cropped,
                                                                      count)
            else:
                if x2_c > x2_prev[column]:
                    x2_prev[column] = x2_c
                y2_prev[column] = y2_c
        print("Semantic test passed. ")
        count += 1
        return x1_c, y1_c, x2_c, y2_c, count

    # Image size
    width_img, height_img = page_config["width"], page_config["height"]
    img = Image.new('RGB', (width_img, height_img), "white")
    img_draw = ImageDraw.Draw(img)
    ground_truth = {}

    for block in position_config_data.keys():
        block = position_config_data[block]
        row, column = block["block_position"]
        x1 = random.randint(page_matrix[row][column][0][0], page_matrix[row][column][1][0])
        y1 = random.randint(page_matrix[row][column][0][1], page_matrix[row][column][1][1])
        # x1 = random.randint(block["position"]["x1"], block["position"]["x2"])
        # y1 = random.randint(block["position"]["y1"], block["position"]["y2"])
        if block["hasTable"]:
            img, ground_truth = tableService.draw_table(block, style_config_data, img, ground_truth, data, x1, y1)
        if "data_fields" in block:
            img_new, b_box, ground_truth = get_block_image(block, data, fields, ground_truth, style_config_data, x1, y1)
            cropped = img_new.crop(b_box)
            x2, y2 = create_b_box(cropped, x1, y1)
            if page_config["header_line"] and block["is_header"]:
                img_draw.line([(x1, y2),
                               (x2, y2)], fill="black", width=3)
                y2_prev[column] = y2
            else:
                try:
                    x1, y1, x2, y2, count = test_layout_semantics(x1, y1, x2, y2, row, column, cropped)
                except ValueError as e:
                    print("Can not find semantics for this block. ", e)
            img.paste(cropped, (x1, y1, x2, y2))
    return img, ground_truth


def create_b_box(cropped, x1, y1):
    y2 = y1 + cropped.height
    x2 = x1 + cropped.width
    return x2, y2


def get_block_image(block, data, fields, ground_truth, style_config_data, x1, y1):
    img = Image.new('RGB', (2480, 3508), "white")
    img_draw = ImageDraw.Draw(img)
    w, h = 0, 0
    x1_block, y1_block, x2_block, y2_block = x1, y1, 0, 0
    width_field = 0
    for data_field in block["data_fields"]:
        direction = block["direction"]
        field = block["data_fields"][data_field]

        # Check if data is generated by generator
        if data_field not in fields:
            continue
        text = data[data_field]

        # If field has a key name
        if field["key"]:
            text = get_keytext(field, text)

        # Get style configurations
        field_style_config = style_config_data[data_field]
        font = get_font(field_style_config)

        # If field value is a list of strings
        if field["isList"]:
            text = "\n".join(text)

        # If a field has dependency on a previous rendered field
        # if field["has_dependent_field"]:
        #     direction = field["key_direction"]
        #     x1 = ground_truth[field["previous_key"]]["x1"]
        #     y1 = ground_truth[field["previous_key"]]["y1"]
        #     h = ground_truth[field["previous_key"]]["y2"] - y1
        #     w = ground_truth[field["previous_key"]]["x2"] - x1

        if direction == "down":
            y1 = y1 + field_style_config["margin-top"] + h
            h = 0
        elif direction == "right":
            x1 = x1 + field_style_config["margin-left"] + w
            h = 0

        w = field_style_config["width"]
        width = 0
        split_text = str(text).split("\n")
        for text_line in split_text:
            wrapped_text = textwrap.wrap(text_line, width=w)
            for line in wrapped_text:
                img_draw.text((x1, y1 + h), str(line.strip()), fill=(0, 0, 0), font=font)
                # Block highest width
                width = font.getsize(line)[0]
                if width > width_field:
                    width_field = width
                h += font.getsize(line)[1]
            h += 10
        y2_block = y1 + h
        x2_block = x1 + width_field
        # Ground Truth Data for each field
        ground_truth[data_field] = {"content": text, "x1": x1, "x2": x1 + width, "y1": y1, "y2": y1 + h}
    return img, (x1_block - 10, y1_block - 10, x2_block + 10, y2_block + 10), ground_truth


def get_font(field_config):
    font = ImageFont.truetype(field_config["font"], size=field_config["font_size"])
    return font


def get_keytext(field, text):
    field_direction = field["key_direction"]
    # TODO: Not generic (Need to generalize it to every field)
    keyname = random.choice(field["key_name"])
    if field_direction == "top":
        text = keyname + "\n" + str(text)
    elif field_direction == "left":
        text = keyname + str(text)
    return text
