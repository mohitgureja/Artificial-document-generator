import glob
import math
import os
import random
import textwrap

from PIL import Image, ImageFont, ImageDraw, ImageOps

from components.data_renderer import tableService, pageService

BACKGROUND_IMAGE_PATH = "data/input/resources/background/"


def get_bordered_image(cropped, block, style_config):
    if "border_block" in block:
        if block["border_block"]:
            border_size = style_config["border"]["border_size"]
            cropped = ImageOps.expand(cropped, border=border_size, fill="black")
    return cropped


def calculate_overlap_area(rect1, rect2):
    # Determine the coordinates of the overlapping region
    x1 = max(rect1[0], rect2[0])
    y1 = max(rect1[1], rect2[1])
    x2 = min(rect1[0] + rect1[2], rect2[0] + rect2[2])
    y2 = min(rect1[1] + rect1[3], rect2[1] + rect2[3])

    # Calculate the area of the overlapping region
    overlap_width = x2 - x1
    overlap_height = y2 - y1
    overlap_area = overlap_width * overlap_height

    return overlap_area


def generate_textimage(data, fields, style_config_data, page_config, position_config_data):
    """
    Render image according to the data and field configurations provided
    :param position_config_data:
    :param page_config:
    :param data:
    :param fields:
    :param style_config_data:
    :return:
    """

    page_matrix = pageService.create_page_matrix(page_config)  # Matrix of the form [[[tuple(x1, y1), tuple(x2, y2)]]]

    top_margin = page_matrix[0][0][1][1]
    l = len(page_matrix[0])
    x1_used_col = [0] * l
    rendered_data = []
    overlap_area = {}

    def test_previous_intersection(x1_c, x2_c, y1_c, y2_c):
        """
        Check if current position bbox overlap with any of the previous blocks
        Uses global variables
        :param x1_c:
        :param x2_c:
        :param y1_c:
        :param y2_c:
        :return:
        """
        if rendered_data:
            for data_row in rendered_data:
                x1_data, y1_data, x2_data, y2_data = data_row[0], data_row[1], data_row[2], data_row[3]
                if y2_data < y1_c or y1_data > y2_c or x1_c > x2_data or x1_data > x2_c:
                    continue
                else:
                    area = calculate_overlap_area((x1_c, y1_c, x2_c - x1_c, y2_c - y1_c),
                                                  (x1_data, y1_data, x2_data - x1_data, y2_data - y1_data))
                    overlap_area[area] = x1_c, y1_c, x2_c, y2_c
                    return False
        return True

    def test_layout_semantics(x1_c, y1_c, x2_c, y2_c, row, column, cropped, count=0):
        """
        Check and update the layout semantics for current positions
        Uses global variables
        :param x1_c:
        :param y1_c:
        :param x2_c:
        :param y2_c:
        :param row:
        :param column:
        :param cropped:
        :param count:
        :return:
        """
        if count == 10:
            raise ValueError("Maximum recursion limit reached.")

        # If current column is not already used earlier
        if x1_used_col[column] == 0:
            if test_previous_intersection(x1_c, x2_c, y1_c, y2_c):
                rendered_data.append([x1_c, y1_c, x2_c, y2_c])
                x1_used_col[column] = x1_c
            else:
                print("Semantic Layout test failed at unused column: ", row, column)
                x1_c = random.randint(page_matrix[row][column][0][0], page_matrix[row][column][1][0])
                y1_c = random.randint(page_matrix[row][column][0][1], page_matrix[row][column][1][1])
                x2_c, y2_c = create_b_box(cropped, x1_c, y1_c)
                count += 1
                x1_c, y1_c, x2_c, y2_c, count = test_layout_semantics(x1_c, y1_c, x2_c, y2_c, row, column, cropped,
                                                                      count)
        # If current column is already used by earlier block
        else:
            x1_c = x1_used_col[column]
            x2_c, y2_c = create_b_box(cropped, x1_c, y1_c)
            if test_previous_intersection(x1_c, x2_c, y1_c, y2_c):
                rendered_data.append([x1_c, y1_c, x2_c, y2_c])
            else:
                print("Semantic Layout test failed at already used column: ", row, column)
                y1_c = random.randint(page_matrix[row][column][0][1], page_matrix[row][column][1][1])
                count += 1
                x2_c, y2_c = create_b_box(cropped, x1_c, y1_c)
                x1_c, y1_c, x2_c, y2_c, count = test_layout_semantics(x1_c, y1_c, x2_c, y2_c, row, column, cropped,
                                                                      count)
        print("Semantic test passed. ")
        count += 1
        return x1_c, y1_c, x2_c, y2_c, count

    def test_layout(x1, y1, x2, y2, row, column, cropped, block, max_try_position):
        tried_block = []
        overlap_area.clear()
        while max_try_position >= 0:
            if max_try_position == 0:
                print("Can not finalise semantics for this block, trying block with minimum overlap area")
                min_area = min(overlap_area, key=lambda k: int(k))
                x1, y1, x2, y2 = overlap_area[min_area]
                print(f'Minimum overlap area: {x1}, {y1}, {x2}, {y2}')
                break
            try:
                if (row, column) not in tried_block:
                    x1, y1, x2, y2, count = test_layout_semantics(x1, y1, x2, y2, row, column, cropped)
                    break
            except ValueError as e:
                print("Can not find semantics for this block, trying another block.", e)
                tried_block.append((row, column))
                max_try_position -= 1
            row, column = random.choice(block["block_position"])
            if (row, column) not in tried_block:
                diff_x = x2 - x1
                diff_y = y2 - y1
                x1 = random.randint(page_matrix[row][column][0][0], page_matrix[row][column][1][0])
                y1 = random.randint(page_matrix[row][column][0][1], page_matrix[row][column][1][1])
                x2 = x1 + diff_x
                y2 = y1 + diff_y
        return x1, y1, x2, y2

    # Image size
    width_img, height_img = page_config["width"], page_config["height"]
    img = Image.new('RGBA', (width_img, height_img))
    image_files = glob.glob(os.path.join(BACKGROUND_IMAGE_PATH, "*.jpg"))
    filepath = random.choice(image_files)
    background = Image.open(filepath)
    background = background.resize(img.size)
    img.paste(background, (0, 0))
    img_draw = ImageDraw.Draw(img)
    ground_truth = {}

    # Generate image using block by block configurations
    for block in position_config_data.keys():
        block = position_config_data[block]
        row, column = random.choice(block["block_position"])
        x1 = random.randint(page_matrix[row][column][0][0], page_matrix[row][column][1][0])
        y1 = random.randint(page_matrix[row][column][0][1], page_matrix[row][column][1][1])

        # If block is an image
        if block["is_image"]:
            img_path = data[block["data_field"]]
            logo = Image.open(img_path)

            mode = logo.mode
            # Handle each mode separately
            if mode == 'P':
                # Convert image2 to mode RGB before pasting
                logo = logo.convert('RGBA')
            elif mode == 'L':
                # Convert image2 to mode RGBA before pasting
                logo = logo.convert('RGBA')
            elif mode == 'CMYK':
                # Convert image2 to mode RGB before pasting
                logo = logo.convert('RGB')
            bbox = logo.getbbox()
            x1, y1, x2, y2 = test_layout(x1, y1, x1 + bbox[2] - bbox[0], y1 + bbox[3] - bbox[1], row,
                                         column, logo, block, len(block["block_position"]))

            img.paste(logo, (x1, y1, x2, y2))

        # If block is a table
        elif block["has_table"]:
            cropped, tb_fields, x2, y2, ground_truth = tableService.draw_table(block, style_config_data, ground_truth,
                                                                               data, x1, y1, page_config)
            b_box_old = (x1, y1, x2, y2)
            x1, y1, x2, y2 = test_layout(x1, y1, x2, y2, row, column, cropped, block,
                                         len(block["block_position"]))
            b_box_new = (x1, y1, x2, y2)
            ground_truth = tableService.get_updated_ground_truth(b_box_old, b_box_new, tb_fields, ground_truth)

            img.paste(cropped, (x1, y1, x2, y2), cropped)
        # If block has data fields
        elif "data_fields" in block:
            img_new, b_box, ground_truth = get_block_image(block, data, fields, ground_truth, style_config_data, x1, y1,
                                                           page_config)
            cropped = img_new.crop(b_box)
            cropped = get_bordered_image(cropped, block, style_config_data)
            x2, y2 = create_b_box(cropped, x1, y1)
            x1, y1, x2, y2 = test_layout(x1, y1, x2, y2, row, column, cropped, block,
                                         len(block["block_position"]))
            mode = cropped.mode
            # Handle each mode separately
            if mode == 'P':
                # Convert image2 to mode RGB before pasting
                cropped = cropped.convert('RGBA')
            elif mode == 'L':
                # Convert image2 to mode RGBA before pasting
                cropped = cropped.convert('RGBA')
            elif mode == 'CMYK':
                # Convert image2 to mode RGB before pasting
                cropped = cropped.convert('RGB')

            img.paste(cropped, (x1, y1, x2, y2), cropped)
    return img, ground_truth


