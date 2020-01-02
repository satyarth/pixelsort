from random import randint, random as random_range
from PIL import ImageFilter
from pixelsort.util import lightness


def edge(image, lower_threshold, **kwargs):
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


def threshold(image, lower_threshold, upper_threshold, **kwargs):
    intervals = []
    image_data = image.load()
    for y in range(image.size[1]):
        intervals.append([])
        for x in range(image.size[0]):
            level = lightness(image_data[x, y])
            if level < lower_threshold or level > upper_threshold:
                intervals[y].append(x)
    return intervals


def random(image, clength, **kwargs):
    intervals = []

    for y in range(image.size[1]):
        intervals.append([])
        x = 0
        while True:
            x += int(clength * random_range())
            if x > image.size[0]:
                break
            else:
                intervals[y].append(x)
    return intervals


def waves(image, clength, **kwargs):
    intervals = []

    for y in range(image.size[1]):
        intervals.append([])
        x = 0
        while True:
            x += clength + randint(0, 10)
            if x > image.size[0]:
                break
            else:
                intervals[y].append(x)
    return intervals


def file_mask(image, interval_image, **kwargs):
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


def file_edges(image, interval_image, lower_threshold, **kwargs):
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


def none(image, **kwargs):
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
