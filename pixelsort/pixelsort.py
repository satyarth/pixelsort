import logging
from PIL import Image

from pixelsort.util import crop_to
from pixelsort.sorter import sort_image
from pixelsort.constants import defaults, black_pixel
from pixelsort.interval import choices as interval_choices
from pixelsort.sorting import choices as sorting_choices


def pixelsort(
        image,
        mask_image=None,
        interval_image=None,
        randomness: float = defaults["randomness"],
        clength: int = defaults["clength"],
        sorting_function: str = defaults["sorting_function"],
        interval_function: str = defaults["interval_function"],
        lower_threshold: float = defaults["lower_threshold"],
        upper_threshold: float = defaults["upper_threshold"],
        angle: int = defaults["angle"]
    ) -> Image.Image:


    logging.debug("Cleaning input image...")
    image.convert('RGBA').rotate(angle, expand=True)

    logging.debug("Getting data...")
    input_data = image.load()

    mask_data = None
    if mask_image:
        logging.debug("Loading mask...")
        mask_data = (mask_image
                     .convert('RGBA')
                     .rotate(angle, expand=True)
                     .resize(image.size, Image.ANTIALIAS).load())

    if interval_image:
        logging.debug("Loading interval image...")
        (interval_image
         .convert('RGBA')
         .rotate(angle, expand=True)
         .resize(image.size, Image.ANTIALIAS))

    logging.debug("Getting pixels...")
    pixels = _get_pixels(input_data, mask_data, image.size)

    logging.debug("Determining intervals...")
    try:
        interval_function = interval_choices[interval_function]
    except KeyError:
        logging.warning("Invalid interval function specified, defaulting to 'threshold'.")
        interval_function = interval_choices["threshold"]
    intervals = interval_function(
        pixels,
        lower_threshold=lower_threshold,
        upper_threshold=upper_threshold,
        clength=clength,
        interval_image=interval_image,
        image=image
    )

    logging.debug("Sorting pixels...")
    try:
        sorting_function = sorting_choices[sorting_function]
    except KeyError:
        logging.warning("Invalid sorting function specified, defaulting to 'lightness'.")
        sorting_function = sorting_choices["lightness"]
    sorted_pixels = sort_image(pixels, intervals, randomness, sorting_function)

    logging.debug("Placing pixels in output image...")
    output_img = _place_pixels(sorted_pixels, mask_data, input_data, image.size)

    if angle is not 0:
        logging.debug("Rotating output image back to original orientation...")
        output_img = output_img.rotate(-angle, expand=True)

        logging.debug("Crop image to apropriate size...")
        output_img = crop_to(output_img, image)

    return output_img


def _get_pixels(data, mask, size):
    pixels = []
    for y in range(size[1]):
        pixels.append([])
        for x in range(size[0]):
            if not (mask and mask[x, y] == black_pixel):
                pixels[y].append(data[x, y])
    return pixels


def _place_pixels(pixels, mask, original, size):
    output_img = Image.new('RGBA', size)
    for y in range(size[1]):
        count = 0
        for x in range(size[0]):
            if mask and mask[x, y] == black_pixel:
                output_img.putpixel((x, y), original[x, y])
            else:
                output_img.putpixel((x, y), pixels[y][count])
                count += 1
    return output_img
