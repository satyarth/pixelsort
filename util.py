import random
import string
from colorsys import rgb_to_hsv


# Generates names for output files
def id_generator(size=5, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Determines the lightness of a pixel
def lightness(pixel):
    return rgb_to_hsv(pixel[0], pixel[1], pixel[2])[2] / 255.0  # For backwards compatibility with python2


def random_width(clength):
    x = random.random()
    width = int(clength * (1 - x))
    return width
