from contextlib import contextmanager
from PIL import Image

from .quantize import mmcq


@contextmanager
def get_palette(filename, color_count=10):
    with Image.open(filename) as image:
        colors = []
        rgb = image.convert('RGB')
        for x in range(0, rgb.width, 5):
            for y in range(0, rgb.height, 5):
                rgb_color = rgb.getpixel((x, y))
                colors.append(rgb_color)

        c_map = mmcq(colors, color_count)
        yield c_map.palette


def get_dominant_color(filename, color_count=10):
    with get_palette(filename, color_count) as palette:
        return palette[0]
