import io
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont, ImageOps

WIDTH = 300
HEIGHT = 90
FONT_SIZE = 16
FONT = 'font.ttf'


def draw_date(draw: ImageDraw, date: datetime):
    font = ImageFont.truetype(FONT, FONT_SIZE)
    draw.text((10, 30), date.strftime("%d-%m-%Y"), font=font, fill=(0, 0, 0))


def draw_longstring(draw: ImageDraw, name: str, position: tuple):
    font = ImageFont.truetype(FONT, FONT_SIZE)

    font_size = FONT_SIZE
    if font.getsize(name)[0] > WIDTH:
        txt_length = font.getsize(name)[0]
        font_size *= WIDTH / txt_length
        font = ImageFont.truetype(FONT, int(font_size) - 1 if font_size > 2 else int(font_size))

    draw.text(position, name, font=font, fill=(0, 0, 0))


def convert(name: str, date: datetime, a_hash: str) -> io.BytesIO:
    img_without_border = Image.new('RGB', (WIDTH, HEIGHT), color=(255, 255, 255))
    img = ImageOps.expand(img_without_border, border=1, fill="black")

    d = ImageDraw.Draw(img)
    draw_date(d, date)
    draw_longstring(d, name, (10, 10))
    draw_longstring(d, a_hash, (10, 60))

    img_bytes = io.BytesIO()
    im1 = img.convert('RGB')
    im1.save(img_bytes, format='pdf')
    img_bytes.seek(0)
    return img_bytes
