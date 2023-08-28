# import PIL
# from PIL import Image, ImageFont
# from data_renderer.drawtable import Drawtable
#
# text_font = ImageFont.truetype("fonts/Arial.ttf", 16)  # PIL.ImageFont.truetype(FONT_PATH,FONTSIZE)
# header_font = ImageFont.truetype("fonts/Arial.ttf", 16)
# list_tb_data_fields = [["Hello", "Mohit"],["Hello","Nimritee"]]
# tdata = [tuple(lst[i] for lst in list_tb_data_fields) for i in range(2)]
# img = Image.open("/Users/ssdn/PycharmProjects/Artificial-document-generator/data/output/images/image1.png")
#
# table = Drawtable(data=tdata,
#                   x=60,
#                   y=80,
#                   font=text_font,
#                   line_spacer=10,
#                   margin_text=10,
#                   image_width=500,
#                   image_height=300,
#                   frame=True,
#                   grid=True,
#                   columngrid=False,
#                   rowgrid=False,
#                   header=True,
#                   text_color='green',
#                   header_color='red',
#                   headerfont=header_font,
#                   )
# image_details = table.draw_table()
# bbox_params = [image_details[1]-5, image_details[2]-5, image_details[3]+5, image_details[4]+5]
# cropped = image_details[0].crop(bbox_params)
# cropped.show()
# x1 = 500
# y1 = 500
# y2 = y1 + cropped.height
# x2 = x1 + cropped.width
# img.paste(cropped, (x1, y1, x2, y2))
# img.show()
# print("Hello")

import matplotlib.pyplot as plt
from PIL import Image


def generate_table(data, col_widths):
    fig, ax = plt.subplots()
    table = ax.table(cellText=data, cellLoc='center', loc='center', colWidths=col_widths)

    for i, cell in table._cells.items():
        cell.set_text_props(wrap=True, va='center', ha='center')

    ax.axis('off')
    plt.tight_layout()

    return fig


# Sample data for the table
data = [
    ['Header 1', 'Header 2', 'Header 3'],
    ['Cell 1,1', 'Cell 1,2',
     'A very long text in this cell A very long text in this cell A very long text in this cell'],
    ['Cell 2,1', 'Short text', 'Cell 2,3'],
    ['Cell 3,1', 'Cell 3,2', 'Another long text in this cell']
]

# Calculate column widths based on content length
max_col_widths = [max([len(str(row[i])) for row in data]) for i in range(len(data[0]))]
sum_width = sum(max_col_widths)
col_widths = [w / sum_width for w in max_col_widths]  # Adjust the scaling factor as needed

# Generate the table as a Matplotlib figure
table_fig = generate_table(data, col_widths)

# Convert the Matplotlib figure to a PIL image
table_fig.canvas.draw()
table_pil_image = Image.frombytes('RGB', table_fig.canvas.get_width_height(), table_fig.canvas.tostring_rgb())

# Load an existing PIL image where you want to paste the table
background_image = Image.open('/data/output/images/image0.png')

# Define the position to paste the table
paste_position = (200, 200)

# Paste the table image onto the background image
background_image.paste(table_pil_image, paste_position)

# Show or save the modified image
background_image.show()
# background_image.save('result_image.png')
