import logging
import typing

import numpy as np
from PIL import Image

from pixelsort.constants import DEFAULTS
from pixelsort.interval import interval_choices
from pixelsort.sorting import sort_image
from pixelsort.sorting import sorting_choices
from pixelsort.util import crop_to
from pixelsort.super_pixel_image import SuperPixelImage


def pixelsort(
    image: Image.Image,
    mask_image: typing.Optional[Image.Image] = None,
    interval_image: typing.Optional[Image.Image] = None,
    randomness: float = DEFAULTS["randomness"],
    char_length: float = DEFAULTS["char_length"],
    sorting_function: typing.Literal[
        "lightness", "hue", "saturation", "intensity", "minimum"
    ] = DEFAULTS["sorting_function"],
    interval_function: typing.Literal[
        "random", "threshold", "edges", "waves", "file", "file-edges", "none"
    ] = DEFAULTS["interval_function"],
    lower_threshold: float = DEFAULTS["lower_threshold"],
    upper_threshold: float = DEFAULTS["upper_threshold"],
    angle: float = DEFAULTS["angle"],
    super_pixel_size: int = DEFAULTS["super_pixel_size"],
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
    :param super_pixel_size: Size of super pixels to sort. Defaults to 1 (single pixel).
    :return: pixelsorted image
    """
    original = image
    image = image.convert("RGBA").rotate(angle, expand=True)

    logging.debug("Converting to SuperPixelImage...")
    super_pixel_image = SuperPixelImage(image=image, super_pixel_size=super_pixel_size)

    logging.debug("Loading Mask...")
    mask_image = mask_image if mask_image else Image.new("1", original.size, color=255)
    mask_image = mask_image.convert("L").rotate(angle, expand=True, fillcolor=0)
    mask_data = _mask_array(mask_image, super_pixel_image)

    logging.debug("Loading Interval Image...")
    if interval_image:
        threshold = 200
        fn = lambda x: 255 if x > threshold else 0
        interval_image = interval_image.convert("L").rotate(angle, expand=True)
        if super_pixel_size > 1:
            interval_image = interval_image.reduce(super_pixel_size)
        interval_image = interval_image.point(fn, mode="1")

    logging.debug("Determining intervals...")
    intervals = interval_choices[interval_function](
        super_pixel_image,
        lower_threshold=lower_threshold,
        upper_threshold=upper_threshold,
        char_length=char_length,
        interval_image=interval_image,
    )
    logging.debug("Sorting pixels...")
    perm = sort_image(
        super_pixel_image.size,
        super_pixel_image,
        mask_data,
        intervals,
        randomness,
        sorting_choices[sorting_function],
    )

    logging.debug("Processing sorted pixels...")
    output_img = _place_blocks(perm, super_pixel_image)
    if angle != 0:
        output_img = output_img.rotate(-angle, expand=True)
        output_img = crop_to(output_img, original)

    final_image = original.convert("RGBA")

    # Squash pixel sorted image onto original to ensure no unexpected transparencies
    final_image.alpha_composite(output_img)

    logging.debug("Done...")
    return final_image


def _mask_array(
    mask_image: Image.Image, super_pixel_image: SuperPixelImage
) -> np.ndarray:
    """Mask as a boolean array on the super pixel grid: a block is sortable
    if any of its pixels are masked for sorting."""
    if super_pixel_image.super_pixel_size > 1:
        mask_image = mask_image.reduce(super_pixel_image.super_pixel_size)
    cols, rows = super_pixel_image.size
    mask = np.zeros((rows, cols), dtype=bool)
    source = np.asarray(mask_image)[:rows, :cols] > 0
    mask[: source.shape[0], : source.shape[1]] = source
    return mask


def _place_blocks(perm: np.ndarray, super_pixel_image: SuperPixelImage) -> Image.Image:
    """Rearranges the source image's super pixel blocks according to perm in
    one vectorized operation, at full resolution."""
    block = super_pixel_image.super_pixel_size
    cols, rows = super_pixel_image.size
    source_width, source_height = super_pixel_image.original_size

    source = np.asarray(super_pixel_image.source_image)
    pad_h = rows * block - source_height
    pad_w = cols * block - source_width
    source = np.pad(source, ((0, pad_h), (0, pad_w), (0, 0)))

    # One row of blocks at a time: map each output pixel column to its source
    # column, then gather. Padded (transparent) pixels travel with blocks that
    # straddle the right/bottom edge, matching the old paste() behavior.
    row_view = source.reshape(rows, block, cols * block, 4)
    col_map = (perm[:, :, None] * block + np.arange(block)).reshape(rows, cols * block)
    output = np.take_along_axis(row_view, col_map[:, None, :, None], axis=2)
    output = output.reshape(rows * block, cols * block, 4)

    return Image.fromarray(output[:source_height, :source_width], "RGBA")
