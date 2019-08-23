try:
    import Image
    import ImageFilter
except ImportError:
    from PIL import Image, ImageFilter
import random as rand
import constants
import util
import logging

def edge(pixels, args):
    img = Image.open(args["image_input_path"])
    img = img.rotate(args["angle"], expand=True)
    edges = img.filter(ImageFilter.FIND_EDGES)
    edges = edges.convert('RGBA')
    edge_data = edges.load()

    filter_pixels = []
    edge_pixels = []
    intervals = []

    logging.debug("Defining edges...")
    for y in range(img.size[1]):
        filter_pixels.append([])
        for x in range(img.size[0]):
            filter_pixels[y].append(edge_data[x, y])

    logging.debug("Thresholding...")
    for y in range(len(pixels)):
        edge_pixels.append([])
        for x in range(len(pixels[y])):
            if util.lightness(filter_pixels[y][x]) < args["bottom_threshold"]:
                edge_pixels[y].append(constants.white_pixel)
            else:
                edge_pixels[y].append(constants.black_pixel)

    logging.debug("Cleaning up edges...")
    for y in range(len(pixels) - 1, 1, -1):
        for x in range(len(pixels[y]) - 1, 1, -1):
            if edge_pixels[y][x] == constants.black_pixel and edge_pixels[y][x - 1] == constants.black_pixel:
                edge_pixels[y][x] = constants.white_pixel

    logging.debug("Defining intervals...")
    for y in range(len(pixels)):
        intervals.append([])
        for x in range(len(pixels[y])):
            if edge_pixels[y][x] == constants.black_pixel:
                intervals[y].append(x)
        intervals[y].append(len(pixels[y]))
    return intervals


def threshold(pixels, args):
    intervals = []

    logging.debug("Defining intervals...")
    for y in range(len(pixels)):
        intervals.append([])
        for x in range(len(pixels[y])):
            if util.lightness(pixels[y][x]) < args["bottom_threshold"] or util.lightness(pixels[y][x]) > args["upper_threshold"]:
                intervals[y].append(x)
        intervals[y].append(len(pixels[y]))
    return intervals


def random(pixels, args):
    intervals = []

    logging.debug("Defining intervals...")
    for y in range(len(pixels)):
        intervals.append([])
        x = 0
        while True:
            width = util.random_width(args["clength"])
            x += width
            if x > len(pixels[y]):
                intervals[y].append(len(pixels[y]))
                break
            else:
                intervals[y].append(x)
    return intervals


def waves(pixels, args):
    intervals = []

    logging.debug("Defining intervals...")
    for y in range(len(pixels)):
        intervals.append([])
        x = 0
        while True:
            width = args["clength"] + rand.randint(0, 10)
            x += width
            if x > len(pixels[y]):
                intervals[y].append(len(pixels[y]))
                break
            else:
                intervals[y].append(x)
    return intervals


def file_mask(pixels, args):
    intervals = []
    file_pixels = []

    img = load_interval_file(args)
    data = img.load()
    for y in range(img.size[1]):
        file_pixels.append([])
        for x in range(img.size[0]):
            file_pixels[y].append(data[x, y])

    logging.debug("Cleaning up edges...")
    for y in range(len(pixels) - 1, 1, -1):
        for x in range(len(pixels[y]) - 1, 1, -1):
            if file_pixels[y][x] == constants.black_pixel and file_pixels[y][x - 1] == constants.black_pixel:
                file_pixels[y][x] = constants.white_pixel

    logging.debug("Defining intervals...")
    for y in range(len(pixels)):
        intervals.append([])
        for x in range(len(pixels[y])):
            if file_pixels[y][x] == constants.black_pixel:
                intervals[y].append(x)
        intervals[y].append(len(pixels[y]))

    return intervals


def file_edges(pixels, args):
    img = load_interval_file(args)
    edges = img.filter(ImageFilter.FIND_EDGES)
    edges = edges.convert('RGBA')
    edge_data = edges.load()

    filter_pixels = []
    edge_pixels = []
    intervals = []

    logging.debug("Defining edges...")
    for y in range(img.size[1]):
        filter_pixels.append([])
        for x in range(img.size[0]):
            filter_pixels[y].append(edge_data[x, y])

    logging.debug("Thresholding...")
    for y in range(len(pixels)):
        edge_pixels.append([])
        for x in range(len(pixels[y])):
            if util.lightness(filter_pixels[y][x]) < args["bottom_threshold"]:
                edge_pixels[y].append(constants.white_pixel)
            else:
                edge_pixels[y].append(constants.black_pixel)

    logging.debug("Cleaning up edges...")
    for y in range(len(pixels) - 1, 1, -1):
        for x in range(len(pixels[y]) - 1, 1, -1):
            if edge_pixels[y][x] == constants.black_pixel and edge_pixels[y][x - 1] == constants.black_pixel:
                edge_pixels[y][x] = constants.white_pixel

    logging.debug("Defining intervals...")
    for y in range(len(pixels)):
        intervals.append([])
        for x in range(len(pixels[y])):
            if edge_pixels[y][x] == constants.black_pixel:
                intervals[y].append(x)
        intervals[y].append(len(pixels[y]))
    return intervals


def none(pixels, args):
    intervals = []
    for y in range(len(pixels)):
        intervals.append([len(pixels[y])])
    return intervals

# Helper functions

def load_interval_file(args):
    img = Image.open(args["interval_file_path"])
    img = img.convert('RGBA')
    img = img.rotate(args["angle"], expand=True)
    img = img.resize(Image.open(args["image_input_path"]).size, Image.ANTIALIAS)
    return img