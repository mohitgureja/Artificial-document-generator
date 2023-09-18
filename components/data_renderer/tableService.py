import random

from PIL import ImageFont

from components.data_renderer.drawtable import Drawtable


def get_dependent_field_positions(x1, y1, x2, y2, width_list, fields, img_margin):
    x1, y1, x2, y2 = x1 + img_margin, y1 + img_margin, x2 - img_margin, y2 - img_margin
    x_diff = x2 - x1
    width_columns = [width_list[i] * x_diff for i in range(len(width_list))]
    table_ground_truth = {}
    for i in range(len(fields)):
        field_dict = {}
        if i == 0:
            field_dict["x1"] = x1
        else:
            field_dict["x1"] = x2 - sum(width_columns[i:])

        if i == len(fields) - 1:
            field_dict["x2"] = x2
        else:
            field_dict["x2"] = x2 - sum(width_columns[i + 1:])

        field_dict["y1"] = y1
        field_dict["y2"] = y2
        field_dict["content"] = ""
        table_ground_truth[fields[i]] = field_dict
    return table_ground_truth


def get_updated_ground_truth(b_box_old, b_box_new, tb_fields, ground_truth):
    for field in tb_fields:
        ground_truth[field]['x1'] = ground_truth[field]['x1'] + b_box_new[0] - b_box_old[0]
        ground_truth[field]['y1'] = ground_truth[field]['y1'] + b_box_new[1] - b_box_old[1]
        ground_truth[field]['x2'] = ground_truth[field]['x2'] + b_box_new[2] - b_box_old[2]
        ground_truth[field]['y2'] = ground_truth[field]['y2'] + b_box_new[3] - b_box_old[3]
    return ground_truth


def draw_table(block, style_config_data, ground_truth, data, x1, y1):
    tb_field_configs = block["table_data_fields"]
    tb_fields = list(tb_field_configs.keys())  # table field names
    list_tb_fields_data: list[int] = [0] * len(tb_fields)
    dependent_fields = []
    header_list = [""] * len(tb_fields)  # Initialize headers for the table

    for i, field in enumerate(tb_fields):
        list_tb_fields_data[i] = data[field]
        header_list[i] = random.choice(tb_field_configs[field]["header"])
        if tb_field_configs[field]["is_dependent_field"]:
            dependent_fields.append(field)

    tdata = [tuple(lst[i] for lst in list_tb_fields_data) for i in range(len(list_tb_fields_data[0]))]
    tdata.insert(0, tuple(header_list))
    field_config = style_config_data[tb_fields[0]]

    header_font = ImageFont.truetype(tb_field_configs[tb_fields[0]]["header_font"], size=field_config["font_size"] + 3)
    text_font = ImageFont.truetype(field_config["font"], size=field_config["font_size"])

    # Calculate column widths based on content length
    max_col_widths = [max([len(str(row[i])) for row in tdata]) for i in range(len(tdata[0]))]
    sum_width = sum(max_col_widths)
    width_list = [w / sum_width for w in max_col_widths]

    table = Drawtable(data=tdata,
                      x=60,
                      y=60,
                      font=text_font,
                      line_spacer=10,
                      margin_text=10,
                      image_width=1800,
                      image_height=1000,
                      columnwidth=width_list,
                      frame=False,
                      grid=False,
                      columngrid=False,
                      rowgrid=False,
                      header=True,
                      text_color='Black',
                      header_color='Black',
                      headerfont=header_font,
                      )

    image_details = table.draw_table()
    img_margin = 5

    bbox_params = [image_details[1] - img_margin, image_details[2] - img_margin, image_details[3] + img_margin,
                   image_details[4] + img_margin]
    cropped = image_details[0].crop(bbox_params)
    y2 = y1 + cropped.height
    x2 = x1 + cropped.width

    table_ground_truth = get_dependent_field_positions(x1, y1, x2, y2,
                                                       width_list, tb_fields, img_margin)
    for field in dependent_fields:
        ground_truth[field] = table_ground_truth[field]
    ground_truth[block["tableName"]] = {"content": tdata, "x1": x1, "x2": x2, "y1": y1, "y2": y2}
    return cropped, dependent_fields, x2, y2, ground_truth