def create_b_box(cropped, x1, y1):
    y2 = y1 + cropped.height
    x2 = x1 + cropped.width
    return x2, y2


def get_block_image(block, data, fields, ground_truth, style_config_data, x1, y1, page_config):
    """
    Generate separate person for each block using position and configuration
    :param block:
    :param data:
    :param fields:
    :param ground_truth:
    :param style_config_data:
    :param x1:
    :param y1:
    :param page_config:
    :return:
    """
    background_color = (255, 255, 255, 0)
    img = Image.new('RGBA', (page_config["width"], page_config["height"]), background_color)
    img_draw = ImageDraw.Draw(img)
    w, h, l = 0, 0, 1
    x1_block, y1_block, x2_block, y2_block = x1, y1, 0, 0
    width_field = 0
    block_data = False

    # If block has a header key
    if block["is_key"]:
        keyname = block["keyname"]
        field_style_config = style_config_data[keyname.lower()]
        font = get_font(field_style_config)
        img_draw.text((x1, y1 + h), str(keyname.strip()), fill=field_style_config["font_color"], font=font)
        # Block highest width
        width = font.getsize(keyname)[0]
        if width > width_field:
            width_field = width
        h += font.getsize(keyname)[1]
        img_draw.line([(x1, y1 + h + 2), (x1 + width, y1 + h + 2)], fill="black", width=3)
        h += 10

        if keyname.lower() in data and data[keyname.lower()] and all(
                isinstance(item, dict) for item in data[keyname.lower()]):
            data = data[block["keyname"].lower()]
            l = len(data)
            # Ground Truth Data for block heading
            if l > 0:
                block_data = True
                ground_truth[keyname] = [{"content": keyname, "x1": x1, "x2": x1 + width, "y1": y1, "y2": y1 + h}]
        else:
            ground_truth[keyname] = {"content": keyname, "x1": x1, "x2": x1 + width, "y1": y1, "y2": y1 + h}
            x2_block = x1 + width
            y2_block = y1 + h + 2
        h += 20

    col_range = block["block_range"]

    # Get pixels upto which data rendering is allowed
    pixels = (sum(page_config["columns"]["size"][:col_range]) * page_config["width"]) / 100

    for i in range(0, l):
        if block_data:
            ground_truth[block["keyname"]].append({})
        block_length = len(block["data_fields"])
        for j, data_field in enumerate(block["data_fields"]):
            direction = block["direction"]
            field = block["data_fields"][data_field]

            # Check if data is generated by generator
            if data_field not in fields:
                continue
            if block_data:
                text = data[i][data_field]
            else:
                text = data[data_field]

            # If field has a key name
            if field["key"]:
                text = get_keytext(field, text)

            # Get style configurations
            field_style_config = style_config_data[data_field]
            font = get_font(field_style_config)

            # If field value is a list of strings
            if isinstance(text, list):
                text = "\n".join(text)

            if direction == "down":
                y1 = y1 + field_style_config["margin-top"] + h
                h = 0
            elif direction == "right":
                x1 = x1 + field_style_config["margin-left"] + w
                h = 0

            w = field_style_config["width"]
            width = 0
            split_text = str(text).split("\n")

            # Renders text line by line on the canvas
            for text_line in split_text:
                if not text_line:
                    text_line = "Default"
                diff = pixels - x1
                text_width_pixels = img_draw.textsize(text_line, font)[0]
                text_width = len(text_line)
                w = (text_width * diff) / text_width_pixels
                wrapped_text = textwrap.wrap(text_line, width=math.ceil(w))
                for line in wrapped_text:
                    img_draw.text((x1, y1 + h), str(line.strip()), fill=field_style_config["font_color"], font=font)
                    # Block highest width
                    width = font.getsize(line)[0]
                    if width > width_field:
                        width_field = width
                    h += font.getsize(line)[1]
                h += 10
            y2_block = y1 + h
            x2_block = x1 + width_field
            # Ground Truth Data for each field
            if block_data:
                ground_truth[block["keyname"]][i + 1][data_field] = {"content": text, "x1": x1, "x2": x1 + width,
                                                                     "y1": y1, "y2": y1 + h}
                if j == block_length - 1:
                    h += 30
            else:
                ground_truth[data_field] = {"content": text, "x1": x1, "x2": x1 + width, "y1": y1, "y2": y1 + h}
    return img, (x1_block - 10, y1_block - 10, x2_block + 10, y2_block + 10), ground_truth


def get_font(field_config):
    font = ImageFont.truetype(field_config["font"], size=field_config["font_size"])
    return font


def get_keytext(field, text):
    """
    Generates data field key value pair to be rendered on image canvas
    :param field:
    :param text:
    :return:
    """
    field_direction = field["key_direction"]
    # TODO: Not generic (Need to generalize it to every field)
    keyname = random.choice(field["key_name"])
    if field_direction == "top":
        text = keyname + "\n" + str(text)
    elif field_direction == "left":
        text = keyname + str(text)
    return text
