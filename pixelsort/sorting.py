import util


def lightness(pixel):
    return util.lightness(pixel)


def intensity(pixel):
    return pixel[0] + pixel[1] + pixel[2]


def hue(pixel):
    return util.hue(pixel)


def saturation(pixel):
    return util.saturation(pixel)


def minimum(pixel):
    return min(pixel[0], pixel[1], pixel[2])
