import logging
from PIL import Image

from pixelsort.util import crop_to
from pixelsort.sorter import sort_image
from pixelsort.constants import DEFAULTS
from pixelsort.interval import choices as interval_choices
from pixelsort.sorting import choices as sorting_choices


def pixelsort(
    image,
    mask_image=None,
    interval_image=None,
    randomness=DEFAULTS["randomness"],
    clength=DEFAULTS["clength"],
    sorting_function=DEFAULTS["sorting_function"],
    interval_function=DEFAULTS["interval_function"],
    lower_threshold=DEFAULTS["lower_threshold"],
    upper_threshold=DEFAULTS["upper_threshold"],
    angle=DEFAULTS["angle"]
):

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
        clength=clength,
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
