import string
from colorsys import rgb_to_hsv
import random
from PIL import Image
import constants

def id_generator(size=5, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def lightness(pixel):
    # For backwards compatibility with python2
    return rgb_to_hsv(pixel[0], pixel[1], pixel[2])[2] / 255.0


def hue(pixel):
    return rgb_to_hsv(pixel[0], pixel[1], pixel[2])[0] / 255.0


def saturation(pixel):
    return rgb_to_hsv(pixel[0], pixel[1], pixel[2])[1] / 255.0


def random_width(clength):
    x = random.random()
    width = int(clength * (1 - x))
    return width


def crop_to(image_to_crop, reference_image):
    """
    Crops image to the size of a reference image. This function assumes that the relevant image is located in the center
    and you want to crop away equal sizes on both the left and right as well on both the top and bottom.
    :param image_to_crop
    :param reference_image
    :return: image cropped to the size of the reference image
    """
    reference_size = reference_image.size
    current_size = image_to_crop.size
    dx = current_size[0] - reference_size[0]
    dy = current_size[1] - reference_size[1]
    left = dx / 2
    upper = dy / 2
    right = dx / 2 + reference_size[0]
    lower = dy / 2 + reference_size[1]
    return image_to_crop.crop(box=(int(left), int(upper), int(right), int(lower)))


def get_pixels(data, mask, size):
    pixels = []
    for y in range(size[1]):
        pixels.append([])
        for x in range(size[0]):
            if not (mask and mask[x, y] == constants.black_pixel):
                pixels[y].append(data[x, y])
    return pixels


def place_pixels(pixels, mask, original, size):
    output_img = Image.new('RGBA', size)
    for y in range(size[1]):
        count = 0
        for x in range(size[0]):
            if mask and mask[x, y] == constants.black_pixel:
                output_img.putpixel((x, y), original[x, y])
            else:
                output_img.putpixel((x, y), pixels[y][count])
                count += 1
    return output_img
