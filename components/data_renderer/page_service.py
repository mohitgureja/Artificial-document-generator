def create_page_matrix(config):
    width_img, height_img = config["width"], config["height"]
    row_size, column_size = config["rows"]["n"], config["columns"]["n"]
    # If rows and columns are of equal size(in percentage)
    if config["rows"]["are_equal"]:
        config["rows"]["size"] = [100 / row_size] * row_size  # refer to the percent
    if config["columns"]["are_equal"]:
        config["columns"]["size"] = [100 / column_size] * column_size
    rows = [0] * (row_size + 1)
    col = [0] * (column_size + 1)
    # Calculate position of rows according to given percentage
    for i in range(1, row_size + 1):
        rows[i] = int(rows[i - 1] + (config["rows"]["size"][i - 1] * height_img) / 100)
    # Calculate position of columns according to given percentage
    for i in range(1, column_size + 1):
        col[i] = int(col[i - 1] + (config["columns"]["size"][i - 1] * width_img) / 100)
    # Add margins on sides, top and bottom
    if config["has_margins"]:
        height_margin = int((config["horizontal-margin"] * width_img) / 100)
        col[0] = height_margin
        col[column_size] = col[column_size] - height_margin
        width_margin = int((config["vertical-margin"] * height_img) / 100)
        rows[0] = width_margin
        rows[row_size] = rows[row_size] - width_margin
    # Make 2D matrix for rows and columns to divide page into blocks
    matrix = [[0] * column_size for i in range(row_size)]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = [(col[j], rows[i]), (col[j + 1], rows[i + 1])]  # Matrix in the form of [(x1,y1), (x2, y2)]
    return matrix
