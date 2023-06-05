import random

from PIL import Image, ImageFont, ImageDraw


def generate_textimage(data, fields, field_config):
    width = 2480
    height = 3508
    img = Image.new('RGB', (width, height), "white")
    img_draw = ImageDraw.Draw(img)

    for field in fields:
        print(field)
        text = data[field]
        config = field_config[field]
        font = ImageFont.truetype(config["font"], size=config["font_size"])
        print(font)
        x = random.randint(config["x1"], config["x2"])
        y = random.randint(config["y1"], config["y2"])
        img_draw.text((x, y), text, fill=(0, 0, 0), font=font)

    img.save('data/image.png')
    return img
