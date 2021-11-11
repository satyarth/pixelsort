import logging
import typing

from PIL import Image

from pixelsort.constants import DEFAULTS
from pixelsort.interval import choices as interval_choices
from pixelsort.sorter import sort_image
from pixelsort.sorting import choices as sorting_choices
from pixelsort.util import crop_to


def pixelsort(
        image: Image.Image,
        mask_image: typing.Optional[Image.Image] = None,
        interval_image: typing.Optional[Image.Image] = None,
        randomness: float = DEFAULTS["randomness"],
        char_length: float = DEFAULTS["char_length"],
        sorting_function: typing.Literal["lightness", "hue", "saturation", "intensity", "minimum"] = DEFAULTS[
            "sorting_function"],
        interval_function: typing.Literal["random", "threshold", "edges", "waves", "file", "file-edges", "none"] =
        DEFAULTS["interval_function"],
        lower_threshold: float = DEFAULTS["lower_threshold"],
        upper_threshold: float = DEFAULTS["upper_threshold"],
        angle: float = DEFAULTS["angle"]
) -> Image.Image:
    """
    pixelsorts an image
    :param image: image to pixelsort
    :param mask_image: Image used for masking parts of the image.
    :param interval_image: Image used to define intervals. Must be black and white.
    :param randomness: What percentage of intervals *not* to sort. 0 by default.
    :param char_length:	Characteristic length for the random width generator. Used in mode `random` and `waves`.
    :param sorting_function: Sorting function to use for sorting the pixels.
    :param interval_function: Controls how the intervals used for sorting are defined.
    :param lower_threshold: How dark must a pixel be to be considered as a 'border' for sorting? Takes values from 0-1.
        Used in edges and threshold modes.
    :param upper_threshold: How bright must a pixel be to be considered as a 'border' for sorting? Takes values from
        0-1. Used in threshold mode.
    :param angle: Angle at which you're pixel sorting in degrees.
    :return: pixelsorted image
    """
    original = image
    image = image.convert('RGBA').rotate(angle, expand=True)
    image_data = image.load()

    mask_image = mask_image if mask_image else Image.new(
        "1", original.size, color=255)

    mask_data = (mask_image
                 .convert('1')
                 .rotate(angle, expand=True, fillcolor=0)
                 .load())

    interval_image = (interval_image
                      .convert('1')
                      .rotate(angle, expand=True)) if interval_image else None
    logging.debug("Determining intervals...")
    intervals = interval_choices[interval_function](
        image,
        lower_threshold=lower_threshold,
        upper_threshold=upper_threshold,
        char_length=char_length,
        interval_image=interval_image,
    )
    logging.debug("Sorting pixels...")
    sorted_pixels = sort_image(
        image.size,
        image_data,
        mask_data,
        intervals,
        randomness,
        sorting_choices[sorting_function])

    output_img = _place_pixels(
        sorted_pixels,
        mask_data,
        image_data,
        image.size)
    if angle != 0:
        output_img = output_img.rotate(-angle, expand=True)
        output_img = crop_to(output_img, original)

    return output_img


def _place_pixels(pixels, mask, original, size):
    output_img = Image.new('RGBA', size)
    for y in range(size[1]):
        count = 0
        for x in range(size[0]):
            if not mask[x, y]:
                output_img.putpixel((x, y), original[x, y])
            else:
                output_img.putpixel((x, y), pixels[y][count])
                count += 1
    return output_img
