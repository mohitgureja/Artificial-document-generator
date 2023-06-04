from PIL import Image, ImageFont, ImageDraw


def generate_textimage(data):
    width = 2480
    height = 3508
    text = data["customer_name"]
    img = Image.new('RGB', (width, height))
    img_draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/arial.ttf", size=100)
    img_draw.text((20, 20), text, fill=(255, 255, 255), font=font)
    img.save('data/image.png')
    return img
