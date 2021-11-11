import random
import typing

# python implementation of the PixelAccess class returned by im.load(), has the same functions so is fine for type hints
from PIL import PyAccess


def sort_image(
        size: typing.Tuple[int, int],
        image_data: PyAccess.PyAccess,
        mask_data: PyAccess.PyAccess,
        intervals: typing.List[typing.List[int]],
        randomness: float,
        sorting_function: typing.Callable[[typing.Tuple[int, int, int]], float]):
    sorted_pixels = []

    for y in range(size[1]):
        row = []
        x_min = 0
        for x_max in intervals[y] + [size[0]]:
            interval = []
            for x in range(x_min, x_max):
                if mask_data[x, y]:
                    interval.append(image_data[x, y])
            if random.random() < randomness / 100:
                row += interval
            else:
                row += sort_interval(interval, sorting_function)
            x_min = x_max
        sorted_pixels.append(row)
    return sorted_pixels


def sort_interval(interval: typing.List, sorting_function: typing.Callable[[typing.Tuple[int, int, int]], float]):
    return [] if interval == [] else sorted(interval, key=sorting_function)
