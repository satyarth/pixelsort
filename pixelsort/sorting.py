import random
import typing

import numpy as np

from pixelsort.super_pixel_image import SuperPixelImage


def sort_image(
    size: typing.Tuple[int, int],
    super_pixel_image: SuperPixelImage,
    mask_data: np.ndarray,
    intervals: typing.List,
    randomness: float,
    sorting_function: typing.Callable[[np.ndarray], np.ndarray],
) -> np.ndarray:
    """Sorts the super pixel grid row by row within the given intervals.

    Returns perm, where perm[y, x] is the source column of the super pixel to
    place at grid position (x, y). Unmasked positions keep their own column.
    """
    width, height = size
    keys = sorting_function(super_pixel_image.average_colors)
    perm = np.tile(np.arange(width), (height, 1))

    for y in range(height):
        masked = np.nonzero(mask_data[y])[0]
        if masked.size == 0:
            continue
        bounds = np.asarray(intervals[y], dtype=np.intp)
        interval_ids = np.searchsorted(bounds, masked, side="right")
        keep_unsorted = np.array(
            [random.random() * 100 < randomness for _ in range(len(bounds) + 1)]
        )
        # Unsorted intervals use the column itself as key, preserving order;
        # lexsort is stable and groups by interval before comparing keys.
        row_keys = np.where(keep_unsorted[interval_ids], masked, keys[y, masked])
        order = np.lexsort((row_keys, interval_ids))
        perm[y, masked] = masked[order]
    return perm


# Sort functions. Each takes the (height, width, 4) array of average colors
# and returns a (height, width) array of sort keys.


def _channels(average_colors: np.ndarray):
    rgb = average_colors.astype(np.float64)
    return rgb[..., 0], rgb[..., 1], rgb[..., 2]


def pixel_lightness(pixel: typing.Tuple[int, int, int]) -> float:
    """Lightness of a raw pixel tuple according to a HLS representation."""
    # taken from rgb_to_hls
    r, g, b = pixel[:3]
    maxc = max(r, g, b)
    minc = min(r, g, b)
    return (minc + maxc) / 2.0


def lightness(average_colors: np.ndarray) -> np.ndarray:
    """Sort by the lightness of a pixel according to a HLS representation."""
    # taken from rgb_to_hls
    r, g, b = _channels(average_colors)
    maxc = np.maximum(np.maximum(r, g), b)
    minc = np.minimum(np.minimum(r, g), b)
    return (minc + maxc) / 2.0


def hue(average_colors: np.ndarray) -> np.ndarray:
    """Sort by the hue of a pixel according to a HLS representation."""
    # taken from rgb_to_hls
    r, g, b = _channels(average_colors)
    maxc = np.maximum(np.maximum(r, g), b)
    minc = np.minimum(np.minimum(r, g), b)
    diffc = maxc - minc
    safe_diffc = np.where(diffc == 0, 1.0, diffc)
    rc = (maxc - r) / safe_diffc
    gc = (maxc - g) / safe_diffc
    bc = (maxc - b) / safe_diffc
    h = np.where(r == maxc, bc - gc, np.where(g == maxc, 2.0 + rc - bc, 4.0 + gc - rc))
    h = (h / 6.0) % 1.0
    return np.where(diffc == 0, 0.0, h)


def saturation(average_colors: np.ndarray) -> np.ndarray:
    """Sort by the saturation of a pixel according to a HLS representation."""
    # taken from rgb_to_hls
    r, g, b = _channels(average_colors)
    maxc = np.maximum(np.maximum(r, g), b)
    minc = np.minimum(np.minimum(r, g), b)
    sumc = minc + maxc
    diffc = maxc - minc
    sdiv = 2.0 - diffc
    s = np.where(
        sumc / 2.0 <= 0.5,
        diffc / np.where(sumc == 0, 1.0, sumc),
        diffc / np.where(sdiv == 0, 1.0, sdiv),
    )
    return np.where((diffc == 0) | (sumc == 0) | (sdiv == 0), 0.0, s)


def intensity(average_colors: np.ndarray) -> np.ndarray:
    """Sort by the intensity of a pixel, i.e. the sum of all the RGB values."""
    r, g, b = _channels(average_colors)
    return r + g + b


def minimum(average_colors: np.ndarray) -> np.ndarray:
    """Sort on the minimum RGB value of a pixel (either the R, G or B)."""
    r, g, b = _channels(average_colors)
    return np.minimum(np.minimum(r, g), b)


sorting_choices = {
    "lightness": lightness,
    "hue": hue,
    "intensity": intensity,
    "minimum": minimum,
    "saturation": saturation,
}
