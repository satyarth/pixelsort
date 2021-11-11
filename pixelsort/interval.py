from random import randint, random as random_range

from PIL import ImageFilter, Image

from pixelsort.util import lightness


def edge(image: Image.Image, lower_threshold: float):
    """Performs an edge detection, which is used to define intervals. Tweak threshold with threshold."""
    edge_data = image.filter(ImageFilter.FIND_EDGES).convert('RGBA').load()
    intervals = []

    for y in range(image.size[1]):
        intervals.append([])
        flag = True
        for x in range(image.size[0]):
            if lightness(edge_data[x, y]) < lower_threshold:
                flag = True
            elif flag:
                intervals[y].append(x)
                flag = False
    return intervals


def threshold(image: Image.Image, lower_threshold: float, upper_threshold: float):
    """Intervals defined by lightness thresholds; only pixels with a lightness between the upper and lower thresholds
     are sorted."""
    intervals = []
    image_data = image.load()
    for y in range(image.size[1]):
        intervals.append([])
        for x in range(image.size[0]):
            level = lightness(image_data[x, y])
            if level < lower_threshold or level > upper_threshold:
                intervals[y].append(x)
    return intervals


def random(image, char_length):
    """Randomly generate intervals. Distribution of widths is linear by default. Interval widths can be scaled using
    char_length."""
    intervals = []

    for y in range(image.size[1]):
        intervals.append([])
        x = 0
        while True:
            x += int(char_length * random_range())
            if x > image.size[0]:
                break
            else:
                intervals[y].append(x)
    return intervals


def waves(image, char_length):
    """Intervals are waves of nearly uniform widths. Control width of waves with char_length."""
    intervals = []

    for y in range(image.size[1]):
        intervals.append([])
        x = 0
        while True:
            x += char_length + randint(0, 10)
            if x > image.size[0]:
                break
            else:
                intervals[y].append(x)
    return intervals


def file_mask(image, interval_image):
    """Intervals taken from another specified input image. Must be black and white, and the same size as the input
    image."""
    intervals = []
    data = interval_image.load()

    for y in range(image.size[1]):
        intervals.append([])
        flag = True
        for x in range(image.size[0]):
            if data[x, y]:
                flag = True
            elif flag:
                intervals[y].append(x)
                flag = False
    return intervals


def file_edges(image, interval_image, lower_threshold):
    """Intervals defined by performing edge detection on the file specified by -f. Must be the same size as the input
    image."""
    edge_data = interval_image.filter(
        ImageFilter.FIND_EDGES).convert('RGBA').load()
    intervals = []

    for y in range(image.size[1]):
        intervals.append([])
        flag = True
        for x in range(image.size[0]):
            if lightness(edge_data[x, y]) < lower_threshold:
                flag = True
            elif flag:
                intervals[y].append(x)
                flag = False
    return intervals


def none(image):
    """Sort whole rows, only stopping at image borders."""
    intervals = []
    for y in range(image.size[1]):
        intervals.append([])
    return intervals


choices = {
    "random": random,
    "threshold": threshold,
    "edges": edge,
    "waves": waves,
    "file": file_mask,
    "file-edges": file_edges,
    "none": none
}
