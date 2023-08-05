from .constant import SIGBITS


def get_color_index(r, g, b):
    return (r << (2 * SIGBITS)) + (g << SIGBITS) + b
