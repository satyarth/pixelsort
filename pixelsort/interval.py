import logging
from random import randint
from PIL import ImageFilter
from pixelsort.constants import BLACK_PIXEL, WHITE_PIXEL
from pixelsort.util import lightness, random_width


def edge(pixels, image, lower_threshold, **kwargs):
    edges = image.filter(ImageFilter.FIND_EDGES)
    edges = edges.convert('RGBA')
    edge_data = edges.load()

    filter_pixels = []
    edge_pixels = []
    intervals = []

    logging.debug("Defining edges...")
    for y in range(image.size[1]):
        filter_pixels.append([])
        for x in range(image.size[0]):
            filter_pixels[y].append(edge_data[x, y])

    logging.debug("Thresholding...")
    for y in range(len(pixels)):
        edge_pixels.append([])
        for x in range(len(pixels[y])):
            if lightness(filter_pixels[y][x]) < lower_threshold:
                edge_pixels[y].append(WHITE_PIXEL)
            else:
                edge_pixels[y].append(BLACK_PIXEL)

    logging.debug("Cleaning up edges...")
    for y in range(len(pixels) - 1, 1, -1):
        for x in range(len(pixels[y]) - 1, 1, -1):
            if edge_pixels[y][x] == BLACK_PIXEL and edge_pixels[y][x - 1] == BLACK_PIXEL:
                edge_pixels[y][x] = WHITE_PIXEL

    logging.debug("Defining intervals...")
    for y in range(len(pixels)):
        intervals.append([])
        for x in range(len(pixels[y])):
            if edge_pixels[y][x] == BLACK_PIXEL:
                intervals[y].append(x)
        intervals[y].append(len(pixels[y]))
    return intervals


def threshold(pixels, lower_threshold, upper_threshold, **kwargs):
    intervals = []

    logging.debug("Defining intervals...")
    for y in range(len(pixels)):
        intervals.append([])
        for x in range(len(pixels[y])):
            if lightness(pixels[y][x]) < lower_threshold or lightness(pixels[y][x]) > upper_threshold:
                intervals[y].append(x)
        intervals[y].append(len(pixels[y]))
    return intervals


def random(pixels, clength, **kwargs):
    intervals = []

    logging.debug("Defining intervals...")
    for y in range(len(pixels)):
        intervals.append([])
        x = 0
        while True:
            width = random_width(clength)
            x += width
            if x > len(pixels[y]):
                intervals[y].append(len(pixels[y]))
                break
            else:
                intervals[y].append(x)
    return intervals


def waves(pixels, clength, **kwargs):
    intervals = []

    logging.debug("Defining intervals...")
    for y in range(len(pixels)):
        intervals.append([])
        x = 0
        while True:
            width = clength + randint(0, 10)
            x += width
            if x > len(pixels[y]):
                intervals[y].append(len(pixels[y]))
                break
            else:
                intervals[y].append(x)
    return intervals


def file_mask(pixels, interval_image, **kwargs):
    intervals = []
    file_pixels = []

    data = interval_image.load()
    for y in range(interval_image.size[1]):
        file_pixels.append([])
        for x in range(interval_image.size[0]):
            file_pixels[y].append(data[x, y])

    logging.debug("Cleaning up edges...")
    for y in range(len(pixels) - 1, 1, -1):
        for x in range(len(pixels[y]) - 1, 1, -1):
            if file_pixels[y][x] == BLACK_PIXEL and file_pixels[y][x - 1] == BLACK_PIXEL:
                file_pixels[y][x] = WHITE_PIXEL

    logging.debug("Defining intervals...")
    for y in range(len(pixels)):
        intervals.append([])
        for x in range(len(pixels[y])):
            if file_pixels[y][x] == BLACK_PIXEL:
                intervals[y].append(x)
        intervals[y].append(len(pixels[y]))

    return intervals


def file_edges(pixels, interval_image, lower_threshold, **kwargs):
    edges = interval_image.filter(ImageFilter.FIND_EDGES)
    edges = edges.convert('RGBA')
    edge_data = edges.load()

    filter_pixels = []
    edge_pixels = []
    intervals = []

    logging.debug("Defining edges...")
    for y in range(interval_image.size[1]):
        filter_pixels.append([])
        for x in range(interval_image.size[0]):
            filter_pixels[y].append(edge_data[x, y])

    logging.debug("Thresholding...")
    for y in range(len(pixels)):
        edge_pixels.append([])
        for x in range(len(pixels[y])):
            if lightness(filter_pixels[y][x]) < lower_threshold:
                edge_pixels[y].append(WHITE_PIXEL)
            else:
                edge_pixels[y].append(BLACK_PIXEL)

    logging.debug("Cleaning up edges...")
    for y in range(len(pixels) - 1, 1, -1):
        for x in range(len(pixels[y]) - 1, 1, -1):
            if edge_pixels[y][x] == BLACK_PIXEL and edge_pixels[y][x - 1] == BLACK_PIXEL:
                edge_pixels[y][x] = WHITE_PIXEL

    logging.debug("Defining intervals...")
    for y in range(len(pixels)):
        intervals.append([])
        for x in range(len(pixels[y])):
            if edge_pixels[y][x] == BLACK_PIXEL:
                intervals[y].append(x)
        intervals[y].append(len(pixels[y]))
    return intervals


def none(pixels, **kwargs):
    intervals = []
    for y in range(len(pixels)):
        intervals.append([len(pixels[y])])
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
