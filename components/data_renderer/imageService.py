import random
import textwrap

from PIL import Image, ImageFont, ImageDraw, ImageChops

from components.data_renderer import tableService, pageService


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
    y2_prev = [top_margin] * l
    x1_used_col = [0] * l
    rendered_data = []

    def test_previous_intersection(x1_c, x2_c, y1_c, y2_c):
        """
        Check if current position overlap with any of the previous blocks
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
            raise ValueError("Maximum recursion limit reached. Creating default coordinates")

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
                x1_c, y1_c, x2_c, y2_c, count = test_layout_semantics(x1_c, y1_c, x2_c, y2_c, row, column, cropped,
                                                                      count)
        print("Semantic test passed. ")
        count += 1
        return x1_c, y1_c, x2_c, y2_c, count

    # Image size
    width_img, height_img = page_config["width"], page_config["height"]
    img = Image.new('RGB', (width_img, height_img), "white")
    img_draw = ImageDraw.Draw(img)
    ground_truth = {}

    # Generate image using block by block configurations
    for block in position_config_data.keys():
        block = position_config_data[block]
        row, column = block["block_position"]
        x1 = random.randint(page_matrix[row][column][0][0], page_matrix[row][column][1][0])
        y1 = random.randint(page_matrix[row][column][0][1], page_matrix[row][column][1][1])

        if block["isImage"]:
            logo_img = "images/Logo.png"
            logo = Image.open(logo_img)
            bbox = ImageChops.invert(logo).getbbox()
            x1, y1, x2, y2, count = test_layout_semantics(x1, y1, x1 + bbox[2] - bbox[0], y1 + bbox[3] - bbox[1], row,
                                                          column, logo)
            img.paste(logo, (x1, y1, x2, y2))
        elif block["hasTable"]:
            cropped, tb_fields, x2, y2, ground_truth = tableService.draw_table(block, style_config_data, ground_truth,
                                                                               data, x1, y1, page_config)
            b_box_old = (x1, y1, x2, y2)
            x1, y1, x2, y2, count = test_layout_semantics(x1, y1, x2, y2, row, column, cropped)
            b_box_new = (x1, y1, x2, y2)
            ground_truth = tableService.get_updated_ground_truth(b_box_old, b_box_new, tb_fields, ground_truth)
            img.paste(cropped, (x1, y1, x2, y2))
        elif "data_fields" in block:
            img_new, b_box, ground_truth = get_block_image(block, data, fields, ground_truth, style_config_data, x1, y1,
                                                           page_config)
            cropped = img_new.crop(b_box)
            x2, y2 = create_b_box(cropped, x1, y1)
            if page_config["header_line"] and block["is_header"]:
                img_draw.line([(x1, y2),
                               (x2, y2)], fill="black", width=3)
                y2_prev[column] = y2
                rendered_data.append([x1, y1, x2, y2])
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


def get_block_image(block, data, fields, ground_truth, style_config_data, x1, y1, page_config):
    """
    Generate separate images for each block using position and configuration
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
    img = Image.new('RGB', (page_config["width"], page_config["height"]), "white")
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
