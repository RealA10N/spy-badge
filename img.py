import os
import ipinfo
from PIL import Image, ImageDraw, ImageFont

handler = ipinfo.getHandler(os.environ['IPINFO_TOKEN'])
font = ImageFont.load_default()


def generate_image(ip: str):
    details = handler.getDetails(ip)

    text = ' | '.join((
        f'{name}: {value}'
        for name, value in details.details.items()
    ))


def text_image(text: str):
    size = font.getsize(text)
    img = Image.new('L', size, color='black')

    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, fill='white', font=font)

    return img
