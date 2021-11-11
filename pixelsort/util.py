import time

from PIL import Image


def id_generator() -> str:
    timestr = time.strftime("%Y%m%d-%H%M%S")
    return timestr


def crop_to(image_to_crop: Image.Image, reference_image: Image.Image) -> Image.Image:
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
    return image_to_crop.crop(
        box=(
            int(left),
            int(upper),
            int(right),
            int(lower)))
